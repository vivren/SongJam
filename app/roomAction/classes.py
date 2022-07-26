import redis

class Rooms:
    def __init__(self):
        self.rooms = redis.StrictRedis('localhost', 6379, charset="utf-8", decode_responses=True)
        self.playlist.flushdb()

    def searchRooms(self):
        # Return rooms matching the search criteria


class Room:
    def __init__(self, *args):
        self.name = name
        self.type = type
        self.password = None

    def validatePassword(self):
        pass

    def getRoomType(self):

    def addRoom(self):
        pass

    def removeRoom(self):
        pass

