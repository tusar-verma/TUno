import socket
import threading
import json
import time


from queue import Queue
from src.CommonResources.DeckClasses import Card
from TUnoClientFunctions import messageQuit



# def switch(func, args):src.TUnoServer
#     print("func: ", func, " args: ", args)
#     switcher = {
#         "1": firstCommand,
#         "2": createGame,
#         "3": startGame,
#         "4": restartGame,
#         "5": joinGame,
#         "6": playCard,
#         "7": getGameStatus,
#         "8": sayUNO,
#         "9": drawCard,
#         "10": eatCards,
#         "11": messageQuit
#     }
#     func = switcher.get(func, lambda a = (): "Invalid")
#     return func(*args)


class TUnoClient:
    socket = None
    connected = False

    # max size 0 = infinito     
    serverMessages = Queue(maxsize=0)

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
        except:
            self.connected = False

    def send_message(self, message):
        print("Sending... ", message)
        try:
            self.socket.sendall(message.encode())
        except (ConnectionResetError, ConnectionAbortedError):
            print("Lost connection with server")
            self.connected = False
            self.serverMessages.put("STOP")



    def thread_receiver(self):
        try:            
            while self.connected:
                data = self.socket.recv(2048).decode()
                if not data:
                    break
                self.serverMessages.put(json.loads(data))
        except:            
            print("Connection with server closed")
        finally:          
            self.connected = False
            self.serverMessages.put("STOP")
        print("Thread receiver stopped")

    def quit_game(self):
        self.send_message(messageQuit())
        self.connected = False
       
    # def thread_processMessage(self):
    #     while self.connected:        
    #         data = self.serverMessages.get()
    #         if data == "STOP":
    #             break
    #         print("Recived from server: ", data)        
    #     print("Thread procesor stopped")

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
