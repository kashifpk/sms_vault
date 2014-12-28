import os
import sys
from sqlalchemy import engine_from_config
import transaction

from pyramid.paster import get_appsettings, setup_logging

from ..models import db
from ..lib import sms_processors
import logging
log = logging.getLogger(__name__)


def usage(argv):
    "Print usage help string for the script"

    cmd = os.path.basename(argv[0])
    print(('usage: %s <config_uri>\n'
          '(example: "%s development.ini user_id importfile1[ importfile2 ....]")' % (cmd, cmd)))
    sys.exit(1)


def get_importer(file_obj):
    """
    Given a file object, traverses through available sms_processors and returns an
    importer object supporting import from the file. Returns None if no valid importer
    is found for the file
    """
    
    pass


def import_smses():
    ""

    sms_import_map = {}
    
    for fieldname, field in request.POST.items():
        if 'uploaders[]' == fieldname:
            #print(field)
            #print(dir(field))
            #print(field.filename)
            #print(field.length)
            #print(field.type)
            sms_import_map[field.filename] = {'file': field.file}
            
            for sms_processor_class in sms_processors:
                file_processor = sms_processor_class(field.file)
                
                log.debug(field.filename)
                log.debug(file_processor.__doc__)
                log.debug(file_processor.valid_format())
                
                if file_processor.valid_format():
                    sms_import_map[field.filename]['importer'] = file_processor
                    log.debug("Found valid format for {}".format(field.filename))
                    break
            
            
            #file_data = field.file.read()
            #print(file_data.encode('utf-8'))
            #file_dict = {'file': request.static_url(APP_BASE + ':static/blog_images/' + field.filename),
            #             'name': field.filename,
            #             'width': 250, 'height': 250,
            #             'type': field.type, 'size': 1000,
            #             'uploadType': request.POST['uploadType']}
            #ret.append(file_dict)
    
    log.warn(sms_import_map)


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
            
    

    #db.flush()
    #transaction.commit()

