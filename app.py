from flask import Flask, request
import os, csv

#--------------------------------
def open_data():
    songs = list()

    if os.path.isfile('data.csv'):
        with open('data.csv', 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for song in reader:
                songs.append(song)
    else:
        with open('data.csv', 'w', newline='') as csvfile:
            fieldnames  = ['band_name', 'album_name', 'nr', 'title']
            writer      = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
    return songs

#--------------------------------
def add_to_data(band_name, album_name, nr, title):
    song_dict = {   'band_name': band_name.lower(),
                    'album_name': album_name.lower(),
                    'nr': str(nr),
                    'title': title.lower()  }

    if song_dict in open_data():
        return False

    with open('data.csv', 'a', newline='\n') as csvfile:
        fieldnames  = ['band_name', 'album_name', 'nr', 'title']
        writer      = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writerow(song_dict)
        return True

#--------------------------------
def update_data(song_dict, song_id):
    songs           = open_data()
    songs[song_id]  = song_dict

    with open('data.scv', 'w', newline='') as csvfile:
        fieldnames  = ['band_name', 'album_name', 'nr', 'title']
        writer      = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for song in songs:
            writer.writerow(song)


#================================================================
app = Flask(__name__)

@app.route('/songs', methods=['GET'])
def get_songs():
    songs = open_data()
    return songs, 200

@app.route('/songs', methods=['POST'])
def add_song():
    band_name   = request.form.get("band_name")
    album_name  = request.form.get("album_name")
    nr          = request.form.get("nr")
    title       = request.form.get("title")

    if add_to_data(band_name, album_name, nr, title):
        return 201
    else:
        return 400

@app.route('/songs/<song_id>', methods=['GET', 'PUT'])
def edit_song(song_id):
    song_id = int(song_id)

    try:
        song = open_data()[song_id]
    except IndexError:
        return 404

    if request.method == 'GET':
        return song, 200
    
    if request.method == 'PUT':
        form = {    'band_name': request.form.get("band_name"), 
                    'album_name': request.form.get("album_name"),
                    'nr': request.form.get("nr"),
                    'title': request.form.get("title")   }
        change = False

        for key in form.keys():
            if form[key]:
                song[key] = form[key]
                change = True

        if change:
            update_data(song, song_id)

        return 200

print(open_data())