
from os import walk
from os.path import join

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import sessionmaker

from ypod.db.schema import Base, Track


def create(config):
    engine = create_engine(config.db)
    Base.metadata.create_all(engine)
    return scoped_session(sessionmaker(autocommit=False, bind=engine))


def sync(config, session):
    gen = Track.next_generation(session.connection())
    track = None
    print config.mp3
    for root, dirs, files in walk(config.mp3):
        for name in files:
            path = join(root, name)
            track = sync_track(path, session, gen, track)


def sync_track(path, session, gen, previous):
    print path
    return previous
