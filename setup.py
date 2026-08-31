from setuptools import setup, find_packages

setup(
    name='absents',
    version='0.13',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask==1.0.2',
        'flask-sqlalchemy==2.3.2',
        'good==0.0.7.post0',
        'Werkzeug==0.16.0',
        'Jinja2<3.0',
        'MarkupSafe<2.1',
        'itsdangerous<2.1',
        'click<8.1',
        'SQLAlchemy<1.4',
    ],
)
