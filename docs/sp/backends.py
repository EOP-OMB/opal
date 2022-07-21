import re

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import FieldDoesNotExist

from .models import IdPUser

UserModel = get_user_model()


class SAMLAuthenticationBackend(ModelBackend):
    def get_username(self, idp, saml):
        """
        For users not already associated with the IdP, generate a username to either
        look up and associate, or to use when creating a new User.
        """
        # Start with either the SAML nameid, or SAML attribute mapped to nameid.
        username = idp.get_nameid(saml)
        # Add IdP-specific prefix and suffix.
        username = idp.username_prefix + username + idp.username_suffix
        # Make sure the username is valid for Django's User model.
        username = re.sub(r"[^a-zA-Z0-9_@\+\.]", "-", username)
        # Make the username unique to the IdP, if SP_UNIQUE_USERNAMES is True.
        if getattr(settings, "SP_UNIQUE_USERNAMES", True):
            username += "-" + str(idp.pk)
        return username

    def authenticate(self, request, idp=None, saml=None):
        # The nameid (potentially mapped) to associate a User with an IdP.
        nameid = idp.get_nameid(saml)
        # A dictionary of SAML attributes, mapped to field names via IdPAttribute.
        attrs = idp.mapped_attributes(saml)
        created = False

        try:
            # If this nameid is already associated with a User, our job is done.
            user = idp.users.get(nameid=nameid).user
        except IdPUser.DoesNotExist:
            # Otherwise, associate or create a user with the generated username, if the
            # IdP settings allow it.
            username = self.get_username(idp, saml)
            username_field = UserModel.USERNAME_FIELD
            if not idp.auth_case_sensitive:
                username_field += "__iexact"
            try:
                # If we find an existing User, and the IdP allows it, associate them
                # with this IdP.
                user = UserModel._default_manager.get(**{username_field: username})
                if not idp.associate_users:
                    return None
                idp.users.create(nameid=nameid, user=user)
            except UserModel.DoesNotExist:
                if not idp.create_users:
                    return None
                # Create the User if the IdP allows it.
                user = UserModel(**{UserModel.USERNAME_FIELD: username})
                user.set_unusable_password()
                created = True
            except UserModel.MultipleObjectsReturned:
                # This can happen with case-insensitive auth.
                return None

        # The set of mapped attributes that should always be updated on the user.
        always_update = set(
            idp.attributes.filter(always_update=True).values_list(
                "mapped_name", flat=True
            )
        )

        # For users created by this backend, set initial user default values.
        if created:
            attrs.update(
                {default.field: [default.value] for default in idp.user_defaults.all()}
            )

        # Keep track of which fields (if any) were updated.
        update_fields = []
        for field, values in attrs.items():
            if created or field in always_update:
                try:
                    f = UserModel._meta.get_field(field)
                    # Only update if the field changed. This is a primitive check, but
                    # will catch most cases.
                    if values[0] != getattr(user, f.attname):
                        setattr(user, f.attname, values[0])
                        update_fields.append(f.name)
                except FieldDoesNotExist:
                    pass

        if created or update_fields:
            # Doing a full clean will make sure the values we set are of the correct
            # types before saving.
            user.full_clean(validate_unique=False)
            if created:
                user.save()
                idp.users.create(nameid=nameid, user=user)
            else:
                user.save(update_fields=update_fields)

        return user
