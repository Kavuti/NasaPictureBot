import json
import logging.config
import os

environment = True

file_dir = os.path.split(os.path.realpath(__file__))[0]
logging.config.fileConfig(os.path.join(file_dir, 'logging.ini'),
                          disable_existing_loggers=False)


class Configuration:
    """
    This class allows to get access to the configuration parameters
    """
    def __init__(self):
        if environment:
            self.__api_id = os.environ.get('API_ID')
            self.__api_hash = os.environ.get('API_HASH')
            self.__bot_token = os.environ.get('BOT_TOKEN')
            self.__nasa_api_key = os.environ.get('NASA_API_KEY')
            self.__db_uri = os.environ.get('DATABASE_URL')
        else:
            with open('configuration/configuration.json', 'r') as configuration_file:
                configuration_file_content = configuration_file.read()
                __json_conf = json.loads(configuration_file_content)
                self.__api_id = __json_conf['api_id']
                self.__api_hash = __json_conf['api_hash']
                self.__bot_token = __json_conf['bot_token']
                self.__nasa_api_key = __json_conf['nasa_api_key']
                self.__db_uri = __json_conf['db_uri']
        self.__logger = logging.getLogger('root')

    def get_api_id(self):
        """
        This method returns the Telegram API id from the configuration.
        :return:
        """
        return self.__api_id

    def get_api_hash(self):
        """
        This method returns the Telegram API hash from the configuration.
        :return:
        """
        return self.__api_hash

    def get_bot_token(self):
        """
        This method returns the bot token from the configuration.
        :return:
        """
        return self.__bot_token

    def get_nasa_api_key(self):
        """
        This method returns the NASA API Key from the configuration
        :return:
        """
        return self.__nasa_api_key

    def get_db_uri(self):
        """
        This method returns the database URI from the configuration
        :return:
        """
        return self.__db_uri

    def get_logger(self):
        """
        This method returns a configured logger.
        :return:
        """
        return self.__logger


current_configuration = Configuration()


def get_current():
    return current_configuration

