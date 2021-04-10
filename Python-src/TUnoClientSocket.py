import socket
import threading
import json
import time

from queue import Queue
from TUnoClientFunctions import *
from DeckClasses import Card


def switch(func, args):
    print("func: ", func, " args: ", args)
    switcher = {
        "1": firstCommand,
        "2": createGame,
        "3": startGame,
        "4": restartGame,
        "5": joinGame,
        "6": playCard,
        "7": getGameStatus,
        "8": sayUNO,
        "9": drawCard,
        "10": eatCards,
        "11": messageQuit
    }
    func = switcher.get(func, lambda a = (): "Invalid")
    return func(*args)


class TUnoClient:
    socket = None
    connected = False

    # max size 0 = infinito     
    serverMessages = Queue(maxsize=0)
    stop = False

    def __init__(self, Host = '127.0.0.1', port = 65432):
        self.HOST = Host
        self.PORT = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connectToServer(self):
        try: 
            self.socket.connect((self.HOST, self.PORT))
            self.connected = True
            threading.Thread(target=self.thread_receiver).start()
            # threading.Thread(target=self.thread_processMessage).start()
            # threading.Thread(target=self.threadConsole).start()
            return True
        except:
            self.connected = False
            return False

    def sendMessage(self, message):
        print("Sending... ", message)
        self.socket.sendall(message.encode())
    
#     def threadConsole(self):
#         command =""
#         while not self.stop and command != "11":        
#             print("""    
# 1: firstCommand (playerId),
# 2: createGame (maxPlayers, penaltie, password),
# 3: startGame,
# 4: restartGame,
# 5: joinGame (gameId, password),
# 6: playCard (card, UNO),
# 7: getGameStatus,
# 8: sayUNO,
# 9: drawCard,
# 10: eatCards,
# 11: Quit   
# """)
#             try:                
#                 command= input()
#                 data = ""
#                 if ";" in command:
#                     command, arguments = command.split(';')
#                     arguments = arguments.split(' ')
#                     data = switch(command, arguments)
#                 else:
#                     data = switch(command,())
#                 if data != "Invalid":
#                     self.sendMessage(data)
#             except:
#                 print("Something gone wrong, couldn't send command to server")
#         print("Thread console stopped")


    def thread_receiver(self):
        try:            
            while not self.stop:
                data = self.socket.recv(2048).decode()
                if not data:
                    break
                self.serverMessages.put(json.loads(data))
        except:            
            print("Connection with server closed")
        finally:          
            self.connected = False
            self.stop = True
            self.serverMessages.put("STOP")
        print("Thread receiver stopped")

    def thread_processMessage(self):
        while not self.stop:        
            data = self.serverMessages.get()
            if data == "STOP":
                break
            print("Recived from server: ", data)        
        print("Thread procesor stopped")

    def quitGame(self, tr, tp, tc):
        self.stop = True
        self.sendMessage(messageQuit())
        self.connected = False
   