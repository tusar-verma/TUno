import json
import socket
import threading
import sys
import traceback
from TUnoGame import TUnoGame

gameId = 0
games = {}
players = []

        
# gameid es el playerid del creador del game
def create(gameId, maxPlayers, password):
    try:
        games[gameId] = TUnoGame(maxPlayers, password)
        games[gameId].addPlayerToGame(gameId)
        return "game created"
    except Exception:
        traceback.print_exc()
        return "couldn't create game"

def join(playerId, gameId, password):
    if gameId in games:
        if games[gameId].checkPassword(password):
            return games[gameId].addPlayerToGame(playerId)
        else:
            return "invalid password"
    else:
        return "game does not exist"
    pass

def play():
    return "implementar"

def quitTUno(playerId):
    if playerId in players:
        players.remove(playerId)
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
                    players.append(players)
                    result = "added_gamer"
                else: 
                    result = "bad_playerId"
            else:         
                if data["commnad"] == "create": result = create(playerId, data["maxPlayers"], data["password"]) 
                if data["commnad"] == "join": result = join(playerId, data["gameId"], data["password"])
                if data["commnad"] == "play": result = play()
                if data["commnad"] == "quit": result = quitTUno(playerId)        
            
            conn.sendall(str.encode(result))
                
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