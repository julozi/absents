from setuptools import setup, find_packages

setup(
    name='absents',
    version='0.9',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask==2.3.2',
        'flask-sqlalchemy==2.3.2',
        'good==0.0.7.post0',
        'Werkzeug==0.16.0'
    ],
)
