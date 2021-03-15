import DeckClasses

class TUnoGame:
    
    __maxPlayers = 4
    __deck = DeckClasses.UnoDeck()
    __players = []
    __discardPile = [] 
    __turn = 0
    handSize = 7

    def __init__(self, maxPlayers):
        if self.checkValidGame(maxPlayers):
           self.maxPlayers = maxPlayers
        else:
           raise Exception("The maximum number of players is invalid")
        
    def checkValidGame(self, maxPlayers):
        return maxPlayers <= 4 and maxPlayers > 1
    
    def addPlayerToGame(self, player):
        self.__players.append(player)
    
    def restartGame(self):
        self.__deck.shuffleDeck()

    def getStartingCards(self):        
        return [self.__deck.getCard() for i in range(self.handSize)]
    
    def getNextPlayerToPlay(self):
        return self.__players[self.__turn]
        
    def firstGameCard(self):
        self.__discardPile.append(self.__deck.getCard())
    
    def validateCardToPlay(self, card):
        pass

    def playCard(self, card):
        pass
        


            
    