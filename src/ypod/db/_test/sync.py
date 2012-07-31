
from unittest import TestCase

from ypod.conf import Config
from ypod.db.actions import create, sync


class SyncTest(TestCase):

    def test_music(self):
        config = Config(db='sqlite://')
        Session = create(config)
        session = Session()
        sync(config, session)
