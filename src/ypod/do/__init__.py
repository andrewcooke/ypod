

def shuffle_to_capacity(update, target):
    to_add = update.to_add()
    to_remove = update.to_remove()
    tracks_to_load = True
    while tracks_to_load:
        while target.has_space() and tracks_to_load:
            try:
                album = next(to_add)
                for track in album.tracks:
                    target.load_track(track)
            except StopIteration:
                tracks_to_load = False
        try:
            album = next(to_remove)
            for track in album.tracks:
                target.unload_track(track)
        except StopIteration:
            return
