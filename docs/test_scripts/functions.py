from django.conf import settings
from django.apps import apps
import os


def generate_model_factory(model):
    opts = model._meta
    str = "class " + opts.model_name + "Factory(factory.Factory):\n"
    str += "  class Meta:\n"
    str += "    model = " + opts.model_name + "\n\n"
    for f in opts.concrete_fields:
        if f.name not in ['id','created_at','updated_at','uuid']:
            if f.get_internal_type() == 'CharField':
                str += "  " + f.name + " = factory.Faker('text')\n"
            if f.get_internal_type() == 'IntegerField':
                str += "  " + f.name + " = factory.Faker('random_int')\n"
    return str


def create_model_factories(app_list=settings.USER_APPS):
    for a in app_list:
        # create a factory file
        file_name = os.path.join(settings.BASE_DIR, a, 'factory.py')
        with open(file_name, 'w') as f:
            model_count = 0
            f.write("import factory\n")
            f.write("from .models import *\n\n\n")
            app_models = apps.get_app_config(a).get_models()
            for model in app_models:
                model_count += 1
                f.write(generate_model_factory(model))
                f.write("\n\n")
        f.close()
        print("created file " + file_name + " with " + str(model_count) + " models.")
    return True