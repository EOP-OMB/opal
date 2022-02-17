import logging



"""
Some useful common functions
"""

import logging.handlers
import os

# your logging setup

def start_logging():
    log_filename = "opal_debug.log"
    # should_roll_over = os.path.isfile(log_filename)
    # handler = logging.handlers.RotatingFileHandler(log_filename, mode='w', backupCount=5)
    # if should_roll_over:  # log already exists, roll over!
    #     handler.doRollover()
    logging.basicConfig(
        filename=log_filename,
        format='%(asctime)s %(name)-12s %(pathname)s:%(lineno)d %(levelname)-8s %(message)s',
        filemode='w'
        )
    logger = logging.getLogger()
    logger.setLevel("DEBUG")
    return logger

def replace_hyphen(s: str):
    logger = logging.getLogger("file")
    logger.debug("replacing hyphen in " + s + " with underscore.")
    return s.replace("-", "_")


def reset_db(app_name):
    logger = start_logging()
    from django.apps import apps
    app_models = apps.get_app_config(app_name).get_models()
    logger.info("Deleting all records from app " + app_name)
    for model in app_models:
        logger.debug("Deleting " + str(model.objects.count()) + " items from " + model._meta.model_name)
        model.objects.all().delete()
        logger.debug("Done. " + str(model.objects.count()) + " items remain in " + model._meta.model_name)

def reset_all_db():
    reset_db('catalog')
    reset_db('ssp')
    reset_db('common')

