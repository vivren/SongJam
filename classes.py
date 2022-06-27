import redis
import json

class Playlist:
    def __init__(self):
        self.playlist = redis.StrictRedis('localhost', 6379, charset="utf-8", decode_responses=True)
        self.playlist.flushdb()

    def isEmpty(self, room):
        return self.playlist.llen(room) == 0

    def addSong(self, room, title, id):
        song = title + ',' + id + ',0'
        self.playlist.rpush(room, song)

    def addSongWithTime(self, room, title, id, time):
        song = title + ',' + id + time
        self.playlist.rpush(room, song)

    def getCurrentSong(self, room):
        if self.isEmpty(room):
            return None
        return self.playlist.lindex(room, 0)

    def updateCurrentSongTime(self, room, time):
        if self.isEmpty(room):
            return None
        new = self.playlist.lindex(room, 0).split(",")[0] + ',' + self.playlist.lindex(room, 0).split(",")[1] + ',' + str(time)
        self.playlist.lset(room, 0, new)

    def getNextSong(self, room):
        if self.isEmpty(room):
            return None
        return self.playlist.lpop(room)

    def getPlaylist(self, room):
        return self.playlist.lrange(room, 0, -1)
