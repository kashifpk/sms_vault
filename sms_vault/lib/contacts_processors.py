"""
Contains classes that process contacts backup files.

Since there can be many different formats used by different backup programs,
we need a class for each supported format.
"""

import codecs
from ..models import db, Contact, ContactCellNumber
import csv
import json
from collections import OrderedDict
from sqlalchemy.orm.exc import FlushError

UTF8_MARKER = codecs.BOM_UTF8.decode('utf-8')


class GoogleCSVContactsProcessor(object):
    "Support for processing CSV Contacts file exported from Gmail Contacts/Mail"

    def __init__(self, file_obj):
        self.file_obj = file_obj

    def valid_format(self):
        """
        Returns True if the file can be imported using this class,
        Otherwise returns False
        """

        self.file_obj.seek(0)
        valid = (UTF8_MARKER + 'Name,Given Name,'
                 == self.file_obj.read(17))
        self.file_obj.seek(0)

        return valid


    def get_contacts(self, owner_id=None, add_to_db=False):
        """
        Returns all smses in form of Contact objects
        The optional owner_id if given sets the owner_id field of the Contact object

        If add_to_db is True then Contact and ContactCellNumber objects are also added
        to db session and flushed so the calling function/method only needs to commit
        """

        reader = csv.DictReader(self.file_obj)
        fieldnames = reader.fieldnames

        contacts = []

        #Phone 1 - Type,Phone 1 - Value,Phone 2 - Type,Phone 2 - Value,
        #Phone 3 - Type,Phone 3 - Value,Phone 4 - Type,Phone 4 - Value,
        #Phone 5 - Type,Phone 5 - Value,Phone 6 - Type,Phone 6 - Value

        phone_types = ['Phone {} - Type'.format(i) for i in range(1, 7)]
        phone_values = ['Phone {} - Value'.format(i) for i in range(1, 7)]

        for rec in reader:
            contact_dict = OrderedDict()
            for fname in fieldnames:
                val = rec.get(fname, '')

                if val is not None and len(val.strip()) > 0:

                    if UTF8_MARKER == fname[0]:
                        contact_dict[fname[1:]] = rec[fname]
                    else:
                        contact_dict[fname] = rec[fname]

            #print(contact_dict)
            #contacts.append(contact_dict)
            if 'Name' in contact_dict and contact_dict['Name']:
                contact = Contact(name=contact_dict['Name'],
                                  owner_id=owner_id,
                                  extra_info=json.dumps(contact_dict))

                contact_added = False

                contact_numbers = []
                for phone_type, phone_value in zip(phone_types, phone_values):
                    if (phone_type in contact_dict and
                        'Mobile' == contact_dict[phone_type]):

                        cell_numbers = contact_dict[phone_value].split(':::')
                        for cell_number in cell_numbers:
                            cell_number = cell_number.strip(u'\u202a\u202c ')
                            if not cell_number:
                                continue

                            prec = ContactCellNumber(cell_number=cell_number)

                            if add_to_db:
                                if not contact_added:
                                    contact_added = True
                                    db.add(contact)
                                    db.flush()

                                prec.contact_id = contact.id
                                try:
                                    db.add(prec)
                                    db.flush()
                                except FlushError as exp:
                                    print(exp)

                            contact_numbers.append(prec)

                contacts.append({'contact': contact,
                                 'cell_numbers': contact_numbers})

        return contacts

