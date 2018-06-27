import sys
import unittest
import os.path
from configtype.jsonconfig import configfile, setup_search_paths

setup_search_paths()

@configfile
class MyPersonalConfigClass(object):
    # defaults
    overridden = False

settings = MyPersonalConfigClass()


class JsonTest(unittest.TestCase):
    def setUp(self):
        self.settings = MyPersonalConfigClass()

    def test_config_is_loaded(self):
        self.assertEqual(settings.value, "somevalue")
        self.assertDictEqual(settings.structure, {
            'flapdrol': False,
            'width': [1, 3, 7]
        })

    def test_override(self):
        self.assertEqual(settings.overridden, True)

    def test_instance_values_are_isolated(self):
        self.assertEqual(self.settings.value, "somevalue")
        self.assertDictEqual(self.settings.structure, {
            'flapdrol': False,
            'width': [1, 3, 7]
        })
        self.assertEqual(self.settings.overridden, True)
        self.settings.value = "newvalue"
        self.assertEqual(self.settings.value, "newvalue")
        self.assertEqual(settings.value, "somevalue")

    def test_just_use_the_class(self):
        self.assertEqual(MyPersonalConfigClass.value, "somevalue")
        self.assertDictEqual(MyPersonalConfigClass.structure, {
            'flapdrol': False,
            'width': [1, 3, 7]
        })
