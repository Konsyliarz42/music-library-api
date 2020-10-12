import uuid

#================================================================
class Song():
    def __init__(self, band_name='-', album_name='-', nr=0, title='-'):
        self.band_name = band_name
        self.album_name = album_name
        self.nr = int(nr)
        self.title = title
        self.id = str(uuid.uuid4())


    def __repr__(self):
        return f"{self.band_name.capitalize()} - {self.title.capitalize()}"

    @property
    def data(self):
        song = {    'band_name': self.band_name.lower(),
                    'album_name': self.album_name.lower(),
                    'nr': self.nr,
                    'title': self.title.lower() }
        return song

    @property
    def in_dict(self):
        song = {    'band_name': self.band_name,
                    'album_name': self.album_name,
                    'nr': self.nr,
                    'title': self.title,
                    'id': self.id   }
        return song
