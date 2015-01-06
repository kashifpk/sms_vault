"Code related to fetching various statistics for SMSes and contacts etc"


from ..models.models import db, SMS, Contact, ContactCellNumber, UserCellNumber
from sqlalchemy import func, and_, or_

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


def get_contact_cell_numbers(contact):
    "Given a contact name returns it's cell numbers"
    
    cell_numbers = []
    
    if contact:
        for cellnum in contact.cell_numbers:
            cell_numbers.append(cellnum.cell_number)
    else:
        cell_numbers.append(contact_name)
    
    return cell_numbers

def contact_messages(owner_id, contact_name):
    "returns contact messages for given contact"
    
    contact = Contact.by_name(owner_id, contact_name)
    cell_numbers = get_contact_cell_numbers(contact)
    
    #select * from smses where owner_id='kashif' and
    #( (incoming='t' and msg_from in ('+923437158780')) OR (outgoing='t' and msg_to in ('+923437158780')) )
    #order by timestamp desc;
    query = db.query(SMS).filter(
        and_(
            SMS.owner_id==owner_id,
            or_(
                and_(
                    SMS.incoming==True,
                    SMS.msg_from.in_(cell_numbers)
                ),
                and_(
                    SMS.outgoing==True,
                    SMS.msg_to.in_(cell_numbers)
                )
            )
        )
    ).order_by(SMS.timestamp.desc())
    
    return query.all()

def get_date_range_counts(owner_id, range_type, contact_name=None, additional_conditions=None):
    """
    Returns distinct years for which SMS records are available for given owner and optionally contact
    
    :param owner_id: ID of the owner for which the range count is desired
    :param range_type: Type of range count can be any of year, month or day
    :param contact_name: (Optional) Limit the counts for only the given contact
    :param addtional_conditions: (Optional) Dictionary of conditions required if
    range_type is month or day, specfies the year for month and year and month for day
    
    :rtype: A list of tuples with first item being the range and second being the count
    """
    
    # TODO: Convert this function to accept year, month or day as parameter
    # and then return group count for that.
    # Update: Need to re-think this, month needs year and day needs year and month
    
    cellnum_str = ''
    if contact_name:
        contact = Contact.by_name(owner_id, contact_name)
        cell_numbers = get_contact_cell_numbers(contact)
        cellnum_str = "'" + "','".join(cell_numbers) + "'"

    query_str = "SELECT date_part('{}', CAST(timestamp as DATE)) as range_count, count(id) ".format(range_type) + \
                "FROM smses WHERE owner_id='{}'".format(owner_id)
    
    if additional_conditions:
        for k,v in additional_conditions.items():
            query_str += " AND {v}=date_part('{k}', CAST(timestamp as DATE))".format(k=k, v=v)
        
    if cellnum_str:
        query_str += " AND ( (incoming='t' and msg_from in ({cellnums})) OR (outgoing='t' and msg_to in ({cellnums})) )".format(
            cellnums=cellnum_str
        )
    query_str += " group by range_count"
    
    log.info(query_str)
    results = db.execute(query_str)
    
    log.info(results)
    
    range_count = []
    for result in results:
        log.info(result)
        range_count.append((int(result[0]), result[1]))
    
    return range_count
