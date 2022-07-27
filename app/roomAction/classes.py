import redis
import json

class Rooms:
    def __init__(self):
        self.rooms = redis.StrictRedis('localhost', 6379, charset="utf-8", decode_responses=True, db=1)
        self.rooms.flushdb()

    def addRoom(self, *args):
        if len(args) == 3:
            args.append(None)
        self.rooms.hset(args[2], args[0], str(args[1]) + ',' + str(args[3]))

    def getRoomId(self):
        return self.id

    def getRoomType(self):
        return self.type

    def removeRoom(self):
        pass

    def getAll(self, type):
        return self.rooms.hkeys(type)




