
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


class Artist(Base, Countable):

    __tablename__ = 'artists'
    name = Column(UnicodeText)


class Album(Base, Countable):

    __tablename__ = 'albums'
    name = Column(UnicodeText)
    path = Column(UnicodeText)
    album_artist_id = Column(Integer, ForeignKey(Artist.id), nullable=True)
    album_artist = relationship(Artist, backref='albums')


class Track(Base, Countable):

    __tablename__ = 'tracks'
    artist_id = Column(Integer, ForeignKey(Artist.id))
    artist = relationship(Artist, backref='tracks')
    album_d = Column(Integer, ForeignKey(Album.id))
    album = relationship(Album, backref='tracks')
    name = Column(UnicodeText)
    path = Column(UnicodeText)
    generation = Column(Integer)
    loaded = Column(Boolean, default=False)

    @classmethod
    def next_generation(cls, session):
        try:
            return 1 + session.connection().execute(select([func.max(cls.generation)])).scalar()
        except TypeError:
            return 1


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if not instance:
        instance = model(**kwargs)
        session.add(instance)
    return instance
