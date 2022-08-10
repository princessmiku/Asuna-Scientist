"""

    Setup your database

"""
from . import *
import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


s2Engine = sq.create_engine(SQLALCHEMY_URI, echo=SQLALCHEMY_ECHO)
s2Metadata = sq.MetaData(bind=s2Engine)
s2Base = declarative_base(metadata=s2Metadata)
s2Base.metadata.engine = s2Engine
s2Base.metadata.create_all(bind=s2Engine)
s2Session = sessionmaker(bind=s2Engine, autoflush=False)
s2Session = s2Session()


userEngine = sq.create_engine(SQLALCHEMY_URI_USER, echo=SQLALCHEMY_ECHO)
userMetadata = sq.MetaData(bind=userEngine)
userBase = declarative_base(metadata=userMetadata)
userBase.metadata.engine = userEngine
userBase.metadata.create_all(bind=userEngine)
userSession = sessionmaker(bind=userEngine)
userSession = userSession()


# https://stackoverflow.com/questions/2546207/does-sqlalchemy-have-an-equivalent-of-djangos-get-or-create
def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


