import socket
import threading
import json
import time
from queue import Queue
from TUnoClientFunctions import *

from DeckClasses import Card

def main():
    try:
        client = TUnoClient()
        client.sendMessage(firstCommand("ElNegro7u7"))
        time.sleep(2)
        client.quitGame()
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
            t1 = threading.Thread(target=self.thread_processMessage)
            t.start()
            t1.start()
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
            data = self.SOCKET.recv(2048).decode()
            if not data:
                self.stop = True
                self.serverMessages.put("STOP")
                break
            self.serverMessages.put(json.loads(data))
        print("Thread receiver stopped")

    def thread_processMessage(self):
        while not self.stop:        
            data = self.serverMessages.get()
            if data == "STOP":
                break
            print("Recived from server: ", data)        
        print("Thread procesor stopped")

    def quitGame(self):
        self.stop = True
        self.sendMessage(messageQuit())


if __name__ == "__main__":
    main()