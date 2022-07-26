import redis

class Rooms:
    def __init__(self):
        self.rooms = redis.StrictRedis('localhost', 6379, charset="utf-8", decode_responses=True, db=1)
        self.rooms.flushdb()

    def addRoom(self, *args):
        if len(args) == 3:
            args.append(None)
        self.rooms.hmset(args[0], {"id": args[1], "type": args[2], "password": args[3]})

    def validatePassword(self):
        pass

    def getRoomId(self):
        return self.id

    def getRoomType(self):
        return self.type

    def removeRoom(self):
        pass


