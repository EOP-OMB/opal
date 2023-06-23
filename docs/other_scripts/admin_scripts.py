import logging
import json
import xmltodict
from django.apps import apps
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from io import StringIO

USER_APPS = settings.USER_APPS

"""Useful functions for testing or administration"""

def check_auth(action):
    user = get_user_model()
    if not user.objects.filter(is_superuser=True).exists():
        return True
    return False


def reset_db(app_name):
    logger = logging.getLogger("django")
    app_models = apps.get_app_config(app_name).get_models()
    logger.info("Deleting all records from app " + app_name)
    for model in app_models:
        logger.info("Deleting " + str(model.objects.count()) + " items from " + model._meta.model_name)
        model.objects.all().delete()
        logger.info("Done. " + str(model.objects.count()) + " items remain in " + model._meta.model_name)


def reset_all_db():
    for app in USER_APPS:
        reset_db(app)


def get_fake_request(path='/', user=None):
    """ Construct a fake request(WSGIRequest) object"""
    req = WSGIRequest(
        {
            'REQUEST_METHOD': 'GET', 'PATH_INFO': path, 'wsgi.input': StringIO(), 'SERVER_NAME': "localhost", "SERVER_PORT": "8000"
            }
        )

    # req.user = AnonymousUser() if user is None else user
    return req


def convert_xml_to_json(file_path):
    with open(file_path) as xml_file:
        data_dict = xmltodict.parse(xml_file.read())
        xml_file.close()

        # generate the object using json.dumps()
        # corresponding to json data

        json_data = json.dumps(data_dict)

        # Write the json data to output
        # json file
        with open("data.json", "w") as json_file:
            json_file.write(json_data)
            json_file.close()

