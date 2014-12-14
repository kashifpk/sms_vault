"""
Contains classes that process contacts backup files.

Since there can be many different formats used by different backup programs,
we need a class for each supported format.
"""

import codecs
from ..models import Contact, ContactCellNumber
import csv
from collections import OrderedDict

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

    def get_contacts(self, owner_id=None):
        """
        Returns all smses in form of Contact objects
        The optional owner_id if given sets the owner_id field of the Contact object
        """

        reader = csv.DictReader(self.file_obj)
        fieldnames = reader.fieldnames

        contacts = []

        for rec in reader:
            contact_dict = OrderedDict()
            for fname in fieldnames:
                val = rec.get(fname, '')

                if val is not None and len(val.strip()) > 0:

                    if UTF8_MARKER == fname[0]:
                        contact_dict[fname[1:]] = rec[fname]
                    else:
                        contact_dict[fname] = rec[fname]

            contacts.append(contact_dict)

        return contacts

