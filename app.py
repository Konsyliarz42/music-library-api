from flask import Flask, request, abort, jsonify
import os

from classes import Song
import functions as func

#================================================================
app = Flask(__name__)

#--------------------------------
@app.route('/songs', methods=['GET'])
def get_songs():
    songs = [song.in_dict for song in func.open_data()]
    return jsonify(songs)

#--------------------------------
@app.route('/songs', methods=['POST'])
def add_song():
    form = request.get_json()
    song = Song(    form['band_name'],
                    form['album_name'],
                    form['nr'],
                    form['title']   )
                    
    if func.add_to_data(song):
        return form, 201
    else:
        abort(400, description="Resource is already in database")

#--------------------------------
@app.route('/songs/<song_id>', methods=['PUT', 'DELETE'])
def edit_song(song_id):
    if request.method == 'PUT':
        form = request.get_json()
        song = Song(    form['band_name'],
                        form['album_name'],
                        form['nr'],
                        form['title']   )

        if not func.update_data(song, song_id):
            abort(404, description="Song ID is incorrect")
        else:
            return form
    else:
        if not func.remove_data(song_id):
            abort(404, description="Song ID is incorrect")
        else:
            return jsonify({}), 204

#================================================================
if __name__ == "__main__":
    print(func.open_data()[1].id)

    if not os.path.isfile('data/songs.pickle'):
        if not os.path.isdir('data'):
            os.mkdir('data')

        open('data/songs.pickle', 'wb').close()
        print("'songs.pickle' is now crated!")

    app.run()