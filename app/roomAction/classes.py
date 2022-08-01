import redis
import json

class Rooms:
    def __init__(self):
        self.rooms = redis.StrictRedis('localhost', 6379, charset="utf-8", decode_responses=True, db=1)
        self.rooms.flushdb()

    def addRoom(self, *args):
        if len(args) == 3:
            args.append(None)
        self.rooms.hset(args[2], args[0], str(args[1]) + ',' + str(args[3]) + ',0')

    def getNumUsersConnected(self, roomId):
        type = 'Private Room' if len(roomId) == 4 else 'Public Room'
        return self.rooms.hget(type, roomId).split(",")[-1]

    def getAllID(self, type):
        return self.rooms.hkeys(type)

    def getAllName(self, type):
        names = [room.split(',')[0] for room in self.rooms.hgetall(type).values()]
        return names

    def getAllUser(self, type):
        users = [room.split(',')[-1] for room in self.rooms.hgetall(type).values()]
        return users

    def newConnection(self, roomId):
        type = 'Private Room' if len(roomId) == 4 else 'Public Room'
        old = self.rooms.hget(type, roomId)
        print(old)
        self.rooms.hset(type, roomId, old.rsplit(",", 1)[0] + ',' + str(int(old.rsplit(",", 1)[1]) + 1))

    def disconnection(self, roomId):
        type = 'Private Room' if len(roomId) == 4 else 'Public Room'
        old = self.rooms.hget(type, roomId)
        if old.rsplit(",", 1)[1] == "1":
            self.rooms.hdel(type, roomId)
        else:
            self.rooms.hset(type, roomId, old.rsplit(",", 1)[0] + ',' + str(int(old.rsplit(",", 1)[1]) - 1))


