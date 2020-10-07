from flask import Flask, request, render_template, abort, jsonify
import os, csv

class Empty_position:
    def __init__(self):
        self.keys = {   "album_name": "-",
                        "band_name": "-",
                        "nr": "-",
                        "title": "-"  }

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
def update_data(song_dict, song_id):
    for key in song_dict:
        song_dict[key] = song_dict[key].lower()

    songs           = open_data()
    songs[song_id]  = song_dict

    with open('data.csv', 'w', newline='') as csvfile:
        fieldnames  = ['band_name', 'album_name', 'nr', 'title']
        writer      = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for song in songs:
            writer.writerow(song)

#--------------------------------
def add_to_data(song_dict):
    for key in song_dict:
        song_dict[key] = song_dict[key].lower()

    songs = open_data()
    empty = Empty_position().keys

    if song_dict in songs:
        return False
 
    if empty in songs:
        song_id = songs.index(empty)
        update_data(song_dict, song_id)
    else:
        with open('data.csv', 'a', newline='\n') as csvfile:
            fieldnames  = ['band_name', 'album_name', 'nr', 'title']
            writer      = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(song_dict)

    return True

#================================================================
app = Flask(__name__)

#--------------------------------
@app.route('/songs', methods=['GET'])
def get_songs():
    songs = open_data()
    return jsonify(songs)

#--------------------------------
@app.route('/songs', methods=['POST'])
def add_song():
    request_data = request.get_json()

    if add_to_data(request_data):
        return request_data, 201
    else:
        abort(400, description="Resource is already in database")

#--------------------------------
@app.route('/songs/<song_id>', methods=['GET', 'PUT'])
def edit_song(song_id):
    song_id = int(song_id) - 1

    try:
        song = open_data()[song_id]
    except IndexError:
        abort(404, description="Resource not found")
    
    if request.method == 'GET':
        return jsonify(song)
    
    if request.method == 'PUT':
        form = request.get_json()
        change = False

        for key in form.keys():
            if form[key]:
                song[key] = form[key]
                change = True

        if change:
            update_data(song, song_id)

        return jsonify(form)

#--------------------------------
@app.route('/songs/<song_id>', methods=['DELETE'])
def remove_song(song_id):
    song_id = int(song_id) - 1
    empty = Empty_position().keys
    update_data(empty, song_id)

    return empty

#================================================================
if __name__ == "__main__":
    app.run()