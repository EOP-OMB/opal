from ssp.models.common import *


# elements of a user, role, and group
class user_function(BasicModel):
    """
    list of functions assigned to roles. e.g. backup servers, deploy software, etc.
    """


class user_privilege(BasicModel):
    functionsPerformed = customMany2ManyField(user_function)


class user_role(ExtendedBasicModel):
    user_privileges = customMany2ManyField(user_privilege)


# elements that can apply to a user, organization or both
class address(BasicModel):
    type = models.CharField(max_length=100)
    postal_address = customTextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    postal_code = models.CharField(max_length=25)
    country = models.CharField(max_length=100)


class email(PrimitiveModel):
    email = models.EmailField()
    type = models.CharField(max_length=50, choices=contactInfoType, default='work')
    supports_rich_text = models.BooleanField(default=True)

    def __str__(self):
        return self.type + ': ' + self.email


class telephone_number(PrimitiveModel):
    number = models.CharField(max_length=25)
    type = models.CharField(max_length=25)

    def __str__(self):
        return self.type + ': ' + self.number


class location(ExtendedBasicModel):
    address = models.ForeignKey(address, on_delete=models.PROTECT)
    emailAddresses = customMany2ManyField(email)
    telephoneNumbers = customMany2ManyField(telephone_number)


class organization(ExtendedBasicModel):
    """
    Groups of people
    """
    locations = customMany2ManyField(location)
    email_addresses = customMany2ManyField(email)
    telephone_numbers = customMany2ManyField(telephone_number)


class person(ExtendedBasicModel):
    """
    An individual who can be assigned roles within a system.
    """
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=25)
    organizations = customMany2ManyField(organization)
    locations = customMany2ManyField(location)
    email_addresses = customMany2ManyField(email)
    telephone_numbers = customMany2ManyField(telephone_number)

    def __str__(self):
        return self.name
