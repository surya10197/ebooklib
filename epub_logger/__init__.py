import os
import json
import logging.config


parent_dir = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(parent_dir, 'logging.json')) as log_config_file:
    log_config = json.load(log_config_file)

logging.config.dictConfig(log_config)
logger = logging.getLogger(__name__)