import os
import sys
import json
from sqlalchemy import engine_from_config
from sqlalchemy.orm import joinedload
import platform
import requests
from slugify import slugify
import transaction

from pyramid.paster import get_appsettings, setup_logging

from ..models import db, Contact

if platform.python_version() > '3':
    from urllib.parse import urlparse
else:
    from urlparse import urlparse

here_parent = os.path.dirname(os.path.dirname(__file__))
project_base = os.path.dirname(here_parent)
photos_path = os.path.join(here_parent, 'static/contact_photos')

api_file_path = os.path.join(project_base, 'GOOGLE_API_KEY.txt')
#print(api_file_path)
GOOGLE_API_KEY = open(api_file_path,'r').read().strip()
#print(GOOGLE_API_KEY)

def usage(argv):
    "Print usage help string for the script"

    cmd = os.path.basename(argv[0])
    print(('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd)))
    sys.exit(1)


def fetch_profile_photo(contact, url):
    "Given a google profile url, fetches the profile photo"

    profile_id = url.path.split('/')[-1]
    req_url = ("https://www.googleapis.com/plus/v1/people/" +
               "{profile_id}?fields=image&key={api_key}".format(
                profile_id=profile_id, api_key=GOOGLE_API_KEY))

    #print(req_url)
    response = requests.get(req_url)
    json_data = response.json()
    #print(json_data)
    if 'image' not in json_data:
        return False, False
    #{
    # "image": {
    #  "url": "https://lh3.googleusercontent.com/-zDpeEc6sXLo/AAAAAAAAAAI/AAAAAAAAAEE/bah-UQxR1l0/photo.jpg?sz=50",
    #  "isDefault": false
    # }
    #}
    img_url = json_data['image']['url']

    # remove any query string params
    img_url = urlparse(img_url)
    img_ext = img_url.path.split('.')[-1]
    img_url = (img_url.scheme + '://' +
               img_url.netloc + img_url.path)

    img_data = requests.get(img_url).content

    profile_photo_name = (slugify(contact.name) + '-' +
                          profile_id + '.' + img_ext)

    profile_photo_path = os.path.join(photos_path, profile_photo_name)

    print("Saving image to: {}".format(profile_photo_path))
    open(profile_photo_path, 'wb').write(img_data)

    return (profile_photo_name, json_data['image']['isDefault'])


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)

    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    db.configure(bind=engine)

    contacts = db.query(Contact)

    website_values = ['Website {} - Value'.format(i) for i in range(1, 7)]

    for contact in contacts:

        #print(contact.name, end='\t')
        #for cell in contact.cell_numbers:
        #    print(cell.cell_number, end=' ')
        #print('')

        db.add(contact)

        extra_info = json.loads(contact.extra_info)

        profile_photos = []

        for web_value in website_values:
            #if (web_type in extra_info and 'Profile' == extra_info[web_type]):
            if web_value in extra_info and extra_info[web_value]:
                print(contact.name)
                print(extra_info[web_value])
                # Fetch the Google+ profile photo for the user
                profile_urls = extra_info[web_value].split(':::')

                for profile_url in profile_urls:
                    url = urlparse(profile_url.strip())
                    if 'www.google.com' == url.netloc:
                        photoname, isdefault = fetch_profile_photo(contact, url)

                        if not photoname:
                            continue

                        if isdefault:
                            profile_photos.insert(0, photoname)
                        else:
                            profile_photos.append(photoname)

        if profile_photos:
            print(profile_photos)
            print(contact.extra_info)
            extra_info['profile_photos'] = profile_photos
            contact.extra_info = json.dumps(extra_info)

            db.flush()
            transaction.commit()
            print("===============")
