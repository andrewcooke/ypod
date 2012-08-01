
from os.path import exists, isdir, join, getsize, realpath, dirname
from os import mkdir, symlink, unlink, walk


class Links(object):

    def __init__(self, config):
        self._root = config.mount
        self._mp3 = config.mp3
        self._capacity = config.capacity
        self._mkdir(self._root)
        self._size = sum(self._file_sizes())

    def _file_sizes(self):
        for root, dirs, files in walk(self._root):
            for name in files:
                yield self._file_size(join(root, name))

    @staticmethod
    def _file_size(path):
        size = getsize(realpath(path))
        print '%s: %d' % (path, size)
        return size

    def has_space(self):
        print '%d < %d' % (self._size, self._capacity)
        return self._size < self._capacity

    def _mkdir(self, path):
        if not exists(path): mkdir(path)
        assert isdir(path), path

    def _move(self, path):
        assert path.startswith(self._mp3)
        moved = join(self._root, path[len(self._mp3)+1:])
        print '%s -> %s' % (path, moved)
        return moved

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def load_track(self, track):
        print 'loading: %s from %s' % (track, track.path)
        self._mkdir(self._move(dirname(track.album.path)))
        self._mkdir(self._move(track.album.path))
        print '%s -> %s' % (self._move(track.path), track.path)
        symlink(track.path, self._move(track.path))
        self._size += self._file_size(track.path)

    def unload_track(self, track):
        print 'unloading %s' % self._move(track.path)
        self._size -= self._file_size(track.path)
        unlink(self._move(track.path))

    def unload_all_tracks(self):
        if self._size > 0:
            raise NotImplementedError('by hand!')
