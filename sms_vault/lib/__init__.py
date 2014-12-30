"Libarary/utility code"

from .sms_file_processors import TSVProcessor, ZipProcessor
from .contact_file_processors import GoogleCSVContactsProcessor, S60ZipMsgsContactsProcessor

contact_processors = (GoogleCSVContactsProcessor, S60ZipMsgsContactsProcessor)
sms_processors = (TSVProcessor, ZipProcessor)
