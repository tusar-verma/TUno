import json

def firstCommand(playerId):
    return json.dumps({
        "command": "firstComm",
        "playerId": playerId
        })

def createGame(maxPlayers, penaltie, password):
    return json.dumps({
        "command": "create",
        "maxPlayers": int(maxPlayers),
        "penaltie": int(penaltie),
        "password": password
    })

def startGame():
    return json.dumps({
        "command": "start"
    })


def joinGame(gameId, password):
    return json.dumps({
        "command": "join",
        "gameId": gameId,
        "password": password
    }) 

def playCard(card, UNO):
    return json.dumps({
        "command": "play",
        "card": card.__dict__,
        "UNO": UNO
    })

def getGameStatus():
    return json.dumps({
        "command": "get"
    })

def sayUNO():
    return json.dumps({
        "command": "UNO"
    })

def drawCard():
    return json.dumps({
        "command": "drawcard"
    })

def eatCards():
    return json.dumps({
        "command": "eatcards"
    })

def messageQuit():
    return json.dumps({
        "command": "quit"
    })

def restartGame():
    return json.dumps({
        "command": "restartgame"
    })
