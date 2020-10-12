from flask import Flask, request, abort, jsonify
import os

from classes import Song
import functions as func

#================================================================
app = Flask(__name__)

#--------------------------------
@app.route('/songs', methods=['GET'])
def get_songs():
    func.check_files()
    songs = [song.in_dict for song in func.open_data()]
    return jsonify(songs)

#--------------------------------
@app.route('/songs', methods=['POST'])
def add_song():
    form = request.get_json()
    
    try:
        song = Song(    form['band_name'],
                        form['album_name'],
                        form['nr'],
                        form['title']   )
    except KeyError:
        abort(400, description="Resource is not complete")

    func.check_files()
    songs   = [obj.in_dict for obj in func.open_data()]
    item    = (song.nr, song.album_name, song.band_name)
    items   = [(x['nr'], x['album_name'], x['band_name']) for x in songs]

    if item in items:
        error = {"error":"Nr is allready in album"}
        return jsonify(form, error), 409
                    
    if func.add_to_data(song):
        return form, 201
    else:
        error = {"error":"Resource is allready in database"}
        return jsonify(form, error), 409

#--------------------------------
@app.route('/songs/<song_id>', methods=['PUT', 'DELETE'])
def edit_song_by_id(song_id):
    func.check_files()

    if request.method == 'PUT':
        form = request.get_json()

        try:
            song = Song(    form['band_name'],
                            form['album_name'],
                            int(form['nr']),
                            form['title']   )
        except KeyError:
            abort(400, description="Resource is not complete")

        if not func.update_data(song, song_id):
            abort(404)
        else:
            return form
    else:
        if not func.remove_data(song_id):
            abort(404)
        else:
            return jsonify({}), 204

#--------------------------------
@app.route('/songs/<band_name>/<album_name>/<nr>', methods=['PUT', 'DELETE'])
def edit_song(band_name, album_name, nr):
    song = func.check_song(band_name, album_name, nr)

    if not song or ' ' in band_name or ' ' in album_name or ' ' in nr:
        abort(404)
    else:
        song_id = song.id
    
    return edit_song_by_id(song_id)

#--------------------------------
@app.route('/songs/<band_name>/<album_name>/<nr>', methods=['GET'])
def get_song(band_name, album_name, nr):
    func.check_files()
    song = func.check_song(band_name, album_name, nr)

    if not song or ' ' in band_name or ' ' in album_name or ' ' in nr:
        abort(404)
    else:
        return song.in_dict

#--------------------------------
@app.route('/songs/<song_id>', methods=['GET'])
def get_song_by_id(song_id):
    func.check_files()
    song = [x for x in func.open_data() if x.id == song_id]

    if song:
        return song[0].in_dict
    else:
        abort(404)

#--------------------------------
@app.route('/songs/<band_name>/<album_name>', methods=['GET'])
def get_album(band_name, album_name):
    func.check_files()
    songs = func.open_data()
    albums = [song.in_dict for song in songs if song.album_name == album_name.replace('-',' ')]
 
    if not albums or ' ' in band_name or ' ' in album_name:
        abort(404)
    else:
        return jsonify(albums)
        
#--------------------------------
@app.route('/songs/<band_name>', methods=['GET'])
def get_band(band_name):
    func.check_files()
    songs = func.open_data()
    bands = [song.album_name for song in songs if song.band_name == band_name.replace('-',' ')]
 
    if not bands or ' ' in band_name:
        abort(404)
    else:
        return jsonify(list(set(bands)))
      
#================================================================
if __name__ == "__main__":
    #print(func.open_data()[0].id)
    app.run()