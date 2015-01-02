from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    )
from sqlalchemy import ForeignKey
from sqlalchemy.orm import backref, relationship

from . import db, Base


# RBAC models
class Permission(Base):
    __tablename__ = 'permissions'

    permission = Column(Unicode(100), primary_key=True)
    description = Column(Unicode(250))


class RoutePermission(Base):
    __tablename__ = 'route_permissions'

    route_name = Column(Unicode(200), primary_key=True)
    method = Column(Unicode(30), default=u'ALL', primary_key=True)
    permission = Column(Unicode(100),
                        ForeignKey(Permission.permission),
                        primary_key=True)


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Unicode(100), primary_key=True)
    password = Column(Unicode(40))
    email = Column(Unicode(200))
    full_name = Column(Unicode(200))
    country_code = Column(Unicode(5))  # for example 92
    mobile_network_prefix = Column(Unicode(3))  # for example 3


class UserPermission(Base):
    __tablename__ = 'user_permissions'

    user_id = Column(Unicode(100), ForeignKey(User.user_id), primary_key=True)
    permission = Column(Unicode(100),
                        ForeignKey(Permission.permission),
                        primary_key=True)

    user = relationship(User, backref=backref('permissions'))
