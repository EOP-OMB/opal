from django.contrib.auth import get_user_model, REDIRECT_FIELD_NAME
from django.core import signing
from django.http import HttpResponse
from django.http.response import HttpResponseBase
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import logging
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.settings import OneLogin_Saml2_Settings
from onelogin.saml2.utils import OneLogin_Saml2_Utils

from sp.models import IdP
from sp.utils import get_request_idp, get_session_nameid


def metadata(request, **kwargs):
    idp = get_request_idp(request, **kwargs)
    saml_settings = OneLogin_Saml2_Settings(
        settings=idp.sp_settings, sp_validation_only=True
    )
    return HttpResponse(saml_settings.get_sp_metadata(), content_type="text/xml")


@csrf_exempt
@require_POST
def acs(request, **kwargs):
    logger = logging.getLogger('django')
    idp = get_request_idp(request, **kwargs)
    if request.POST.get("RelayState"):
        logger.info("Found RelayState in POST data")
        try:
            # Login with state relayed from our application.
            state = signing.loads(request.POST["RelayState"], max_age=idp.state_timeout)
        except (signing.BadSignature, signing.SignatureExpired) as ex:
            return render(
                request,
                "sp/error.html",
                {
                    "idp": idp,
                    "state": None,
                    "errors": [str(ex)],
                    "reason": "Invalid SSO request signature.",
                },
                status=500,
            )
    else:
        logger.info("IdP-initiated login.")
        state = {"test": False, "verify": False, "redir": ""}

    logger.info("Processing the saml response...")
    saml = OneLogin_Saml2_Auth(idp.prepare_request(request), old_settings=idp.settings)
    logger.info("saml.post_data = %s" % request.POST )
    saml.process_response()
    errors = saml.get_errors()
    if errors:
        logger.info("Error processing saml request")
        return render(
            request,
            "sp/error.html",
            {
                "idp": idp,
                "state": state,
                "errors": errors,
                "reason": saml.get_last_error_reason(),
            },
            status=500,
        )
    else:
        if state.get("test", False):
            logger.info("This is a test...")
            attrs = []
            for saml_attr, value in saml.get_attributes().items():
                attr, created = idp.attributes.get_or_create(saml_attribute=saml_attr)
                attrs.append((attr, "; ".join(value)))
            return render(
                request,
                "sp/test.html",
                {
                    "idp": idp,
                    "attrs": attrs,
                    "nameid": saml.get_nameid(),
                    "nameid_format": saml.get_nameid_format(),
                },
            )
        elif state.get("verify", False):
            logger.info("state.verify == true")
            user = idp.authenticate(request, saml)
            if user == request.user:
                logger.info("user == request.user")
                return redirect(idp.get_login_redirect(state.get("redir")))
            else:
                logger.info("user != request.user")
                return render(
                    request,
                    "sp/unauth.html",
                    {"nameid": idp.get_nameid(saml), "idp": idp, "verify": True},
                    status=401,
                )
        else:
            user = idp.authenticate(request, saml)
            logger.info("user = %s" % user)
            if user:
                if isinstance(user, HttpResponseBase):
                    return user
                else:
                    idp.login(request, user, saml)
                    idp.last_login = timezone.now()
                    idp.save(update_fields=("last_login",))
                    return redirect(idp.get_login_redirect(state.get("redir")))
            else:
                return render(
                    request,
                    "sp/unauth.html",
                    {"nameid": idp.get_nameid(saml), "idp": idp, "verify": False},
                    status=401,
                )


def slo(request, **kwargs):
    idp = get_request_idp(request, **kwargs)
    saml = OneLogin_Saml2_Auth(idp.prepare_request(request), old_settings=idp.settings)
    state = request.GET.get("RelayState")
    redir = saml.process_slo()
    errors = saml.get_errors()
    if errors:
        return render(
            request,
            "sp/error.html",
            {
                "idp": idp,
                "state": state,
                "errors": errors,
                "reason": saml.get_last_error_reason(),
            },
            status=500,
        )
    else:
        idp.logout(request)
        if not redir:
            redir = idp.get_logout_redirect(state)
        return redirect(redir)


def login(request, test=False, verify=False, **kwargs):
    idp = get_request_idp(request, **kwargs)
    if idp == "No IDP is defined":
        context = {
            'err_msg': "No IDP is defined"
            }
        return render(request, "error.html", context=context)
    else:
        saml = OneLogin_Saml2_Auth(idp.prepare_request(request), old_settings=idp.settings)
        reauth = verify or "reauth" in request.GET
        state = signing.dumps(
            {
                "test": test,
                "verify": verify,
                "redir": request.GET.get(REDIRECT_FIELD_NAME, ""),
            }
        )
        # When verifying, we want to pass the (unmapped) SAML nameid, stored in the session.
        # TODO: do we actually want UPN here, or some other specified mapped field? At least
        # Auth0 is pre-populating the email field with nameid, which is not what we want.
        nameid = get_session_nameid(request) if verify else None
        return redirect(saml.login(state, force_authn=reauth, name_id_value_req=nameid))


def logout(request, **kwargs):
    idp = get_request_idp(request, **kwargs)
    redir = idp.get_logout_redirect(request.GET.get(REDIRECT_FIELD_NAME))
    saml = OneLogin_Saml2_Auth(idp.prepare_request(request), old_settings=idp.settings)
    if saml.get_slo_url() and idp.logout_triggers_slo:
        # If the IdP supports SLO, send it a logout request (it will call our SLO).
        return redirect(saml.logout(redir))
    else:
        # Handle the logout "locally", i.e. log out via django.contrib.auth by default.
        idp.logout(request)
        return redirect(redir)



def bootstrap(request):
    bootstrap_saml_function()
    return redirect("/sso")

def bootstrap_saml_function():
    """Bootstraps the SP with a default "admin" user and a local test IdP."""
    User = get_user_model()
    if User.objects.filter(is_superuser=True).count() == 0:
        print(
            'Creating default "admin" account with password "letmein" '
            "-- change this immediately!"
        )
        User.objects.create_superuser(
            "admin",
            "admin@example.com",
            "letmein",
            first_name="Admin",
            last_name="User",
        )
    if IdP.objects.count() == 0:
        print('Creating "local" IdP for http://localhost:8000')
        idp = IdP.objects.create(
            name="Local SimpleSAML Provider",
            url_params={"idp_slug": "local"},
            base_url="http://localhost:8000",
            contact_name="Admin User",
            contact_email="admin@example.com",
            metadata_url="http://localhost:8888/simplesaml/saml2/idp/metadata.php",
            respect_expiration=True,
            logout_triggers_slo=True,
        )
        idp.generate_certificate()
        # The local IdP sends an email address, but it isn't the nameid. Override it
        # to be our nameid, AND set the email field on User.
        idp.attributes.create(
            saml_attribute="email", mapped_name="email", is_nameid=True
        )
        try:
            idp.import_metadata()
        except Exception:
            print(
                "Could not import IdP metadata; "
                "make sure your local IdP exposes {}".format(idp.metadata_url)
            )