from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from sp.models import IdP


class Command(BaseCommand):
    help = 'Bootstraps the SP with a default "admin" user and a local test IdP.'

    def handle(self, *args, **options):
        User = get_user_model()
        if User.objects.count() == 0:
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
        admin = User.objects.filter(is_superuser=True).first()
        if IdP.objects.count() == 0:
            print('Creating "local" IdP for http://localhost:8000')
            idp = IdP.objects.create(
                name="Local SimpleSAML Provider",
                url_params={"idp_slug": "local"},
                base_url="http://localhost:8000",
                contact_name=admin.get_full_name(),
                contact_email=admin.email,
                metadata_url="http://localhost:8080/simplesaml/saml2/idp/metadata.php",
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

            print('Creating "stub" IdP at https://stubidp.sustainsys.com/Metadata')
            idp = IdP.objects.create(
                name="Sustainsys Stub",
                url_params={"idp_slug": "stub"},
                base_url="http://localhost:8000",
                contact_name=admin.get_full_name(),
                contact_email=admin.email,
                metadata_url="https://stubidp.sustainsys.com/Metadata",
                logout_triggers_slo=True,
                require_attributes=False,
            )
            idp.generate_certificate()
            try:
                idp.import_metadata()
            except Exception:
                print(
                    "Could not import IdP metadata; "
                    "make sure {} is available to download".format(idp.metadata_url)
                )
