from mutagen.id3 import ID3



class Manager:
    def __init__(self, handler):
        self.handler = handler
        self.song = None

    def get_song_title(self, song):
        self.song = song
        try:
            self.audio = ID3(self.song)
            return self.audio["TIT2"].text[0]
        except:
            return self.song
