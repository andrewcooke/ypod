
from unittest import TestCase
from os.path import expanduser

from ypod.conf import Config
from ypod.db.changes import RandomUpdateAlbum
from ypod.db.disk import sync_mp3
from ypod.db.engine import create_session
from ypod.do import shuffle_to_capacity
from ypod.links import Links


class LinksShuffleTest(TestCase):

    def test_shuffle(self):
        config = Config(mount=expanduser('~/project/ypod/ln-music'),
                        mp3=expanduser('~/project/ypod/music'),
                        db='sqlite://', capacity=1e6)
        Session = create_session(config)
        session = Session()
        sync_mp3(config, session)
        target = Links(config)
        shuffle_to_capacity(RandomUpdateAlbum(session), target)
        print 'size: %d' % target._size
        shuffle_to_capacity(RandomUpdateAlbum(session), target)
        print 'size: %d' % target._size

