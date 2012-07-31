
from unittest import TestCase

from ypod.conf import Config
from ypod.db.changes import RandomUpdateAlbum
from ypod.db.disk import sync_mp3
from ypod.db.engine import create


class SimulateLoadingTest(TestCase):

    def test_load(self):
        config = Config(db='sqlite://')
        Session = create(config)
        session = Session()
        sync_mp3(config, session)
        capacity, contains = 100, 0
        capacity, contains = self.load_once(session, capacity, contains)
        assert contains > capacity
        capacity, contains = self.load_once(session, capacity, contains)
        assert contains > capacity

    def load_once(self, session, capacity, contains):
        update = RandomUpdateAlbum(session)
        to_add = update.to_add()
        to_remove = update.to_remove()
        while True:
            while contains < capacity:
                try:
                    album = next(to_add)
                    contains += len(album.tracks)
                    print 'added %d tracks for %s' % (len(album.tracks), album.name)
                except StopIteration:
                    pass
            try:
                album = next(to_remove)
                contains -= len(album.tracks)
                print 'removed %d tracks for %s' % (len(album.tracks), album.name)
            except StopIteration:
                return capacity, contains
