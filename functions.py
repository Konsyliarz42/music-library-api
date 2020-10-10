import os, pickle

from classes import Song

#--------------------------------
def check_files():
    if not os.path.isfile('data/songs.pickle'):
        if not os.path.isdir('data'):
            os.mkdir('data')

        open('data/songs.pickle', 'wb').close()
        print("'songs.pickle' is now crated!")

#--------------------------------
def open_data():
    patch = 'data/songs.pickle'
    songs = list()

    with open(patch, 'rb') as pfile:
        while True:
            try:
                songs.append(pickle.load(pfile))
            except EOFError:
                break
            
    return songs

#--------------------------------
def add_to_data(song):
    patch   = 'data/songs.pickle'
    songs   = [obj.in_dict for obj in open_data()]

    if song.in_dict in songs:
        return False

    with open(patch, 'ab') as pfile:
        pickle.dump(song, pfile)

    return True

#--------------------------------
def update_data(song, song_id):
    patch = 'data/songs.pickle'
    songs = open_data()

    try:
        song_id = song_id
    except ValueError:
        return False

    for obj in songs:
        if obj.id == song_id:
            song.id = song_id
            songs[songs.index(obj)] = song

            with open(patch, 'wb') as pfile:
                for song in songs:
                    pickle.dump(song, pfile)

            return True

    return False

#--------------------------------
def remove_data(song_id):
    patch = 'data/songs.pickle'
    songs = open_data()

    try:
        song_id = song_id
    except ValueError:
        return False

    for obj in songs:
        if obj.id == song_id:
            index = songs.index(obj)
            songs.pop(index)

            with open(patch, 'wb') as pfile:
                for song in songs:
                    pickle.dump(song, pfile)

            return True

    return False

#--------------------------------
def check_song(band, album, nr):
    songs   = open_data()
    band    = band.replace('-', ' ')
    album   = album.replace('-', ' ')
    nr      = str(int(nr)).zfill(2)

    for obj in songs:
        song = obj.in_dict

        if song['band_name'] == band and song['album_name'] == album and song["nr"] == nr:
            return obj

    return False
