
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import sessionmaker

from ypod.db.schema import Base


def create(config):
    engine = create_engine(config.db)
    Base.metadata.create_all(engine)
    return scoped_session(sessionmaker(autocommit=False, bind=engine))

