
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.sql.expression import func, select
from sqlalchemy.types import Text, Integer, Boolean

Base = declarative_base()


class Artist(Base):

    __tablename__ = 'artists'
    id = Column(Integer, primary_key=True)
    name = Column(Text)


class Album(Base):

    __tablename__ = 'albums'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    album_artist_id = Column(Integer, ForeignKey(Artist.id), nullable=True)
    album_artist = relationship(Artist, backref='albums')


class Track(Base):

    __tablename__ = 'tracks'
    id = Column(Integer, primary_key=True)
    artist_id = Column(Integer, ForeignKey(Artist.id))
    artist = relationship(Artist, backref='tracks')
    album_d = Column(Integer, ForeignKey(Album.id))
    album = relationship(Album, backref='tracks')
    name = Column(Text)
    path = Column(Text)
    generation = Column(Integer)
    loaded = Column(Boolean, default=False)

    @classmethod
    def next_generation(cls, conn):
        try:
            return 1 + conn.execute(select([func.max(cls.generation)])).scalar()
        except TypeError:
            return 1

