import redis

class Playlist:
    def __init__(self):
        self.playlist = redis.StrictRedis('localhost', 6379, charset="utf-8", decode_responses=True, db=0)
        self.playlist.flushdb()

    def isEmpty(self, room):
        return self.playlist.llen(room) == 0

    def addSong(self, room, title, id):
        song = title + ',' + id
        self.playlist.rpush(room, song)

    def getCurrentSong(self, room):
        if self.isEmpty(room):
            return None
        return self.playlist.lindex(room, 0)

    def getNextSong(self, room):
        if self.isEmpty(room):
            return None
        return self.playlist.lpop(room)

    def getPlaylist(self, room):
        return self.playlist.lrange(room, 0, -1)

    def getCurrentSongs(self, rooms):
        songs = [self.getCurrentSong(room).split(",")[0] for room in rooms]
        return ['No Current Song Playing' if song is None else song for song in songs]
