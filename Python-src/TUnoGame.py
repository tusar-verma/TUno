import DeckClasses

class TUnoGame:
    maxPlayers = 2
    deck = None
    def __init__(self, playerAmount):
        self.__playersAumount = playerAmount
        self.deck = DeckClasses.UnoDeck()
        
    def checkValidGame(self):
        return self.__playersAumount <= 4 and self.__playersAumount > 1

    
            
    