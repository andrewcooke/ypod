
from unittest import TestCase

from ypod.conf import Config
from ypod.db.disk import sync_mp3
from ypod.db.engine import create_session
from ypod.db.schema import Track
from ypod.gpod import GPod


class TestTransfer(TestCase):

    def setUp(self):
        config = Config(db='sqlite://')
        with GPod(config) as db:
            db.delete_all_tracks()

    def test_track(self):
        config = Config(db='sqlite://')
        Session = create_session(config)
        session = Session()
        sync_mp3(config, session)
        track = session.query(Track).order_by(Track.id).first()
        assert track
        with GPod(config) as db:
            db.load_track(track)

