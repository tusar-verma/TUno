import socket
import threading
import json
from queue import Queue

from DeckClasses import Card

def main():
    try:
        client = TUnoClient()
        client.sendMessage(client.firstCommand("Tusar"))
    except:
        print("Couldn't connect to server")

class TUnoClient:

    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 65432        # The port used by the server
    SOCKET = None

    # max size 0 = infinito     
    serverMessages = Queue(maxsize=0)
    stop = False

    def __init__(self):
        try:
            self.connectToServer()   
            t = threading.Thread(target=self.thread_receiver)     
            t.start()
        except:
            raise Exception

    def connectToServer(self):
        self.SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SOCKET.connect((self.HOST, self.PORT))
        print("Connected!")

    def sendMessage(self, message):
        print("Sending... ", message)
        self.SOCKET.sendall(message.encode())

    def thread_receiver(self):
        while not self.stop:
            data = self.SOCKET.recv(1024)
            self.serverMessages.put(json.loads(data))
            print(data)
        print("Server stopped!")

    def thread_processMessage(self):
        print(self.serverMessages.get())

    def firstCommand(self, playerId):
        return json.dumps({
            "command": "firstComm",
            "playerId": playerId
            })

    def createGame(self, maxPlayers, penaltie, password):
        return json.dumps({
            "command": "create",
            "maxPlayers": maxPlayers,
            "penaltie": penaltie,
            "password": password
        })

    def joinGame(self, gameId, password):
        return json.dumps({
            "command": "join",
            "gameId": gameId,
            "password": password
        }) 

    def playCard(self, card, UNO):
        return json.dumps({
            "command": "play",
            "card": Card("4","Green", False).__dict__,
            "UNO": UNO
        })

if __name__ == "__main__":
    main()