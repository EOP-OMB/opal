import factory
from .models import *


class import_profilesFactory(factory.Factory):
  class Meta:
    model = import_profiles

  href = factory.Faker('text')


class system_idsFactory(factory.Factory):
  class Meta:
    model = system_ids

  identifier_type = factory.Faker('text')
  system_id = factory.Faker('text')


class information_type_idsFactory(factory.Factory):
  class Meta:
    model = information_type_ids

  information_type_id = factory.Faker('text')


class categorizationsFactory(factory.Factory):
  class Meta:
    model = categorizations

  system = factory.Faker('text')


class information_type_impact_levelFactory(factory.Factory):
  class Meta:
    model = information_type_impact_level

  base = factory.Faker('text')
  selected = factory.Faker('text')


class information_typesFactory(factory.Factory):
  class Meta:
    model = information_types

  title = factory.Faker('text')
  description = factory.Faker('text')


class systems_informationFactory(factory.Factory):
  class Meta:
    model = systems_information



class diagramsFactory(factory.Factory):
  class Meta:
    model = diagrams

  caption = factory.Faker('text')


class authorization_boundariesFactory(factory.Factory):
  class Meta:
    model = authorization_boundaries



class network_architecturesFactory(factory.Factory):
  class Meta:
    model = network_architectures



class data_flowsFactory(factory.Factory):
  class Meta:
    model = data_flows



class system_characteristicsFactory(factory.Factory):
  class Meta:
    model = system_characteristics

  system_name = factory.Faker('text')
  system_name_short = factory.Faker('text')
  security_sensitivity_level = factory.Faker('text')
  security_impact_level = factory.Faker('text')
  security_objective_confidentiality = factory.Faker('text')
  security_objective_integrity = factory.Faker('text')
  security_objective_availability = factory.Faker('text')
  status = factory.Faker('text')


class leveraged_authorizationsFactory(factory.Factory):
  class Meta:
    model = leveraged_authorizations

  title = factory.Faker('text')


class system_functionsFactory(factory.Factory):
  class Meta:
    model = system_functions

  system_functions = factory.Faker('text')


class privilegesFactory(factory.Factory):
  class Meta:
    model = privileges

  title = factory.Faker('text')


class usersFactory(factory.Factory):
  class Meta:
    model = users

  title = factory.Faker('text')
  short_name = factory.Faker('text')


class inventory_itemsFactory(factory.Factory):
  class Meta:
    model = inventory_items



class system_implementationsFactory(factory.Factory):
  class Meta:
    model = system_implementations



class system_security_plansFactory(factory.Factory):
  class Meta:
    model = system_security_plans



