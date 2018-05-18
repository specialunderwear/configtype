import json
from six import add_metaclass

class JsonConfigType(type):
    def __new__(cls, name, bases, attrs):
        path = attrs.pop('path', 'config.json')
        with open(path) as config_file:
            loaded_attrs = json.load(config_file)
            attrs.update(loaded_attrs)

        return type.__new__(cls, name, bases, attrs)


configfile = add_metaclass(JsonConfigType)
