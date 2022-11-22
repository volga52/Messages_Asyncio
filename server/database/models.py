from datetime import datetime

from sqlalchemy import ForeignKey, func, Unicode, UniqueConstraint
from sqlalchemy import String, Column, Integer, DateTime, Boolean, LargeBinary
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Client(Base):
    """Таблица с клиентами"""
    __tablename__ = 'client'

    id = Column(Integer(), primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(LargeBinary(), nullable=False)
    info = Column(String(255), default='')
    online_status = Column(Boolean(), default=False)


class History(Base):
    """Таблица с историей входящих клиентов"""
    __tablename__ = 'history'

    id = Column(Integer(), primary_key=True)
    time = Column(DateTime(), default=datetime.now(), nullable=False)
    # time = Column(DateTime(), server_default=func.now(), nullable=False)
    ip_address = Column(String(255))
    client_id = Column(Integer(), ForeignKey('client.id'))
    client = relationship(
        'Client',
        backref=backref('history', order_by=client_id)
    )


class Contacts(Base):
    """Таблица с контактами"""
    __tablename__ = 'contacts'
    __table_args__ = (
        UniqueConstraint('client_id', 'contact_id', name='unique_contact'),)

    id = Column(Integer(), primary_key=True)
    client_id = Column(Integer(), ForeignKey('client.id'))
    contact_id = Column(Integer(), ForeignKey('client.id'))

    client = relationship('Client', foreign_keys=[client_id])
    contact = relationship('Client', foreign_keys=[contact_id])


class Messages(Base):
    """Таблица сообщений клиента"""
    __tablename__ = 'messages'

    id = Column(Integer(), primary_key=True)
    client_id = Column(Integer(), ForeignKey('client.id'))
    contact_id = Column(Integer(), ForeignKey('client.id'))
    time = Column(DateTime(), default=datetime.now(), nullable=False)
    message = Column(Unicode())

    client = relationship('Client', foreign_keys=[client_id])
    contact = relationship('Client', foreign_keys=[contact_id])
