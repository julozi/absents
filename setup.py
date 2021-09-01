from setuptools import setup, find_packages

setup(
    name='absents',
    version='0.8',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask==1.0.2',
        'flask-sqlalchemy==2.3.2',
        'good==0.0.7.post0',
        'Werkzeug==0.16.0'
    ],
)
