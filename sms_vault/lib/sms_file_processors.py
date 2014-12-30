"""
Contains classes that process SMS files ready for import.

Since there can be many different formats used by different backup programs,
we need a class for each supported format.
"""

import codecs
from datetime import datetime
from ..models import SMS, UserCellNumber
from zipfile import ZipFile

import logging
log = logging.getLogger(__name__)


class TSVProcessor(object):
    "Tab separated values sms backup file importer"

    def __init__(self, filename):
        
        self.file_obj = open(filename, mode='rb')

    def valid_format(self):
        """
        Returns True if the file can be imported using this class,
        Otherwise returns False
        """

        self.file_obj.seek(0)
        data = self.file_obj.read(500)
        
        self.file_obj.seek(0)
        log.debug(data)

        if data.startswith(codecs.BOM_UTF8) and '+' == chr(data[3]) and b'\t\t' in data:
            return True
        else:
            return False

    def parse_msg_string(self, msg, owner_cell_number):
        "Given a msg string, parses it and creates an SMS object"
        
        # '+923435782789\t13/11/2014 18:58:30\tAbu ki med laani hy sath shop se.\t1'
        # 2 at the end is sent, 1 in incoming
        
        log.debug(msg)
        number, timestamp, msg_text, msg_type = msg.split('\t')
        
        sms_obj = SMS(message=msg_text)
        sms_obj.timestamp = datetime.strptime(timestamp, "%d/%m/%Y %H:%M:%S")
        
        if "1" == msg_type:
            sms_obj.msg_from = number
            sms_obj.msg_to = owner_cell_number
            sms_obj.incoming = True
        elif "2" == msg_type:
            sms_obj.msg_from = owner_cell_number
            sms_obj.msg_to = number
            sms_obj.outgoing = True
        
        return sms_obj
    
    def get_smses(self, owner_id=None):
        """
        Returns all smses in form of SMS objects
        The optional owner_id if given sets the owner_id field of the SMS object
        """
        
        ret = dict(smses=[], errors=0, successful=0, error_messages=[])

        self.file_obj.seek(0)
        data = self.file_obj.read().decode('utf-8')

        msgs = data.split('\t\t')
        
        owner_cell_number = UserCellNumber.get_default_number(owner_id)

        if codecs.BOM_UTF8.decode('utf-8') == msgs[0][0]:
            msgs[0] = msgs[0][1:]

        for msg in msgs:
            try:
                #sms_obj.owner_id = ''
                # set owner ID and msg_from number for sent smses
                log.debug(msg)
                if not msg.strip():
                    continue
                
                log.debug(bytes(msg.encode('utf-8')))
                msg_obj = self.parse_msg_string(msg, owner_cell_number)
                msg_obj.owner_id = owner_id
                
                ret['smses'].append(msg_obj)
                
                ret['successful'] += 1
                
            except Exception as exp:
                ret['errors'] += 1
                ret['error_messages'].append(str(exp))
                
        return ret


class ZipProcessor(object):
    "Zip file containing one text file per message"
    """
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

    def __init__(self, filename):
        self.filename = filename
        

    def valid_format(self):
        """
        Returns True if the file can be imported using this class,
        Otherwise returns False
        """

        try:
            zip_file = ZipFile(self.filename)
            zipinfo = zip_file.getinfo(zip_file.namelist()[0])

            if self.filename.lower().endswith('.zip') and zip_file.open(zipinfo).read().decode('utf-16').startswith('From:'):
                return True
            else:
                return False
        except Exception as exp:
            log.error(str(exp))
            return False
        

    def parse_msg_string(self, msg, owner_cell_number):
        "Given a msg string, parses it and creates an SMS object"
        
        # '+923435782789\t13/11/2014 18:58:30\tAbu ki med laani hy sath shop se.\t1'
        # 2 at the end is sent, 1 in incoming
        
        log.debug(msg)
        number, timestamp, msg_text, msg_type = msg.split('\t')
        
        sms_obj = SMS(message=msg_text)
        sms_obj.timestamp = datetime.strptime(timestamp, "%d/%m/%Y %H:%M:%S")
        
        if "1" == msg_type:
            sms_obj.msg_from = number
            sms_obj.msg_to = owner_cell_number
            sms_obj.incoming = True
        elif "2" == msg_type:
            sms_obj.msg_from = owner_cell_number
            sms_obj.msg_to = number
            sms_obj.outgoing = True
        
        return sms_obj
    
    def get_smses(self, owner_id=None):
        """
        Returns all smses in form of SMS objects
        The optional owner_id if given sets the owner_id field of the SMS object
        """
        
        ret = dict(smses=[], errors=0, successful=0, error_messages=[])

        self.file_obj.seek(0)
        data = self.file_obj.read().decode('utf-8')

        msgs = data.split('\t\t')
        
        owner_cell_number = UserCellNumber.get_default_number(owner_id)

        if codecs.BOM_UTF8.decode('utf-8') == msgs[0][0]:
            msgs[0] = msgs[0][1:]

        for msg in msgs:
            try:
                #sms_obj.owner_id = ''
                # set owner ID and msg_from number for sent smses
                log.debug(msg)
                if not msg.strip():
                    continue
                
                log.debug(bytes(msg.encode('utf-8')))
                msg_obj = self.parse_msg_string(msg, owner_cell_number)
                msg_obj.owner_id = owner_id
                
                ret['smses'].append(msg_obj)
                
                ret['successful'] += 1
                
            except Exception as exp:
                ret['errors'] += 1
                ret['error_messages'].append(str(exp))
                
        return ret
