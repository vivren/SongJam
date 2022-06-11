from collections import deque
import json

class Song:
    def __init__(self, title, id):
        self.title = title
        self.id = id

    def getTitle(self):
        return self.title

    def getID(self):
        return self.id

    def __str__(self):
        return self.getTitle() + "," + self.getID()

class Playlist:
    def __init__(self):
        self.playlist = deque()

    def isEmpty(self):
        return len(self.playlist) == 0

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
            returnVal.append(str(song))
        return returnVal

    # def convertJson(self):
    #     jsonString = '{"songs": ['
    #     for song in self.playlist:
    #         jsonString += "{"
    #         jsonString += f'"name": "{song.getTitle()}", "id": "{song.getID()}"'
    #         if song == self.getLastSong():
    #             jsonString += "}"
    #         else:
    #             jsonString += "},"
    #     jsonString += "]}"
    #     return jsonString




