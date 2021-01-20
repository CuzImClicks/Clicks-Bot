from mojang import MojangAPI


class User:

    def __init__(self, nickname):

        self.nickname = nickname

    def get_uuid(self):

        return MojangAPI.get_uuid(self.nickname)