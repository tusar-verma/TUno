class Player:
    name = ""
    socket = None

    def __init__(self, name, socket):
        self.name = name
        self.socket = socket