import os
import sys
import json
from sqlalchemy import engine_from_config
import platform

from pyramid.paster import get_appsettings, setup_logging

from ..models import db, Contact

if platform.python_version() > '3':
    from urllib.parse import urlparse
else:
    from urlparse import urlparse


def usage(argv):
    "Print usage help string for the script"

    cmd = os.path.basename(argv[0])
    print(('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd)))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)

    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    db.configure(bind=engine)

    contacts = db.query(Contact)

    website_types = ['Website {} - Type'.format(i) for i in range(1, 7)]
    website_values = ['Website {} - Value'.format(i) for i in range(1, 7)]

    here_parent = os.path.dirname(os.path.dirname(__file__))
    photos_path = os.path.join(here_parent, 'static/contact_photos')

    for contact in contacts:

        #print(contact.name, end='\t')
        #for cell in contact.cell_numbers:
        #    print(cell.cell_number, end=' ')
        #print('')

        extra_info = json.loads(contact.extra_info)

        for web_type, web_value in zip(website_types, website_values):
            #if (web_type in extra_info and 'Profile' == extra_info[web_type]):
            if web_value in extra_info and extra_info[web_value]:
                print(contact.name)
                print(extra_info[web_value])
                # Fetch the Google+ profile photo for the user
                profile_urls = extra_info[web_value].split(':::')
                for profile_url in profile_urls:
                    url = urlparse(profile_url.strip())
                    if 'www.google.com' == url.domain:
                        profile_id = url.path.split('/')[-1]
                
