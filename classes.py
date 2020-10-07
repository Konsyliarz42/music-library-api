#================================================================
class Song():
    def __init__(self, band_name='-', album_name='-', nr=0, title='-'):
        self.band_name = band_name.lower()
        self.album_name = album_name.lower()
        self.nr = str(int(nr))
        self.title = title.lower()
        self.id = id(self)

    def __repr__(self):
        return f"{self.band_name.capitalize()} - {self.title.capitalize()}"

    @property
    def in_dict(self):
        song = {    'band_name': self.band_name,
                    'album_name': self.album_name,
                    'nr': self.nr,
                    'title': self.title }
        return song

#================================================================
class Album():
    def __init__(self, band_name=None, album_name=None, year=0):
        self.band_name = band_name
        self.album_name = album_name
        self.year = str(int(year))
        self.songs = list()
        self.id = id(self)

    def __repr__(self):
        return f"({self.year}) {self.album_name}"