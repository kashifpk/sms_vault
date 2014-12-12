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
from sms_vault.apps import enabled_apps
for enabled_app in enabled_apps:
    if hasattr(enabled_app, 'app_requires'):
        for requirement in enabled_app.app_requires:
            if requirement not in requires:
                requires.append(requirement)

setup(
    name='sms_vault',
    version='0.0',
    description='sms_vault',
    long_description='SMS backup, search and browsing application',
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
    test_suite='sms_vault',
    install_requires=requires,
    entry_points="""\
    [paste.app_factory]
    main = sms_vault:main
    [console_scripts]
    sms_vault_populate = sms_vault.scripts.populate:main
    sms_vault_newapp = sms_vault.scripts.newapp:main
    """,
)
