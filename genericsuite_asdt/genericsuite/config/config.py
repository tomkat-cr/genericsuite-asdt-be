"""
Configuration manager
"""
# C0103 | Disable "name doesn't conform to naming rules..." (snake_case)
# pylint: disable=C0103
# R0902 | Disable "too-many-instance-attributes"
# pylint: disable=R0902
# R0903 | Disable "too-few-public-methods"
# pylint: disable=R0903
# R0915 | Disable "too-many-statements "
# pylint: disable=R0915
# W0105 | Disable "pointless-string-statement" (for """ comments)
# pylint: disable=W0105
# C0301: | Disable "line-too-long"
# pylint: disable=C0301

from typing import Union, Any
import os
import json
import logging
import datetime


# from genericsuite.config.config_secrets import get_secrets_from_iaas


def get_default_resultset() -> dict:
    """Returns an standard base resultset, to be used in the building
       of responses to the outside world
    """
    resultset = {
        'error': False,
        'error_message': None,
        'totalPages': None,
        'resultset': {}
    }
    return resultset


def formatted_log_message(message: str) -> str:
    """ Returns a formatted message with database name and date/time """
    return f"[{os.environ.get('APP_DB_NAME', 'APP_DB_NAME not set')}]" + \
        f" {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}" + \
        f" | {message}"


def get_config_logger() -> logging.Logger:
    """
    Get the logger object.
    """
    return logging.getLogger(os.environ.get('APP_NAME'))


def config_log_error(message: str) -> None:
    """
    Log a message to the console.
    """
    get_config_logger().error("%s", formatted_log_message(message))


def config_log_debug(message: str) -> None:
    """
    Log a message to the console.
    """
    get_config_logger().debug("%s", formatted_log_message(message))


def config_log_info(message: str) -> None:
    """
    Log a message to the console.
    """
    get_config_logger().debug("%s", formatted_log_message(message))


def text_to_dict(text: str) -> Union[dict, None]:
    """
    Convert a text string to a dictionary.
    """
    result = None
    try:
        result = json.loads(text)
    except json.JSONDecodeError as e:
        config_log_error(f'ERROR [C-E010] | converting text to dict: {e}')
    return result


def is_local_service() -> bool:
    return os.environ.get('AWS_SAM_LOCAL') == 'true' or \
        os.environ.get('GS_LOCAL_ENVIR') == 'true'


class Config():
    """ Configuration class, to have the most used App variables """
    def __init__(self, app_context: Any = None) -> None:

        # Set the local app_context to eventually get values from
        # Database (any other place than the App initialization)
        self.app_context = app_context

        # Get secrets and set environment variables
        # params = get_secrets_from_iaas(get_default_resultset,
        #                                get_config_logger())
        # if params["error"]:
        #     error_msg = 'CNFG-1) ERROR: Config.__init__() |' + \
        #                 f' Getting Secrets | params: {params}'
        #     raise Exception(error_msg)

        # ............................

        # IMPORTANT: these parameters values must be always retrieved
        # from environment variables

        # Database configuration

        if is_local_service():
            # Handles the \@ issue in environment variables values when runs
            # by "sam local start-api"
            os.environ['APP_DB_URI'] = \
                os.environ['APP_DB_URI'].replace('\\@', '@')
            os.environ['APP_SUPERADMIN_EMAIL'] = \
                os.environ['APP_SUPERADMIN_EMAIL'].replace('\\@', '@')

        self.DB_CONFIG = {
            'mongodb_uri': os.environ['APP_DB_URI'],
            'mongodb_db_name': os.environ['APP_DB_NAME'],
            'dynamdb_prefix': os.environ.get('DYNAMDB_PREFIX', ''),
        }
        # DB_ENGINE = 'MONGO_DB'
        # DB_ENGINE = 'DYNAMO_DB'
        self.DB_ENGINE = os.environ['APP_DB_ENGINE']

        # App general configuration

        self.DEBUG = self.get_env('APP_DEBUG', '0') == '1'

        self.APP_NAME = os.environ['APP_NAME']
        self.APP_VERSION = os.environ.get('APP_VERSION', 'N/A')
        self.STAGE = os.environ.get('APP_STAGE')
        self.SECRET_KEY = os.environ.get('SECRET_KEY', str(os.urandom(16)))

        # App specific configuration

        self.APP_SECRET_KEY = os.environ['APP_SECRET_KEY']
        self.APP_SUPERADMIN_EMAIL = \
            os.environ['APP_SUPERADMIN_EMAIL']

        self.APP_HOST_NAME = os.environ['APP_HOST_NAME']
        self.STORAGE_URL_SEED = os.environ['STORAGE_URL_SEED']

        self.GIT_SUBMODULE_LOCAL_PATH = os.environ['GIT_SUBMODULE_LOCAL_PATH']

        self.TEMP_DIR = os.environ.get('TEMP_DIR', '/tmp')

        # ............................

        # Auth parameters

        self.CORS_ORIGIN = self.get_env('APP_CORS_ORIGIN', '*')
        self.HEADER_TOKEN_ENTRY_NAME = self.get_env(
            'HEADER_TOKEN_ENTRY_NAME',
            'Authorization'  # 'x-access-tokens'
        )

        # Languages

        self.DEFAULT_LANG = self.get_env('DEFAULT_LANG', 'en')

    def get_env(self, var_name: str, def_value: Any = None) -> Any:
        """
        Get value of a config variable. If it's in the app_context,
        get from there, if not, get from os.environ.
        """
        result = os.environ.get(var_name, def_value)
        if self.app_context:
            result = self.app_context.get_env_var(
                var_name=var_name,
                def_value=result,
            )
        return result
        # return getattr(self, var_name)

    def debug_vars(self) -> str:
        """
        Show all defined config variables.
        """
        return (
            'Config.debug_vars:\n\n' +
            f'DEBUG = {self.DEBUG}\n' +
            f'SECRET_KEY = {self.SECRET_KEY}\n' +
            f'DB_CONFIG = {self.DB_CONFIG}\n' +
            f'DB_ENGINE = {self.DB_ENGINE}\n' +
            f'APP_SECRET_KEY = {self.APP_SECRET_KEY}\n' +
            f'APP_SUPERADMIN_EMAIL = {self.APP_SUPERADMIN_EMAIL}\n' +
            f'CORS_ORIGIN = {self.CORS_ORIGIN}\n' +
            f'HEADER_TOKEN_ENTRY_NAME = {self.HEADER_TOKEN_ENTRY_NAME}\n' +
            f'STAGE = {self.STAGE}\n' +
            '\n'
        )
