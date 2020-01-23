import json


class Configuration:
    """
    This class allows to get access to the configuration parameters
    """
    def __init__(self):
        with open('configuration/configuration.json', 'r') as configuration_file:
            configuration_file_content = configuration_file.read()
            self.__json_conf = json.loads(configuration_file_content)

    def get_api_id(self):
        """
        This method returns the Telegram API id from the configuration.
        :return:
        """
        return self.__json_conf['api_id']

    def get_api_hash(self):
        """
        This method returns the Telegram API hash from the configuration.
        :return:
        """
        return self.__json_conf['api_hash']

    def get_bot_token(self):
        """
        This method returns the bot token from the configuration.
        :return:
        """
        return self.__json_conf['bot_token']

    def get_nasa_api_key(self):
        """
        This method returns the NASA API Key from the configuration
        :return:
        """
        return self.__json_conf['nasa_api_key']


current_configuration = Configuration()


def get_current():
    return current_configuration
