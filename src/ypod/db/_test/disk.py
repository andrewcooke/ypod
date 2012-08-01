from sqlalchemy.sql.expression import func
from unittest import TestCase

from ypod.conf import Config
from ypod.db.engine import create_session
from ypod.db.disk import sync_mp3
from ypod.db.schema import Track, Album, Artist


class SyncTest(TestCase):

    def test_sync_mp3(self):
        config = Config(db='sqlite://')
        Session = create_session(config)
        session = Session()
        sync_mp3(config, session)
        assert Track.count(session) == 141, Track.count(session)
        assert Artist.count(session) == 27, Artist.count(session)
        assert Album.count(session) == 12, Album.count(session)
