class Song:
    def __init__(self, name, artist=None, features=None, album=None):
        self.name = name
        self.artist = artist
        self.features = features
        self.album = album

    def __str__(self):
        return str(self.name) + " by " + str(self.artist) + " Ft. " + str(self.features)


class Album:
    def __init__(self, name, songs=[]):
        self.name = name
        self.songs = songs

    def __str__(self):
        return str(self.name) + ": " + str(self.songs)
