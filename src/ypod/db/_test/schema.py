
from unittest import TestCase

from ypod.conf import Config
from ypod.db.engine import create
from ypod.db.schema import Track, Artist, Album


class SchemaTest(TestCase):

    def test_schema(self):
        config = Config(db='sqlite://')
        Session = create(config)
        session = Session()
        assert Track.current_disk_generation(session) == 0, Track.current_disk_generation(session)

    def test_next_disk_generation(self):
        config = Config(db='sqlite://')
        Session = create(config)
        session = Session()
        artist = Artist(name='bob')
        session.add(artist)
        album = Album(name='bob sings')
        session.add(album)
        track = Track(artist=artist, album=album, name='a sad song',
            disk_generation=3, path='/music/bob/songs')
        session.add(track)
        session.commit()
        assert Track.current_disk_generation(session) == 3
        track = session.query(Track).filter(Track.name == 'a sad song').one()
        assert track.name == 'a sad song'
        assert track.artist.name == 'bob'
        artist = session.query(Artist).filter(Artist.name == 'bob').one()
        assert artist.name == 'bob'
        assert track.artist == artist
