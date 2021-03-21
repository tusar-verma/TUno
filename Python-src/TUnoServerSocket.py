import json
import socket
import threading
import sys
import traceback
from DeckClasses import Card
from TUnoGame import TUnoGame, gameStatus


games = {}
players = {}

        
# gameid es el playerid del creador del game
def create(gameId, maxPlayers, password):
    try:
        games[gameId] = TUnoGame(maxPlayers, password)
        games[gameId].addPlayerToGame(gameId)
        players[gameId] = gameId
        return (True, "game created")
    except Exception:
        traceback.print_exc()
        return (False, "couldn't create game")
# lock
def join(playerId, gameId, password):
    if gameId in games:
        if games[gameId].checkPassword(password):
            result, message = games[gameId].addPlayerToGame(playerId)
            if result: 
                players[playerId] = gameId
                return (True, message)
            return (False,  message)
        else:
            return (False, "invalid password")
    else:
        return (False, "game does not exist")
    pass

def startGame(playerId):
    pass

def drawCard(playerId):
    pass

def eatCards(playerId):
    pass

def dealCards(gameId):
    pass

# lock
def play(playerId, gameId, card):  
    try:
        games[gameId].playCard(card)
        return "Card played"
    except: 
        return "Invalid play"

def get_game_status(playerId, gameId):
    return games[gameId].getGameState()
    

def quitTUno(playerId, gameId):
    message = ""
    if playerId in players:
        del players[playerId]
        message += "Removed player from server; "
    if playerId in games:
        del games[playerId]
        message += "Removed game of player; " 
    if gameId != None and gameExists(gameId):
        result = games[gameId].removePlayer(playerId)
        if result == 0:
            message += "Succesfully removed from game"
        elif result == 1:
            message += "Gamer was not in game"
        else:
            message += "Succesfully removed from game and game deleted due to lack of players"
    return message

def gameExists(gameId):
    return gameId in games

def isPlayerTurn(playerId, gameId):
    return games[gameId].getNextPlayerToPlay() == playerId

def validate_playerId(playerId):
    return ((playerId != None or playerId != "") and playerId not in players)
   

def thread_TUno_func(conn):
    playerId = None
    gameId = None
    quiting = False
    while True:
        data = json.loads(conn.recv(2048).decode())
        if not data:
            quitTUno(playerId, gameId)
            print("Lost connection with: ", conn, " PlayerID: ", playerId)
            break
        else:
            print("From: ", conn, f" ({playerId}): ", data)
            message = ""
            if playerId == None:       
                if validate_playerId(data["playerId"]):
                    playerId = data["playerId"]
                    players[playerId] = None
                    message = "Added gamer"
                else: 
                    message = "Bad playerId"
            else:         
                if data["commnad"] == "create": 
                    result, message = create(playerId, data["maxPlayers"], data["password"]) 
                    if result:
                        gameId = playerId
                elif data["commnad"] == "join": 
                    result, message = join(playerId, data["gameId"], data["password"])
                    if result:
                        gameId = data["gameId"]
                elif gameId != None and gameExists(gameId):                        
                    if isPlayerTurn(playerId, gameId):
                        if data["commnad"] == "play": 
                            message = play(playerId, gameId, data["card"])     
                        elif data["commnad"] == "quit": 
                            message = quitTUno(playerId,gameId) 
                            quiting = True
                        elif data["commnad"] == "get": 
                            message = get_game_status(playerId, gameId)     
                        else: 
                            message = "Bad command"
                    else:
                        message = "Not your turn"
                else:
                    gameId = None
                    message = "There is no game"
            conn.sendall(json.dumps(message))
            if quiting: break
    conn.close()

def main():    
    if len(sys.argv) != 3:
        raise Exception("Please check the command line arguments") 

    HOST = str(sys.argv[1])  # Standard loopback interface address (localhost)
    PORT = int(sys.argv[2])        # Port to listen on (non-privileged ports are > 1023)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            
            print('Connected by', addr)
            x = threading.Thread(target=thread_TUno_func,args=(conn,))
            x.start()

main()