from sys import stderr
from os import walk
from os.path import join

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

from ypod.db.schema import Base, Track, Artist, get_or_create, Album


def sync_mp3(config, session):
    gen = Track.next_generation(session)
    for root, dirs, files in walk(config.mp3):
        if files:
            sync_album(session, gen, root, files)
    session.commit()


def sync_album(session, gen, root, files):
    album, artists = None, {}
    for name in files:
        album = sync_track(session, gen, root, name, album, artists)
    if len(artists) == 1:
        album.album_artist = artists[artists.keys()[0]]


def sync_track(session, gen, root, name, album, artists):
    path = join(root, name)
    try:
        id3 = MP3(path, ID3=EasyID3)
        name = id3['album'][0]
        if album:
            assert album.name == name, (album.name, name)
        else:
            album = get_or_create(session, Album, name=name, path=root)
        name = id3['artist'][0]
        if name not in artists:
            artists[name] = get_or_create(session, Artist, name=name)
        artist = artists[name]
        track = get_or_create(session, Track, artist=artist, album=album, name=id3['title'][0])
        track.generation = gen
        return album
    except Exception as e:
#        print '%s: %s' % (path, e.message)
        print >> stderr, path
        return album
