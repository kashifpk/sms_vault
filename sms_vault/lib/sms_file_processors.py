"""
Contains classes that process SMS files ready for import.

Since there can be many different formats used by different backup programs,
we need a class for each supported format.
"""

import codecs
from datetime import datetime
from ..models import SMS, UserCellNumber

import logging
log = logging.getLogger(__name__)


class TSVProcessor(object):
    "Tab separated values sms backup file importer"

    def __init__(self, file_obj):
        self.file_obj = file_obj

    def valid_format(self):
        """
        Returns True if the file can be imported using this class,
        Otherwise returns False
        """

        self.file_obj.seek(0)
        data = self.file_obj.read(500)
        self.file_obj.seek(0)
        log.debug(data)

        if (codecs.BOM_UTF8.decode('utf-8') == data[0] and
                '+' == data[1] and '\t\t' in data):
            return True
        else:
            return False

    def parse_msg_string(self, msg, owner_cell_number):
        "Given a msg string, parses it and creates an SMS object"
        
        # '+923435782789\t13/11/2014 18:58:30\tAbu ki med laani hy sath shop se.\t1'
        # 2 at the end is sent, 1 in incoming
        
        number, timestamp, msg_text, msg_type = msg.strip('\t')
        
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
        data = self.file_obj.read()

        msgs = data.split('\t\t')
        
        onwer_cell_number = UserCellNumber.get_default_number(owner_id)

        if codecs.BOM_UTF8.decode('utf-8') == msgs[0]:
            msgs[0] = msgs[0][1:]

        for msg in msgs:
            try:
                #sms_obj.owner_id = ''
                # set owner ID and msg_from number for sent smses
                msg_obj = self.parse_msg_string(msg, owner_cell_number)
                ret['successful'] += 1
            except Exception as exp:
                ret['errors'] += 1
                ret['error_messages'].append(str(exp))
            
            
        

