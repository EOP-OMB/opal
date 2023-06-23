import logging
from uuid import UUID
from django.apps import apps
from django.conf import settings
from django.core.exceptions import FieldError, ObjectDoesNotExist

"""
Some useful common functions
"""


def replace_hyphen(s: str):
    logger = logging.getLogger("django")
    logger.debug("replacing hyphen in " + s + " with underscore.")
    return s.replace("-", "_")


# got this from https://towardsdatascience.com/4-cute-python-functions-for-working-with-dirty-data-2cf7974280b5
def coalesce(*values):
    """Return the first non-None value or None if all values are None"""
    return next((v for v in values if v is not None and v != ""), "N/A")


def search_for_uuid(uuid_str, app_list=settings.USER_APPS):
    logger = logging.getLogger("django")
    try:
        logger.info("Searching for uuid: " + uuid_str)
        for a in app_list:
            logger.info("Looking in app " + a.title())
            app_models = apps.get_app_config(a).get_models()
            logger.info("Got list of models")
            for model in app_models:
                logger.info("Trying " + model._meta.model_name)
                try:
                    if model.objects.filter(uuid=uuid_str).count() > 0:
                        logging.debug("Found matching!")
                        return model.objects.get(uuid=uuid_str)
                except FieldError:
                    logging.warning("%s uuid field does not exist!!" % model._meta.model_name)
        logger.info("Could not find an object with uuid: " + uuid_str)
        return None
    except ValueError:
        logger.info(uuid_str + " is not a valid uuid")
        return None



