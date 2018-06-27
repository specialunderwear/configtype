import sys
import imp
import json
import importlib
import copy
import logging
from os.path import join, exists, realpath

from six import add_metaclass

from .errors import ConfigurationError

logger = logging.getLogger()


def setup_search_paths(*paths):
    """
    This function MUST be called or no config file can be found
    """
    if paths:
        json_importer = JsonFinder(paths)
    else:
        json_importer = JsonFinder()

    sys.meta_path.append(json_importer)


class JsonFinder(object):
    def __init__(self, search_paths=('.')):
        self.search_paths = search_paths

    def find_module(self, fullname, path=None):
        try:
            module, extension = fullname.rsplit('.', 1)
        except ValueError:
            return None

        if extension != 'json':
            return None

        package_parts = module.split('.')

        for search_path in self.search_paths:
            while package_parts:
                filename = "%s.json" % join(
                    realpath(search_path),
                    *package_parts
                )
                logger.debug("Looking for json config at %s", filename)

                if exists(filename):
                    return JsonLoader(path, filename)

                package_parts.pop()

        return None


class JsonLoader(object):
    def __init__(self, path_entry, filename):
        self.filename = filename
        self.path_entry = path_entry

    def load_module(self, fullname):
        if fullname in sys.modules:
            mod = sys.modules[fullname]
        else:
            mod = sys.modules.setdefault(fullname, imp.new_module(fullname))

        logger.info("config module %s loaded from %s" % (
            fullname, self.filename
        ))
        # Set a few properties required by PEP 302
        mod.__file__ = self.filename
        mod.__name__ = fullname
        mod.__loader__ = self
        mod.__package__, _ = fullname.rsplit('.', 1)

        with open(self.filename) as jsonfile:
            json_data = json.load(jsonfile)
            mod.__dict__.update(json_data)

        return mod


class JsonConfigType(type):
    def __new__(cls, name, bases, attrs):
        try:
            class_module = attrs['__module__']
            parent_module, _ = class_module.rsplit('.', 1)
            config_module_name = "%s.json" % parent_module
            config_module = importlib.import_module(config_module_name)

            # update attrs with values from config module
            for k in dir(config_module):
                if not k.startswith('__'):
                    value = getattr(config_module, k)
                    attrs[k] = copy.deepcopy(value)

        except ImportError as e:
            if attrs.get('ignore_missing_config', False):
                logger.info(
                    "Config file not found, but ignoring because class"
                    " is configured with `ignore_missing_config`"
                )
            else:
                raise ConfigurationError(e)

        return type.__new__(cls, name, bases, attrs)


configfile = add_metaclass(JsonConfigType)
