"""
Contains classes that process contacts backup files.

Since there can be many different formats used by different backup programs,
we need a class for each supported format.
"""

import codecs
from ..models import db, Contact, ContactCellNumber
import csv
from zipfile import ZipFile
import json
import re
from collections import OrderedDict
from sqlalchemy.orm.exc import FlushError
from .sms_file_processors import ZipProcessor

import logging
log = logging.getLogger(__name__)


UTF8_MARKER = codecs.BOM_UTF8.decode('utf-8')


class GoogleCSVContactsProcessor(object):
    "Support for processing CSV Contacts file exported from Gmail Contacts/Mail"

    def __init__(self, filename):
        self.filename = filename
        self.file_obj = open(filename, mode='rb')

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

    def get_contacts(self, owner_id=None, add_to_db=True):
        """
        Returns all smses in form of Contact objects
        The optional owner_id if given sets the owner_id field of the Contact object

        If add_to_db is True then Contact and ContactCellNumber objects are also added
        to db session and flushed so the calling function/method only needs to commit
        """

        ret = dict(contacts=[], errors=0, successful=0, error_messages=[])
        
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


class S60ZipMsgsContactsProcessor(ZipProcessor):
    """
    Imports contact's name and number from message backup files generated using the
    SMS Export tool on Nokia Symbian series 60 phones.
    """

    def process_contact_string(self, contact_str):
        "Processes contact string for format From: contact_name <+contact_num>"

        contact_line = contact_str.split('\n')[0].split(':')[1]
        log.warn(contact_line)
        contact_name = ''
        
        if '<' in contact_line:
            contact_name, contact_number = re.findall("(.*?)<(.*?)>", contact_line, re.I+re.U)[0]
        else:
            contact_number = contact_line
        
        return (contact_name.strip(), contact_number.strip())
    
    def get_contacts(self, owner_id=None, add_to_db=True):
        """
        Returns all contacts in form of Contact objects
        The optional owner_id if given sets the owner_id field of the Contact object
        
        If add_to_db is True then Contact and ContactCellNumber objects are also added
        to db session and flushed so the calling function/method only needs to commit
        
        >>> from zipfile import ZipFile
        >>> z = ZipFile('iru.zip', 'r')
        >>> z.namelist()
        >>> zi = z.getinfo('sms/20141229-185602.txt')
        >>> f = z.open(zi)
        >>> data = f.read()
        >>> data.decode('utf-16')
        >>> print(data.decode('utf-16'))
        
            From: Saima pindi warid <+923215331687>
            Date: 29/12/2014
            Time: 6:56 pm
            Content: 
            But thank u so much but ap kon hai?
            ][V][Â§T€R
            ][V][¡N|)
        """
        
        ret = dict(total_contacts=0, total_numbers=0,
                   errors=0, successful=0, error_messages=[])
        
        contacts_dict = {}
        
        zip_file = ZipFile(self.filename, 'r')
        for subfilename in zip_file.namelist():
            log.info("Processing {} from the zip file".format(subfilename))
            file_info = zip_file.getinfo(subfilename)
            subfile = zip_file.open(file_info)
            file_data = subfile.read().decode('utf-16')
            log.debug(file_data)
            contact_name, contact_number = self.process_contact_string(file_data)
            log.info((contact_name, contact_number))
            if contact_name:
                
                if contact_name not in contacts_dict:
                    contacts_dict[contact_name] = [contact_number, ]
                    ret['total_contacts'] += 1
                    ret['total_numbers'] += 1
                
                elif contact_number not in contacts_dict[contact_name]:
                    contacts_dict[contact_name].append(contact_number)
                    ret['total_numbers'] += 1
        
        for contact_name, contact_numbers in contacts_dict.items():
            try:
                new_contact = Contact(owner_id=owner_id, name=contact_name)
                if add_to_db:
                    db.add(new_contact)
                    db.flush()
                
            except Exception as exp:
                ret['errors'] += 1
                ret['error_messages'].append(str(exp))  
            
            for contact_number in contact_numbers:
                
                try:
                    contact_number = ContactCellNumber(contact_id=new_contact.id,cell_number=contact_number)
                    if add_to_db:
                        db.add(contact_number)
                        db.flush()
                except Exception as exp:
                    ret['errors'] += 1
                    ret['error_messages'].append(str(exp))  
        
        return ret

