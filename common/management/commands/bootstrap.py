from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from catalog.models import available_catalog_list
from catalog.views import download_catalog, import_catalog_task
from common.models import roles
from sp.models import IdP


def create_admin_user(user):
    password = user.objects.make_random_password()
    user.objects.create_superuser(
        "admin",
        "",
        password,
        first_name="Admin",
        last_name="User",
        )
    return password


def load_default_role_list():
    import json
    f = open("common/management/commands/role_list.json", "r")
    default_role_list = json.load(f)
    for role in default_role_list:
        roles.objects.get_or_create(**role)
    return default_role_list


def load_catalog_import_list():
    catalog_list = [
                    # 'https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_HIGH-baseline-resolved-profile_catalog-min.json',
                    # 'https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_MODERATE-baseline-resolved-profile_catalog-min.json',
                    # 'https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_LOW-baseline-resolved-profile_catalog-min.json',
                    # 'https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_PRIVACY-baseline-resolved-profile_catalog-min.json',
                    'https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json',]
    for c in catalog_list:
        catalog_dict = download_catalog(c)
        available_catalog_list_item = {
            'catalog_uuid': catalog_dict['uuid'],
            'name': catalog_dict['metadata']['title'],
            'link': c,
            }
        available_catalog_list.objects.get_or_create(**available_catalog_list_item)
    return catalog_list


class Command(BaseCommand):
    help = 'Bootstraps the app with a default "admin" user, a test IdP, default roles, and a default catalog list.'

    def handle(self, *args, **options):
        # If no admin user exists, create an admin account
        user = get_user_model()
        if not user.objects.filter(is_superuser=True).exists():
            password = create_admin_user(user)
            print("Created account 'admin' with password '%s'. This password will not be displayed again." % password)

        # create a sample idp if none exists
        if IdP.objects.count() == 0:
            print('Creating "stub" IdP at https://stubidp.sustainsys.com/Metadata')
            idp = IdP.objects.create(
                name="Sustainsys Stub",
                url_params={"idp_slug": "stub"},
                base_url="http://localhost:8000",
                contact_name="admin",
                contact_email="admin@example.com",
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

        # Populate the Catalog import list
        catalog_list = load_catalog_import_list()

        print("Added %s entries to the available catalog list" % len(catalog_list))

        # Add some default roles
        default_role_list = load_default_role_list()
        print("Added %s default roles" % len(default_role_list))

        # import sample Catalog
        import_catalog_task(test=True)