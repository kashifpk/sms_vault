"""
Contains classes that process SMS files ready for import.

Since there can be many different formats used by different backup programs,
we need a class for each supported format.
"""

import codecs
from ..models import SMS


class TSVProcessor(object):
    "Tab separated values sms backup file import"

    def __init__(self, file_obj):
        self.file_obj = file_obj

    def valid_format(self):
        """
        Returns True if the file can be imported using this class,
        Otherwise returns False
        """

        self.file_obj.seek(0)
        data = self.file_obj.read(2200)
        self.file_obj.seek(0)

        if (codecs.BOM_UTF8.decode('utf-8') == data[0] and
                '+' == data[1] and '\t\t' in data):
            return True
        else:
            return False

    def get_smses(self, owner_id=None):
        """
        Returns all smses in form of SMS objects
        The optional owner_id if given sets the owner_id field of the SMS object
        """
        pass
