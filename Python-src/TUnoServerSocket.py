import json
import socket
import threading
import sys
import traceback
from TUnoGame import TUnoGame, gameStatus


games = {}
players = {}

        
# gameid es el playerid del creador del game
def create(gameId, maxPlayers, password):
    try:
        games[gameId] = TUnoGame(maxPlayers, password)
        games[gameId].addPlayerToGame(gameId)
        players[gameId] = gameId
        return "game created"
    except Exception:
        traceback.print_exc()
        return "couldn't create game"

def join(playerId, gameId, password):
    if gameId in games:
        if games[gameId].checkPassword(password):
            result, message = games[gameId].addPlayerToGame(playerId)
            if result: 
                players[playerId] = gameId
            return message
        else:
            return "invalid password"
    else:
        return "game does not exist"
    pass

def play():
    return "implementar"

def get_game_status(playerId):
    gameId = players.get(playerId)
    if gameId == None:
        return (False, "No game")
    else:     
        return (True, games[gameId].getGameState())
    

def quitTUno(playerId):
    if playerId in players:
        del players[playerId]
    if playerId in games:
        del games[playerId]
    return "quited"

def validate_playerId(playerId):
    return ((playerId != None or playerId != "") and playerId not in players)
   

def thread_TUno_func(conn):
    playerId = None
    while True:
        data = json.loads(conn.recv(2048).decode())
        if not data:
            break
        else:
            print("From: ", conn, ": ", data)
            result = ""
            if playerId == None:       
                if validate_playerId(data["playerId"]):
                    playerId = data["playerId"]
                    players[playerId] = None
                    result = "added_gamer"
                else: 
                    result = "bad_playerId"
            else:         
                if data["commnad"] == "create": message = create(playerId, data["maxPlayers"], data["password"]) 
                if data["commnad"] == "join": message = join(playerId, data["gameId"], data["password"])
                if data["commnad"] == "play": message = play()     
                if data["commnad"] == "quit": message = quitTUno(playerId)    
                
                if data["commnad"] == "get": 
                    result, message = get_game_status(playerId)   
                    if result:
                        conn.sendall(json.dumps(result))
                        break            
            conn.sendall(str.encode(message))
                
        # conn.send(data)
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