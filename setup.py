from setuptools import setup
from absents.version import __version__

setup(
    name='absents',
    version=__version__,
    packages=['absents'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)
