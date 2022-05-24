import factory
from .models import *


class importsFactory(factory.Factory):
    class Meta:
        model = imports

    href = factory.Faker('text')
    import_type = factory.Faker('text')


class modifyFactory(factory.Factory):
    class Meta:
        model = modify


class profileFactory(factory.Factory):
    class Meta:
        model = profile

    merge = factory.Faker('text')
