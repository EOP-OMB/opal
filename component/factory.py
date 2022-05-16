import factory
from .models import *


class responsible_rolesFactory(factory.Factory):
  class Meta:
    model = responsible_roles



class parametersFactory(factory.Factory):
  class Meta:
    model = parameters

  values = factory.Faker('text')


class control_implementationsFactory(factory.Factory):
  class Meta:
    model = control_implementations



class componentsFactory(factory.Factory):
  class Meta:
    model = components

  type = factory.Faker('text')
  title = factory.Faker('text')
  purpose = factory.Faker('text')
  status = factory.Faker('text')


class implemented_requirementsFactory(factory.Factory):
  class Meta:
    model = implemented_requirements



class statementsFactory(factory.Factory):
  class Meta:
    model = statements



class by_componentsFactory(factory.Factory):
  class Meta:
    model = by_components

  implementation_status = factory.Faker('text')


class exportFactory(factory.Factory):
  class Meta:
    model = export



class inheritedFactory(factory.Factory):
  class Meta:
    model = inherited



class satisfiedFactory(factory.Factory):
  class Meta:
    model = satisfied



class responsibilitiesFactory(factory.Factory):
  class Meta:
    model = responsibilities



class provided_control_implementationFactory(factory.Factory):
  class Meta:
    model = provided_control_implementation



