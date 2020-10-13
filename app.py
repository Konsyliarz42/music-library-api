from flask import Flask, request, abort, jsonify

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
    try:
        form = request.get_json()
        song = Song(    form['band_name'],
                        form['album_name'],
                        int(form['nr']),
                        form['title']   )
    except KeyError:
        abort(400, description="Resource is not complete")
    except ValueError:
        abort(400, description="Nr is not number")
    else:
        func.check_files()
        song_data = song.data
    
    if func.check_song(song_data['band_name'], song_data['album_name'], song_data['nr']):
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
    if request.method == 'PUT':
        form = request.get_json()

        try:
            song = Song(    form['band_name'],
                            form['album_name'],
                            int(form['nr']),
                            form['title']   )
        except KeyError:
            abort(400, description="Resource is not complete")
        else:
            func.check_files()
            song_data = song.data

            if func.check_song(song_data['band_name'], song_data['album_name'], song_data['nr']):
                error = {"error":"Nr is allready in album"}
                return jsonify(form, error), 409

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
    song    = func.check_song(band_name, album_name, nr)
    song_id = song.id
    
    return edit_song_by_id(song_id)

#--------------------------------
@app.route('/songs/<band_name>/<album_name>/<nr>', methods=['GET'])
def get_song(band_name, album_name, nr):
    func.check_files()
    song = func.check_song(band_name, album_name, nr)

    if song:
        return song.in_dict
    else:
        abort(404)

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
def get_album_songs(band_name, album_name):
    func.check_files()
    songs   = func.open_data()
    albums  = [ song.in_dict for song in songs
                if song.album_name.lower() == album_name.replace('-',' ').lower()   ]
        
    return jsonify(albums)

#--------------------------------
@app.route('/bands', methods=['GET'])
def get_band():
    func.check_files()
    bands = [song.band_name for song in func.open_data()]
 
    return jsonify(list(set(bands)))

#--------------------------------
@app.route('/bands/<band_name>', methods=['GET'])
def get_band_albums(band_name):
    func.check_files()
    songs = func.open_data()
    bands = [   song.album_name for song in songs
                if song.band_name.lower() == band_name.replace('-',' ').lower() ]
 
    return jsonify(list(set(bands)))
      
#================================================================
if __name__ == "__main__":
    app.run()