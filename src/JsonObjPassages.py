import threading
import json
from src.TUnoServer.TUnoGame import TUnoGame
from types import SimpleNamespace
from src.DeckPackage.DeckClasses import Card


def main():    
    print(Card("2","Green",False).__dict__)
    a = TUnoGame(3, "asdasd")
    a.addPlayerToGame("player1")
    a.addPlayerToGame("player2")
    a.addPlayerToGame("player3")
    a.addPlayerToGame("player4")
    a.setInitRandomTurn()
    a.playCard(Card("+4", "Green", True), False)
    a.eatCards()
    result, message = a.playCard(Card("4", "Green", True), False)
    print(result, message)
    s = a.getGameState()
    print(json.dumps(s, indent=4))
    a.restartGame()
    s = a.getGameState()
    print(json.dumps(s, indent=4))


if __name__ == "__main__":
    main()
        

