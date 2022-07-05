import datetime

from ckan.model import core, meta
from ckan.model.domain_object import DomainObject
from sqlalchemy import Column, Table, types


ark_table = Table(
    'ark',
    meta.metadata,
    Column('identifier', types.UnicodeText, primary_key=True),
    Column('package_id', types.UnicodeText, nullable=False, unique=True),
    Column('who', types.UnicodeText),
    Column('what', types.UnicodeText),
    Column('when', types.UnicodeText),
    Column('created', types.DateTime, default=datetime.datetime.utcnow),
    Column('last_modified', types.DateTime),
    Column('state', types.UnicodeText, default=core.State.ACTIVE),
)


class ARK(DomainObject):
    '''ARK Object'''
    pass


meta.mapper(ARK, ark_table)
