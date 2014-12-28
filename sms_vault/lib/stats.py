"Code related to fetching various statistics for SMSes and contacts etc"


from ..models.models import db, SMS, Contact, ContactCellNumber, UserCellNumber
from sqlalchemy import func

import logging
log = logging.getLogger(__name__)


def get_contact_message_counts(user_id):
    "Returns contacts with count of sent and received messages"
    
    incoming_counts = db.query(SMS.msg_from, func.count(SMS.id)
                               ).filter_by(owner_id=user_id, incoming=True
                                           ).group_by(SMS.msg_from).all()
    
    outgoing_counts = db.query(SMS.msg_to, func.count(SMS.id)
                               ).filter_by(owner_id=user_id, outgoing=True
                                           ).group_by(SMS.msg_to).all()

    log.warn(incoming_counts)
    log.warn(outgoing_counts)
