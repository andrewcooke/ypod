
from gpod.ipod import Database


class GPod(object):

    def __init__(self, config):
        self.db = Database(config.mount)
        print 'created %s' % db

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print 'flushing %s' % db
        self.db.copy_delayed_files()
        print 'closing %s' % db
        self.db.close()

    def load_track(self, track):
        print 'loading: %s from %s' % (track, track.path)
        self.db.import_file(track.path)

    def delete_all_tracks(self):
        while self.db:
            print 'deleting: %s' % db[0]
            self.db.remove(db[0], ipod=True)
