import sys


class ConfigurationError(Exception):
    def __init__(self, msg):
        message = (
            "ImportError, is import mechanism loaded?"
            " Try calling setup_search_paths somewhere %s %s") % (
            sys.meta_path,
            msg
        ) 
        super(ConfigurationError, self).__init__(message)
