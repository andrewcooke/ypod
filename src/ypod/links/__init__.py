
from os.path import exists, isdir, join
from os import mkdir, symlink, unlink


class Links(object):

    def __init__(self, config):
        self._root = config.mount
        self._mp3 = config.mp3
        self._mkdir(self._root)

    def _mkdir(self, path):
        if not exists(path): mkdir(path)
        assert isdir(path), path

    def _move(self, path):
        assert path.startswith(self._mp3)
        return join(self._root, path[len(self._mp3):])

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def load_track(self, track):
        print 'loading: %s from %s' % (track, track.path)
        self._mkdir(self._move(track.artist.path))
        self._mkdir(self._move(track.album.path))
        symlink(track.path, self._move(track.path))

    def unload_track(self, track):
        unlink(self._move(track.path))

    def unload_all_tracks(self):
        raise NotImplementedError('by hand!')
