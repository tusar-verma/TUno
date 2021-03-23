import json
from TUnoGame import TUnoGame
from types import SimpleNamespace
from DeckClasses import Card

def main():
    a = TUnoGame(3, "asdasd")
    a.addPlayerToGame("player1")
    a.addPlayerToGame("player2")
    a.playCard(Card("+4", "Green", True))
    s = a.getGameState()
    sc = a.getStartingCards()
    print(len(sc[0]))
    print(sc[0])
    #j = json.dumps(s.__dict__, sort_keys = True, indent=4)
    jsc = json.dumps(sc, sort_keys = True, indent=4)
    #print(j)
    #o = json.loads(j,object_hook=lambda d: SimpleNamespace(**d))
    print(jsc)
    #c = a.eatCards()
    #j1 = json.dumps(c, sort_keys= True, indent=4)
    #print(j1)
    # print(type(o))
    # print(o.lastCardPlayed)


if __name__ == "__main__":
    main()
        

