import factory
from .models import *


class testsFactory(factory.Factory):
  class Meta:
    model = tests

  expression = factory.Faker('text')


class constraintsFactory(factory.Factory):
  class Meta:
    model = constraints



class guidelinesFactory(factory.Factory):
  class Meta:
    model = guidelines



class paramsFactory(factory.Factory):
  class Meta:
    model = params

  param_id = factory.Faker('text')
  param_class = factory.Faker('text')
  label = factory.Faker('text')
  values = factory.Faker('text')
  select = factory.Faker('text')
  how_many = factory.Faker('text')


class partsFactory(factory.Factory):
  class Meta:
    model = parts

  part_id = factory.Faker('text')
  name = factory.Faker('text')
  ns = factory.Faker('text')
  part_class = factory.Faker('text')
  title = factory.Faker('text')


class controlsFactory(factory.Factory):
  class Meta:
    model = controls

  control_id = factory.Faker('text')
  control_class = factory.Faker('text')
  title = factory.Faker('text')


class groupsFactory(factory.Factory):
  class Meta:
    model = groups

  group_id = factory.Faker('text')
  group_class = factory.Faker('text')
  title = factory.Faker('text')


class catalogsFactory(factory.Factory):
  class Meta:
    model = catalogs



