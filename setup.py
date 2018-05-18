from setuptools import setup, find_packages


__version__ = "0.0.1"


setup(
    # package name in pypi
    name='configtype',
    # extract version from module.
    version=__version__,
    description="Load a config file as a type, to enable parse time configuration",
    long_description="",
    classifiers=[],
    keywords='',
    author='',
    author_email='',
    url='',
    license='',
    # include all packages in the egg, except the test package.
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    # for avoiding conflict have one namespace for all apc related eggs.
    namespace_packages=[],
    # include non python files
    include_package_data=True,
    zip_safe=False,
    # specify dependencies
    install_requires=[
        'setuptools',
        'six',
    ],
    # mark test target to require extras.
    extras_require = {
        'test':  ["nose"]
    },
    # generate scripts
    # entry_points={
    #     'console_scripts':[
    #         'script_name = name.module:main',
    #     ]
    # },
)
