from factory.django import DjangoModelFactory
from factory import Faker
from .models import *


class testsFactory(DjangoModelFactory):
  class Meta:
    model = tests

  expression = Faker('text')


class constraintsFactory(DjangoModelFactory):
  class Meta:
    model = constraints



class guidelinesFactory(DjangoModelFactory):
  class Meta:
    model = guidelines



class paramsFactory(DjangoModelFactory):
  class Meta:
    model = params

  param_id = Faker('text')
  param_class = Faker('text')
  label = Faker('text')
  values = Faker('text')
  select = Faker('text')
  how_many = Faker('text')


class partsFactory(DjangoModelFactory):
  class Meta:
    model = parts

  part_id = Faker('text')
  name = Faker('text')
  ns = Faker('text')
  part_class = Faker('text')
  title = Faker('text')


class controlsFactory(DjangoModelFactory):
  class Meta:
    model = controls

  control_id = Faker('text')
  control_class = Faker('text')
  title = Faker('text')


class groupsFactory(DjangoModelFactory):
  class Meta:
    model = groups

  group_id = Faker('text')
  group_class = Faker('text')
  title = Faker('text')


class catalogsFactory(DjangoModelFactory):
  class Meta:
    model = catalogs



