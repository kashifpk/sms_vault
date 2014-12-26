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

from . import db, Base
from .auth import User


class UserCellNumber(Base):
    "Cell numbers that belong to the user"

    __tablename__ = 'user_cell_numbers'

    user_id = Column(Unicode(100), ForeignKey(User.user_id), primary_key=True)
    cell_number = Column(Unicode(50), primary_key=True)

    user = relationship(User, backref=backref('cell_numbers'))


class SMS(Base):
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


class Contact(Base):
    "SMS Contact"

    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True)
    owner_id = Column(Unicode(100), ForeignKey(User.user_id))
    name = Column(Unicode(200))
    extra_info = Column(JSON)

    owner = relationship(User, backref=backref('contacts'))


class ContactCellNumber(Base):
    "Cell numbers that belong to a contact"

    __tablename__ = 'contact_cell_numbers'

    contact_id = Column(Integer, ForeignKey(Contact.id), primary_key=True)
    cell_number = Column(Unicode(50), primary_key=True)

    contact = relationship(Contact, backref=backref('cell_numbers'))
