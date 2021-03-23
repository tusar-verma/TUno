import json
import socket
import threading
import sys
import traceback
from DeckClasses import Card
from TUnoGame import TUnoGame, gameStatus

# El gameId es el playerId del usuario que creo la sala
# {gameId: (TUnoGame, [conn1,...,conn4])}
games = {}
# Los keys son el playerId y el value es el gameId del juego en el que se encuentra
# {playerId: gameId}
players = {}

        
# gameid es el playerid del creador del game
def create(gameId, maxPlayers, password, playerConn):
    try:
        games[gameId] = (TUnoGame(maxPlayers, password), [playerConn])
        games[gameId][0].addPlayerToGame(gameId)
        players[gameId] = gameId
        return (True, "game created")
    except Exception:
        traceback.print_exc()
        return (False, "couldn't create game")
# lock
def join(playerId, gameId, password, playerConn):
    if gameId in games:
        if games[gameId].checkPassword(password):
            result, message = games[gameId][0].addPlayerToGame(playerId)
            if result: 
                players[playerId] = gameId
                games[gameId][1].append(playerConn)
                return (True, message)
            return (False,  message)
        else:
            return (False, "invalid password")
    else:
        return (False, "game does not exist")
    pass

def startGame(playerId):
    if playerId in games:
        game = games[playerId][0]
        if len(game.players) > 1:
            x = threading.Thread(target=thread_TUno_game_broadcast,args=(playerId,games[playerI))
            x.start()
        else:
            return (False, "Not enough players")
        # repartir cartas
        # pedir la siguiente jugada al jugador correspondiente
        pass
    else:
        return (False, "Player has no game")

def drawCard(gameId):
    return games[gameId][0].getCard().__dict__

def eatCards(gameId):
    cards = games[gameId][0].eatCards()
    if len(cards) == 0:
        return (False, "You dont have to eat cards")
    else:
        return (True, cards)
    pass

def dealCards(gameId):
    pass

# lock
def play(playerId, gameId, card):  
    try:
        games[gameId][0].playCard(card)
        return "Card played"
    except: 
        return "Invalid play"
#unlock

def get_game_status(playerId, gameId):
    return games[gameId].getGameState()
    

def quitTUno(playerId, gameId, playerConn):
    message = ""
    # borrar game si tiene
    if playerId in games:
        del games[playerId]
        message += "Removed game of player; " 
    # borrar de la lista de jugadores
    if playerId in players:
        del players[playerId]
        message += "Removed player from server; "
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
   
def thread_TUno_game_broadcast(gameId, message):
    jsonMessage = json.dumps(message.__dict__, sort_keys = True, indent=4)
    for c in games[gameId][1]:
        c.sendAll(jsonMessage)

def thread_TUno_func(playerConn):
    playerId = None
    gameId = None
    quiting = False
    while True:
        data = json.loads(playerConn.recv(2048).decode())
        if not data:
            quitTUno(playerId, gameId, playerConn)
            print("Lost connection with: ", playerConn, " PlayerID: ", playerId)
            break
        else:
            print("From: ", playerConn, f" ({playerId}): ", data)
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
                    result, message = create(playerId, data["maxPlayers"], data["password"], playerConn) 
                    if result:
                        gameId = playerId
                elif data["commnad"] == "join": 
                    result, message = join(playerId, data["gameId"], data["password"], playerConn)
                    if result:
                        gameId = data["gameId"]
                elif gameId != None and gameExists(gameId):                        
                    if isPlayerTurn(playerId, gameId):
                        if data["commnad"] == "play": 
                            message = play(playerId, gameId, data["card"])     
                        elif data["commnad"] == "quit": 
                            message = quitTUno(playerId,gameId, playerConn) 
                            quiting = True
                        elif data["commnad"] == "get": 
                            message = get_game_status(playerId, gameId)     
                        elif data["command"] == "drawcard":
                            message = drawCard(gameId)
                        else: 
                            message = "Bad command"
                    else:
                        message = "Not your turn"
                else:
                    gameId = None
                    message = "There is no game"
            playerConn.sendall(json.dumps(message))
            if quiting: break
    playerConn.close()

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