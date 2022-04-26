import factory
from .models import *


class port_rangesFactory(factory.Factory):
  class Meta:
    model = port_ranges

  start = factory.Faker('random_int')
  end = factory.Faker('random_int')
  transport = factory.Faker('text')


class protocolsFactory(factory.Factory):
  class Meta:
    model = protocols

  name = factory.Faker('text')
  title = factory.Faker('text')


class propsFactory(factory.Factory):
  class Meta:
    model = props

  name = factory.Faker('text')
  ns = factory.Faker('text')
  value = factory.Faker('text')
  property_class = factory.Faker('text')


class linksFactory(factory.Factory):
  class Meta:
    model = links

  href = factory.Faker('text')
  rel = factory.Faker('text')
  media_type = factory.Faker('text')
  text = factory.Faker('text')


class revisionsFactory(factory.Factory):
  class Meta:
    model = revisions

  title = factory.Faker('text')
  version = factory.Faker('text')
  oscal_version = factory.Faker('text')


class document_idsFactory(factory.Factory):
  class Meta:
    model = document_ids

  scheme = factory.Faker('text')
  identifier = factory.Faker('text')


class rolesFactory(factory.Factory):
  class Meta:
    model = roles

  role_id = factory.Faker('text')
  title = factory.Faker('text')
  short_name = factory.Faker('text')
  description = factory.Faker('text')


class emailsFactory(factory.Factory):
  class Meta:
    model = emails

  email_address = factory.Faker('text')


class telephone_numbersFactory(factory.Factory):
  class Meta:
    model = telephone_numbers

  type = factory.Faker('text')
  number = factory.Faker('text')


class addressesFactory(factory.Factory):
  class Meta:
    model = addresses

  type = factory.Faker('text')
  city = factory.Faker('text')
  state = factory.Faker('text')
  postal_code = factory.Faker('text')
  country = factory.Faker('text')


class locationsFactory(factory.Factory):
  class Meta:
    model = locations

  title = factory.Faker('text')


class external_idsFactory(factory.Factory):
  class Meta:
    model = external_ids

  scheme = factory.Faker('text')
  external_id = factory.Faker('text')


class organizationsFactory(factory.Factory):
  class Meta:
    model = organizations



class partiesFactory(factory.Factory):
  class Meta:
    model = parties

  type = factory.Faker('text')
  name = factory.Faker('text')
  short_name = factory.Faker('text')


class responsible_partiesFactory(factory.Factory):
  class Meta:
    model = responsible_parties

  role_id = factory.Faker('text')


class metadataFactory(factory.Factory):
  class Meta:
    model = metadata

  title = factory.Faker('text')
  version = factory.Faker('text')
  oscal_version = factory.Faker('text')


class citationsFactory(factory.Factory):
  class Meta:
    model = citations

  text = factory.Faker('text')


class hashesFactory(factory.Factory):
  class Meta:
    model = hashes

  algorithm = factory.Faker('text')


class rlinksFactory(factory.Factory):
  class Meta:
    model = rlinks



class base64Factory(factory.Factory):
  class Meta:
    model = base64

  filename = factory.Faker('text')
  media_type = factory.Faker('text')


class resourcesFactory(factory.Factory):
  class Meta:
    model = resources

  title = factory.Faker('text')


class back_matterFactory(factory.Factory):
  class Meta:
    model = back_matter



