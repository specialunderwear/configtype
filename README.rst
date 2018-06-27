Configtype configuration loaded
===============================

Configtype let's you define application configuration in both python and
configuration languages like json, ini and yaml.

Haha that's a lie, only json is implemented.

Overview
--------

Configtype will construct a python type that has all the top level values
in the config file defined as attributes.

Which amounts to::

    {
        "sitename": "Bank of amurika",
        "production": true,
        "structure": {
            "width": [1,3,7],
            "flapdrol": false
        }
    }

will become something in python that looks like this::


    class Config(object):
        sitename = "Great value"
        production = True
        structure = {"width": [1, 3, 7], "flapdrol": False}

That is nice to have! Because now you can load your configuration where you
need it using ``import``. You can create instances, where you can change some
configuration details without messing with the global settings.

Package structure
-----------------

So how does it work? somewhere in your project, you need to create a module
that hold your configuration class definition, with default values. This can
not be a top level module, but MUST be contained in a package, do not put it
in the global namespace!::

    config.py <--- toplevel don;t put it here
    myapp/__init__.py
    myapp/config.py  <-- you can put it here.

The file should look like this::

    from configtype.jsonconfig import configfile, setup_search_paths

    setup_search_paths()
    
    @configfile
    class MyPersonalConfigClass(object):
        # defaults
        sitename = "Default sitename"
        production = False

    settings = MyPersonalConfigClass()

So just create a type with some default values as attributes and slap a
decorator on top. These defaults will be used if the values are not defined in
your json config. That way you can be sure the values are defined and avoid
adding checks in your code.

Search path an json filename
----------------------------

In the above example, note the use of ``setup_search_paths`` if you never call
this function, you will get errors, because the json file will not be found.
If you call ``setup_search_paths`` without arguments, configtype will look
for the file from the current folder. It will start in the folder where you
have put the configtype class definition and use the module names for the
config file filename.

What???
=======

Let say you project looks like this::

    myapp/__init__.py
    myapp/settings/__init__.py
    myapp/settings/config.py <-- type declaration goes here

configtype will look for the following filenames::

  myapp/settings.json
  myapp.json

It will do so in all folders you registered for the search paths::


    setup_search_paths() <--- current directory is search path
    setup_search_paths('/etc/pythonapps', 'blub') <-- hmm

The second declaration will look for the following files::

    /etc/pythonapps/myapp/settings.json
    /etc/pythonapps/myapp.json
    ./blub/myapp/settings.json
    ./blub/myapp.json

The reason the naming is weird is because python's import mechanism is used
to do the searching and that means is the files are dropped in a folder, this
folder should also be the name of a python package.

Try it! after you called ``setup_search_paths``, you can import the json
even without the configtype, suppose we stuck the json in
/etc/pythonapps/myapp/settings.json::

    import myapp.settings.json

And also, if your json look like this::


    {'SITE_ID': 100}


you can immport values from the json directly::

    from myapp.settings.json import SITE_ID
