from setuptools import setup

setup(
    name='absents',
    version='0.1',
    packages=['absents'],
    include_package_data=True,
    install_requires=[
        'flask==1.0.2',
        'flask-sqlalchemy==1.2.10',
        'good==0.0.7'
    ],
)
