from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    DateTime,
    Boolean
    )

from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import ForeignKey
from sqlalchemy.orm import backref, relationship

from . import db, Base, OrmObject
from .auth import User


class UserCellNumber(Base, OrmObject):
    "Cell numbers that belong to the user"

    __tablename__ = 'user_cell_numbers'

    user_id = Column(Unicode(100), ForeignKey(User.user_id), primary_key=True)
    cell_number = Column(Unicode(50), primary_key=True)
    default = Column(Boolean)

    user = relationship(User, backref=backref('cell_numbers'))
    
    @classmethod
    def get_default_number(cls, user_id):
        "Return user's default cell number"
        
        ret = None
        rec = db.query(cls).filter_by(user_id=user_id, default=True).one()
        
        if rec:
            ret = rec.cell_number
        
        return ret


class SMS(Base, OrmObject):
    "SMS record storage"

    __tablename__ = 'smses'

    id = Column(Integer, primary_key=True)
    owner_id = Column(Unicode(100), ForeignKey(User.user_id))
    timestamp = Column(DateTime)
    msg_from = Column(Unicode(50), nullable=False)
    msg_to = Column(Unicode(50))
    incoming = Column(Boolean, default=False)
    outgoing = Column(Boolean, default=False)
    message = Column(Unicode(2000))

    owner = relationship(User, backref=backref('smses'))


class Contact(Base, OrmObject):
    "SMS Contact"

    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True)
    owner_id = Column(Unicode(100), ForeignKey(User.user_id))
    name = Column(Unicode(200))
    extra_info = Column(JSON)

    owner = relationship(User, backref=backref('contacts'))
    
    @classmethod
    def by_name(cls, owner_id, name):
        return db.query(cls).filter_by(owner_id=owner_id, name=name).one()


class ContactCellNumber(Base, OrmObject):
    "Cell numbers that belong to a contact"

    __tablename__ = 'contact_cell_numbers'

    contact_id = Column(Integer, ForeignKey(Contact.id), primary_key=True)
    cell_number = Column(Unicode(50), primary_key=True)

    contact = relationship(Contact, backref=backref('cell_numbers'))
