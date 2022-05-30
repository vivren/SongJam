from collections import deque

class Song:
    def __init__(self, title, id):
        self.title = title
        self.id = id
        self.link = f"https://www.youtube.com/embed/{id}?autoplay=1"

    def getTitle(self):
        return self.title

    def getLink(self):
        return self.link

    def getID(self):
        return self.id

class Playlist:
    def __init__(self):
        self.playlist = deque()

    def addSong(self, song):
        self.playlist.append(song)

    def getCurrentSong(self):
        if len(self.playlist) == 0:
            return None
        return self.playlist[0]

    def getNextSong(self):
        return self.playlist.popleft()

    def getLastSong(self):
        if len(self.playlist) == 0:
            return None
        return self.playlist[-1]

    def getPlaylist(self):
        returnVal = []
        for song in self.playlist:
            returnVal.append(song.getTitle())
        return returnVal

