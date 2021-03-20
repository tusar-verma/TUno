import json
from TUnoGame import TUnoGame
from types import SimpleNamespace

def main():
    a = TUnoGame(3, "asdasd")
    a.addPlayerToGame("player1")
    a.addPlayerToGame("player2")
    s = a.getGameState()
    print(s)
    j = json.dumps(s.__dict__, sort_keys = True, indent=4)
    o = json.loads(j,object_hook=lambda d: SimpleNamespace(**d))
    print(j)
    print()
    
    print(type(o))
    print(o.lastCardPlayed)


if __name__ == "__main__":
    main()
        

