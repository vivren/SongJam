# from collections import deque
# import json
#
# class Song:
#     def __init__(self, title, id):
#         self.title = title
#         self.id = id
#         self.time = 0
#
#     def getTitle(self):
#         return self.title
#
#     def getID(self):
#         return self.id
#
#     def getTime(self):
#         return self.time
#
#     def updateTime(self, time):
#         self.time = time;
#
#     def __str__(self):
#         return self.getTitle() + "," + self.getID()
#
# class Playlist:
#     def __init__(self):
#         self.playlist = deque()
#
#     def isEmpty(self):
#         return len(self.playlist) == 0
#
#     def addSong(self, song):
#         self.playlist.append(song)
#
#     def getCurrentSong(self):
#         if len(self.playlist) == 0:
#             return None
#         return self.playlist[0]
#
#     def getNextSong(self):
#         return self.playlist.popleft()
#
#     def getLastSong(self):
#         if len(self.playlist) == 0:
#             return None
#         return self.playlist[-1]
#
#     def getPlaylist(self):
#         returnVal = []
#         for song in self.playlist:
#             returnVal.append(str(song))
#         return returnVal

import redis
import json

class Song:
    def __init__(self, title, id):
        self.title = title
        self.id = id
        self.time = 0

    def getTitle(self):
        return self.title

    def getID(self):
        return self.id

    def getTime(self):
        return self.time

    def updateTime(self, time):
        self.time = time

    def __str__(self):
        return self.getTitle() + "," + self.getID() + "," + str(self.getTime())


class Playlist:
    def __init__(self):
        self.playlist = redis.StrictRedis('localhost', 6379, charset="utf-8", decode_responses=True)
        self.playlist.flushdb()

    def isEmpty(self, room):
        return self.playlist.llen(room) == 0

    def addSong(self, room, song):
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
