import os
import sys
from sqlalchemy import engine_from_config
import transaction

from pyramid.paster import get_appsettings, setup_logging

from ..models import db
from ..lib import contact_processors
import logging
log = logging.getLogger(__name__)


def usage(argv):
    "Print usage help string for the script"

    cmd = os.path.basename(argv[0])
    print(('\nusage: %s <config_uri> input_filenames\n\n'
          '     example: %s development.ini user_id importfile1[ importfile2 ....]' % (cmd, cmd)))
    sys.exit(1)


def get_importer(filename):
    """
    Given a file object, traverses through available contact_processors and returns an
    importer object supporting import from the file. Returns None if no valid importer
    is found for the file
    """
    
    for contact_processor_class in contact_processors:
        file_processor = contact_processor_class(filename)
        
        log.debug(file_processor.valid_format())
        
        if file_processor.valid_format():
            return file_processor
    
    return None


def main(argv=sys.argv):
    if len(argv) < 3:
        usage(argv)

    _, config_uri, user_id, *filenames = argv
    
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    db.configure(bind=engine)
    
    for filename in filenames:
        if not os.path.isfile(filename):
            log.error("{} does not exist".format(filename))
            continue
        
        importer = get_importer(filename)
        if not importer:
            log.warn("No supported importer found for {}".format(filename))
            continue
        
        log.info("Importing {} using {}".format(filename, importer.__class__.__name__))
        ret = importer.get_contacts(owner_id=user_id)
        
        import_summary = """
        Total contacts: {}
        Successfully imported: {}
        Failed: {}
        """.format(ret['successful']+ret['errors'],
                   ret['successful'],
                   ret['errors'])
        
        log.info(import_summary)
        if ret['errors'] > 0:
            for error_msg in ret['error_msgs']:
                log.error(error_msg)

        db.add_all(ret['contacts'])

        db.flush()
        transaction.commit()
