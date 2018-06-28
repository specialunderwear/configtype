from setuptools import setup, find_packages


__version__ = "0.0.5"


setup(
    # package name in pypi
    name='configtype',
    # extract version from module.
    version=__version__,
    description="Configtype bridges json configuration to python.",
    long_description="Configure your app with json, but import from python",
    classifiers=[],
    keywords='',
    author='Lars van de Kerkhof',
    author_email='lars@permanentmarkers.nl',
    url='https://github.com/specialunderwear/configtype',
    license='GPLv3',
    # include all packages in the egg, except the test package.
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests', 'test']),
    # for avoiding conflict have one namespace for all related eggs.
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
)
