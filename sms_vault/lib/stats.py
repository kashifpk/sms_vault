"Code related to fetching various statistics for SMSes and contacts etc"


from ..models.models import db, SMS, Contact, ContactCellNumber, UserCellNumber
from sqlalchemy import func

import logging
log = logging.getLogger(__name__)

def get_message_count_by_cellnumber(user_id):
    "Return message count for each cell number grouped by incoming and outging"
    
    incoming_counts = db.query(SMS.msg_from, func.count(SMS.id)
                               ).filter_by(owner_id=user_id, incoming=True
                                           ).group_by(SMS.msg_from).all()
    
    outgoing_counts = db.query(SMS.msg_to, func.count(SMS.id)
                               ).filter_by(owner_id=user_id, outgoing=True
                                           ).group_by(SMS.msg_to).all()
    
    log.debug(incoming_counts)
    log.debug(outgoing_counts)
    
    msg_counts = {}
    for cell_number, msg_count in incoming_counts:
        if cell_number not in msg_counts:
            msg_counts[cell_number] = {'incoming': 0, 'outgoing': 0}
        
        msg_counts[cell_number]['incoming'] = msg_count
    
    for cell_number, msg_count in outgoing_counts:
        if cell_number not in msg_counts:
            msg_counts[cell_number] = {'incoming': 0, 'outgoing': 0}
        
        msg_counts[cell_number]['outgoing'] = msg_count
    
    return msg_counts

def get_contact_message_counts(user_id):
    "Returns contacts with count of sent and received messages"
    
    number_to_contact = {}
    contact_counts = {}
    
    contacts = db.query(Contact).filter_by(owner_id=user_id)
    for contact in contacts:
        for cellnum in contact.cell_numbers:
            
            if cellnum.cell_number not in number_to_contact:
                number_to_contact[cellnum.cell_number] = contact.name
                
    log.error(number_to_contact)
    msg_counts = get_message_count_by_cellnumber(user_id)
    
    for cellnum in msg_counts:
        contact_name = number_to_contact.get(cellnum, cellnum)
        if contact_name in contact_counts:
            countact_counts[contact_name]['incoming'] += msg_counts[cellnum]['incoming']
            countact_counts[contact_name]['outgoing'] += msg_counts[cellnum]['outgoing']
        else:
            contact_counts[contact_name] = msg_counts[cellnum]
    
    return contact_counts
