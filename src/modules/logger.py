import modules.utils as utils
import logging
import logging.config
import os

# Create destination path if it does not exist
dest_path = os.path.join(utils.get_path(__file__), '..', '..', 'data', 'output', 'logs')
if not os.path.exists(dest_path):
    os.makedirs(dest_path)

# Read the configuration files
actual_path = utils.get_path(__file__)
config_path = os.path.join(actual_path, '..', '..', 'config')
logging.config.fileConfig(config_path+'/logger.conf')

# Create logger
logger = logging.getLogger('root')