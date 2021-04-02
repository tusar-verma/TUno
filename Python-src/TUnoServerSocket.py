import json
import socket
import threading
import sys
import traceback
from DeckClasses import Card
from TUnoGame import TUnoGame, gameStatus

#python TUnoServerSocket.py 127.0.0.1 65432

# El gameId es el playerId del usuario que creo la sala
# {gameId: (TUnoGame, {player1: conn1, ..., playerN: connN})}
games = {}
# Los keys son el playerId y el value es el gameId del juego en el que se encuentra
# {playerId: gameId}
players = {}

# gameid es el playerid del creador del game
def create(gameId, maxPlayers, password, playerConn, penaltie = 2):
    try:
        games[gameId] = (TUnoGame(maxPlayers, password, penaltie), {gameId: playerConn})
        games[gameId][0].addPlayerToGame(gameId)
        players[gameId] = gameId
        return (True, "game created")
    except Exception:
        traceback.print_exc()
        return (False, "couldn't create game")

def join(playerId, gameId, password, playerConn):
    if gameId in games:
        if games[gameId].checkPassword(password):
            result, message = games[gameId][0].addPlayerToGame(playerId)
            if result: 
                players[playerId] = gameId
                games[gameId][1][playerId] = playerConn
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
            game.setInitRandomTurn()
            threadStart = threading.Thread(target=thread_TUno_start_game_broadcast,args=(playerId))
            threadStart.start()
            threadStart.join()             
            return None
        else:
            return "Not enough players"
    else:
        return "Player has no game"

def drawCard(gameId):
    return games[gameId][0].getCard()

def eatCards(gameId):
    cards = games[gameId][0].eatCards()
    if cards == None:
        return (False, "You dont have to eat cards")
    return (True, cards)

def play(gameId, card, UNO):  
    return games[gameId][0].playCard(card, UNO)    

def get_game_status(gameId):
    return games[gameId][0].getGameState()

def sayUno(playerId, gameId):
    game = games[gameId][0]
    result, message = game.sayUNO(playerId)
    if result: 
        c = games[gameId][1][message]
        c.sendAll(game.getPenalitieCards())
        return (True, None)
    else:
        return (False, message)
    
def quitTUno(playerId, gameId, playerConn):
    # borrar game si tiene
    if playerId in games:
        del games[playerId]
    # borrar de la lista de jugadores
    if playerId in players:
        del players[playerId]
    if gameId != None and gameExists(gameId):
        # Si se borra el jugador y no se puede seguir, borrar el juego
        if not games[gameId].removePlayer(playerId):
            del games[gameId]    
        else:
            # Si se puede seguir, mandar a los jugadores restantes el status del juego
            # mostrando que se fue el jugador removido
            tQuit = threading.Thread(target=thread_TUno_game_status_broadcast,args=(gameId,))
            tQuit.start()

def restartGame(playerId):
    if gameExists(playerId):
        game = games[playerId][0]        
        return game.restartGame()
    else:
        return (False, "Player has no game")
    pass

def gameExists(gameId):
    return gameId in games

def isPlayerTurn(playerId, gameId):
    return games[gameId].getNextPlayerToPlay() == playerId

def validate_playerId(playerId):
    return ((playerId != None or playerId != "") and playerId not in players)

# El thread manda a cada jugador del game "gameId" sus cartas iniciales y el gameStatus
def thread_TUno_start_game_broadcast(gameId):
    if (gameExists(gameId)):
        for c in games[gameId][1].values():
            startCards = games[gameId][0].getStartingCards()
            gameStatus = games[gameId][0].getGameState()
            jMessage = json.dumps([startCards, gameStatus], sort_keys = True)
            c.sendall(jMessage)
    else:
        raise Exception("Attempted to start a non-existent game")
        
   
def thread_TUno_game_status_broadcast(gameId):
    if gameExists(gameId):            
        message = games[gameId][0].getGameState()
        jsonMessage = json.dumps(message.__dict__, sort_keys = True, indent=4)
        for c in games[gameId][1].values():
            c.sendAll(jsonMessage)
    else:
        raise Exception("Attempted to broadcast in a non-existent game")

def thread_TUno_func(playerConn):
    print("Started thread for: ", playerConn.getsockname(), ". Remote: ", playerConn.getpeername())
    playerId = None
    gameId = None
    while True:
        recived = None
        try:
            recived = playerConn.recv(2048).decode()
            print("From: ", playerConn.getsockname(), f" ({playerId}): ", recived)
            data = json.loads(recived)
        except:
            break
        if not data:
            break
        else:                        
            message = None
            broadcastStatus = False
            command = data["command"]            
            if playerId == None:
                if command == "firstComm":       
                    if validate_playerId(data["playerId"]):
                        playerId = data["playerId"]
                        players[playerId] = None
                        message = "Added gamer"
                    else: 
                        message = "Bad playerId"
                else:
                    message = "No playerId is stored for this client"
            else:                         
                if command == "create": 
                    result, message = create(playerId, data["maxPlayers"], data["password"], playerConn, data["penaltie"]) 
                    if result: gameId = playerId                       
                elif command == "quit":       
                    break
                elif command == "join": 
                    broadcastStatus, message = join(playerId, data["gameId"], data["password"], playerConn)
                    if broadcastStatus: gameId = data["gameId"]                        
                elif gameId != None and gameExists(gameId):      
                    if command == "start":
                        # el broadcast se hace en el thread de start
                        message = startGame(playerId)
                    elif command == "restartgame":
                        broadcastStatus, message = restartGame(playerId)                        
                    elif command == "get": 
                        message = get_game_status(gameId)  
                    elif command == "UNO":
                        broadcastStatus, message = sayUno(playerId, gameId)
                    elif isPlayerTurn(playerId, gameId):
                        if command == "play":        
                            broadcastStatus, message = play(gameId, data["card"], data["UNO"])
                        elif command == "drawcard":
                            message = drawCard(gameId)
                            broadcastStatus = True
                        elif command == "eatcards":
                            # broadcast status y mandar mensaje de las cartas que hay q comer
                            broadcastStatus, message = eatCards(gameId)
                        else: 
                            message = "Bad command"
                    else:
                        message = "Not your turn"
                else:
                    gameId = None
                    message = "There is no game"

            if message != None:     
                print("Sending to ", playerId, ": ", message)               
                playerConn.sendall(json.dumps(message).encode())
            elif broadcastStatus:
                tBrodcast = threading.Thread(target=thread_TUno_game_status_broadcast,args=(gameId,))
                tBrodcast.start()
    
    quitTUno(playerId, gameId, playerConn)
    print("Disconnected from: ", playerConn.getsockname(), " PlayerID: ", playerId)
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