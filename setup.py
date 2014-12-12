import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

requires = [
    'PyCK',
    'pyramid',
    'SQLAlchemy',
    'psycopg2',
    'transaction',
    'pyramid_mako',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'zope.sqlalchemy',
    'webtest',
    'waitress',
    'wtforms',
    'wtdojo'
]

if sys.version_info[:3] < (2, 5, 0):
    requires.append('pysqlite')

# Requires from subapps
from sms_volt.apps import enabled_apps
for enabled_app in enabled_apps:
    if hasattr(enabled_app, 'app_requires'):
        for requirement in enabled_app.app_requires:
            if requirement not in requires:
                requires.append(requirement)

setup(
    name='sms_volt',
    version='0.0',
    description='sms_volt',
    long_description='SMS backup and search application',
    classifiers=[
        "Programming Language :: Python",
        "Framework :: PyCK",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='',
    author_email='',
    url='',
    keywords='web PyCK framework pylons pyramid',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='sms_volt',
    install_requires=requires,
    entry_points="""\
    [paste.app_factory]
    main = sms_volt:main
    [console_scripts]
    sms_volt_populate = sms_volt.scripts.populate:main
    sms_volt_newapp = sms_volt.scripts.newapp:main
    """,
)
