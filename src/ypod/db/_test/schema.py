
from unittest import TestCase

from ypod.conf import Config
from ypod.db.actions import create
from ypod.db.schema import Track, Artist, Album


class SchemaTest(TestCase):

    def test_schema(self):
        config = Config(db='sqlite://')
        Session = create(config)
        session = Session()
        assert Track.next_generation(session.connection()) == 1

    def test_next_gen(self):
        config = Config(db='sqlite://')
        Session = create(config)
        session = Session()
        artist = Artist(name='bob')
        session.add(artist)
        album = Album(name='bob sings')
        session.add(album)
        track = Track(artist=artist, album=album, name='a sad song',
            generation=3, path='/music/bob/songs')
        session.add(track)
        session.commit()
        assert Track.next_generation(session.connection()) == 4
        track = session.query(Track).filter(Track.name == 'a sad song').one()
        assert track.name == 'a sad song'
        assert track.artist.name == 'bob'
        artist = session.query(Artist).filter(Artist.name == 'bob').one()
        assert artist.name == 'bob'
        assert track.artist == artist
