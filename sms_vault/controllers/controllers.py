from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
import logging

from ..models import db

from ..forms import ContactForm
from ..lib import sms_processors
from ..lib.stats import (get_contact_message_counts,
                         contact_messages,
                         get_distinct_years)

from ..lib.sort import alphanumeric_sort
from collections import OrderedDict

log = logging.getLogger(__name__)

@view_config(route_name='home', renderer='home.mako')
def homepage(request):
    return {}


@view_config(route_name='msg_counts', renderer='json')
def msg_counts(request):
    msg_counts = get_contact_message_counts(request.session['logged_in_user'])
    sorted_contacts = alphanumeric_sort(msg_counts.keys())
    
    ret = []
    for contact in sorted_contacts:
        dict_item = msg_counts[contact]
        dict_item['contact_name'] = contact
        ret.append(dict_item)
    
    return ret


@view_config(route_name='contact_msgs', renderer='json')
def contact_messages_view(request):
    
    msgs = contact_messages(request.session['logged_in_user'],
                            request.matchdict['contact'])
    
    log.warn(msgs)
    return msgs

@view_config(route_name='msg_years', renderer='json')
def msg_years(request):
    
    msgs = get_distinct_years(request.session['logged_in_user'],
                            request.matchdict['contact'])
    
    log.warn(msgs)
    return msgs


@view_config(route_name='import_smses', renderer='import_smses.mako')
def imprt_smses(request):
    "Allow importing smses"

    print(request.POST)
    #request.session['logged_in_user']
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
    
    return {'import_map': sms_import_map}

@view_config(route_name='contact', renderer="contact.mako")
def contact_form(request):

    f = ContactForm(request.POST)   # empty form initializes if not a POST request

    if 'POST' == request.method and 'form.submitted' in request.params:
        if f.validate():
            #TODO: Do email sending here.

            request.session.flash("Your message has been sent!")
            return HTTPFound(location=request.route_url('home'))

    return {'contact_form': f}
