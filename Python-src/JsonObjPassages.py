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
    a.playCard(Card("+4", "Green", True))
    a.eatCards()
    result, message = a.playCard(Card("+4", "Green", True))
    print(message)
    s = a.getGameState()
    sc = a.getStartingCards()
    #j = json.dumps(s.__dict__, sort_keys = True, indent=4)
    jsc = json.dumps(s.__dict__, sort_keys = True, indent=4)
    #print(j)
    o = json.loads(jsc)
    print(jsc)
    print("-"*20)
    #print(o)
    #print("-"*30,o[1]["isAddingCards"])
    #c = a.eatCards()
    #j1 = json.dumps(c, sort_keys= True, indent=4)
    #print(j1)
    # print(type(o))
    # print(o.lastCardPlayed)

if __name__ == "__main__":
    main()
        

