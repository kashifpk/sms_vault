import datetime
from sqlalchemy.ext.declarative import declarative_base
from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

db = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class OrmObject(object):
    """
    Based on:
    http://www.sqlalchemy.org/trac/wiki/UsageRecipes/GenericOrmBaseClass
    """

    def __repr__(self):
        atts = []
        for key in list(self.__table__.c.keys()):
            if key in self.__dict__:
                if not (hasattr(self.__table__.c.get(key).default, 'arg') and
                        getattr(self.__table__.c.get(key).default, 'arg') == getattr(self, key)):
                    atts.append((key, getattr(self, key)))

        return self.__class__.__name__ + '(' + ', '.join(x[0] + '=' + repr(x[1]) for x in atts) + ')'

    def __json__(self, request):
        
        obj_dict = self.to_dict()
        json_dict = {}
        
        for k, v in obj_dict.items():
            if isinstance(v, datetime.datetime):
                json_dict[k] = str(v).split('.')[0]
            else:
                json_dict[k] = v
        
        return json_dict
    
    def to_dict(self):
        d = {}
        for k, v in self.__dict__.items():
            if not k.startswith('_'):
                d[k] = v

        return d

    @classmethod
    def from_dict(cls, data):
        U = cls()
        for k, v in data.items():
            if hasattr(U, k):
                setattr(U, k, v)

        return U

from .models import UserCellNumber, SMS, Contact, ContactCellNumber
from .auth import Permission, User, UserPermission, RoutePermission

# Place additional model names here for ease of importing.
__all__ = ['db', 'Base', 'OrmObject',
           'Permission', 'User', 'UserPermission', 'RoutePermission',
           'UserCellNumber', 'SMS', 'Contact', 'ContactCellNumber']
