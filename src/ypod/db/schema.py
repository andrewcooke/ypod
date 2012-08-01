
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.sql.expression import func, select
from sqlalchemy.types import Integer, Boolean, UnicodeText

Base = declarative_base()


class Countable(object):

    id = Column(Integer, primary_key=True)

    @classmethod
    def count(cls, session):
        return session.connection().execute(select([func.count(cls.id)])).scalar()


class Generationed(object):

    @classmethod
    def _current_generation(cls, session, column):
        gen = session.connection().execute(select([func.max(column)])).scalar()
        if gen is None: return 0
        return gen


class Artist(Base, Countable):

    __tablename__ = 'artists'
    name = Column(UnicodeText)


class Album(Base, Countable, Generationed):

    __tablename__ = 'albums'
    name = Column(UnicodeText)
    path = Column(UnicodeText)
    album_artist_id = Column(Integer, ForeignKey(Artist.id), nullable=True)
    album_artist = relationship(Artist, backref='albums')
    ipod_generation = Column(Integer)
    disk_generation = Column(Integer)
    loaded = Column(Boolean, default=False)

    @classmethod
    def current_ipod_generation(cls, session):
        return cls._current_generation(session, cls.ipod_generation)

    @classmethod
    def current_disk_generation(cls, session):
        return cls._current_generation(session, cls.disk_generation)


class Track(Base, Countable, Generationed):

    __tablename__ = 'tracks'
    artist_id = Column(Integer, ForeignKey(Artist.id))
    artist = relationship(Artist, backref='tracks')
    album_id = Column(Integer, ForeignKey(Album.id))
    album = relationship(Album, backref='tracks')
    name = Column(UnicodeText)
    path = Column(UnicodeText)
    disk_generation = Column(Integer)

    @classmethod
    def current_disk_generation(cls, session):
        return cls._current_generation(session, cls.disk_generation)

    def __str__(self):
        return '%s: %s (%s)' % (self.artist.name, self.name, self.album.name)


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if not instance:
        instance = model(**kwargs)
        session.add(instance)
    return instance
