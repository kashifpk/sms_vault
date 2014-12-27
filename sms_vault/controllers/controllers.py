from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from ..models import (
    db,
    )

from ..forms import ContactForm


@view_config(route_name='home', renderer='home.mako')
def homepage(request):
    return {'project': 'sms_vault'}

@view_config(route_name='import_smses', renderer='import_smses.mako')
def imprt_smses(request):
    "Allow importing smses"

    print(request.POST)
    for fieldname, field in request.POST.items():
        if 'uploaders[]' == fieldname:
            print(field)
            print(dir(field))
            print(field.filename)
            print(field.length)
            print(field.type)
            file_data = field.file.read()
            print(file_data.encode('utf-8'))
            #file_dict = {'file': request.static_url(APP_BASE + ':static/blog_images/' + field.filename),
            #             'name': field.filename,
            #             'width': 250, 'height': 250,
            #             'type': field.type, 'size': 1000,
            #             'uploadType': request.POST['uploadType']}
            #ret.append(file_dict)
    return {}

@view_config(route_name='contact', renderer="contact.mako")
def contact_form(request):

    f = ContactForm(request.POST)   # empty form initializes if not a POST request

    if 'POST' == request.method and 'form.submitted' in request.params:
        if f.validate():
            #TODO: Do email sending here.

            request.session.flash("Your message has been sent!")
            return HTTPFound(location=request.route_url('home'))

    return {'contact_form': f}
