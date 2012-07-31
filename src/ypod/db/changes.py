
from random import shuffle
from sqlalchemy.sql.expression import and_
from ypod.db.schema import Album


class RandomUpdateAlbum(object):
    '''
    This contains two collaborating generators.  One is a source of
    albums to add; the other a source of albums to delete.  By loading
    the former, and deleting the latter only when space is low, a new
    set of albums is loaded efficiently (sampled fairly over all albums
    available).
    '''

    def __init__(self, session):
        self._session = session
        self._disk_gen = Album.current_disk_generation(self._session)
        self._ipod_gen = Album.current_ipod_generation(self._session)
        print "current generations: %d, %d" % (self._disk_gen, self._ipod_gen)

    def to_add(self):
        album_ids = list(map(lambda x: x[0], self._session.query(Album.id).filter(Album.disk_generation == self._disk_gen).all()))
        shuffle(album_ids)
        for album_id in album_ids:
            album = self._session.query(Album).filter(Album.id == album_id).first()
            album.ipod_generation = self._ipod_gen + 1
            album.loaded = True
            self._session.commit()
            yield album

    def to_remove(self):
        # first, remove albums deleted from disk
        while True:
            album = self._session.query(Album).filter(
                and_(Album.disk_generation != self._disk_gen,
                    Album.ipod_generation != self._ipod_gen+1,
                    Album.loaded == True)).order_by(
                Album.disk_generation.asc()).first()
            if not album: break
            album.loaded = False
            self._session.commit()
            yield album
        # next, remove any albums not loaded in this load
        while True:
            album = self._session.query(Album).filter(
                and_(Album.ipod_generation != self._ipod_gen+1,
                    Album.loaded == True)).order_by(
                Album.disk_generation.asc()).first()
            if not album: break
            album.loaded = False
            self._session.commit()
            yield album


