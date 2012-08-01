

def shuffle_to_capacity(update, target):
    to_add = update.to_add()
    to_remove = update.to_remove()
    while True:
        while target.has_space():
            try:
                album = next(to_add)
                for track in album.tracks:
                    target.load_track(track)
            except StopIteration:
                pass
        try:
            album = next(to_remove)
            for track in album.tracks:
                target.unload_track(track)
        except StopIteration:
            return

