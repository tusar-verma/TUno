import threading
import json
from TUnoGame import TUnoGame
from types import SimpleNamespace
from DeckClasses import Card

asd = 2

def main():
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
    print(json.dumps(s.__dict__, indent=4))
    a.restartGame()
    s = a.getGameState()
    print(json.dumps(s.__dict__, indent=4))


if __name__ == "__main__":
    main()
        

