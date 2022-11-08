from datetime import datetime
from sqlalchemy import ForeignKey, func
from sqlalchemy import String, Column, Integer, DateTime, Boolean, Unicode,\
    LargeBinary
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
    "Таблица с историей входящих клиентов"
    __tablename__ = 'history'

    id = Column(Integer(), primary_key=True)
    time = Column(DateTime(), server_default=func.now(), nullable=False)
    ip_address = Column(String(255))
    client_id = Column(Integer(), ForeignKey('client.id'))
    client = relationship(
        'Client',
        backref=backref('history', order_by=client_id)
    )
