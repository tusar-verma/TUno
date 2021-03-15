import DeckClasses

class TUnoGame:
    
    __maxPlayers = 4
    __deck = DeckClasses.UnoDeck()
    __discardPile = None 
    __turn = 0
    __reverse = False
    
    players = []
    handSize = 7

    def __init__(self, maxPlayers):
        if self.checkValidGame(maxPlayers):
           self.maxPlayers = maxPlayers
        else:
           raise Exception("The maximum number of players is invalid")
        
    def checkValidGame(self, maxPlayers):
        return maxPlayers <= 4 and maxPlayers > 1
    
    def addPlayerToGame(self, player):
        self.players.append(player)
    
    def restartGame(self):
        self.__deck.shuffleDeck()

    def getStartingCards(self):        
        return [self.__deck.getCard() for i in range(self.handSize)]
    
    def getNextPlayerToPlay(self):
        return self.players[self.__turn]
        
    def firstGameCard(self):
        card = self.__deck.getCard()
        while card.special:
            self.__deck.putCardInDeck(card)
            card = self.__deck.getCard()

        self.__discardPile = card
    
    def validateCardToPlay(self, card):
        if card.color == self.__discardPile.color:
            return True
        elif card.name == "+4" or card.name == "Wild":
            return True
        return False


    def playCard(self, card):
        if self.validateCardToPlay(card):
            self.__deck.putCardInDeck(self.__discardPile)
            self.__discardPile = card
            # El cambio de color de las cartas wild y +4 se da cuando el cliente
            # pone el color del atributo de la carta segun lo que eliga el usuario
            # al usar la carta

            if self.__discardPile.name == "Reverse":
                self.__reverse = not self.__reverse
            elif self.__discardPile.name == "Skip":
                # bug: cuando se pasa del turno 3 (cuando max players es 4) 
                self.__turn += 2
            elif self.__discardPile.name == "Wild": 
                # bug: mismo bug de skip
                self.__turn += 1   
            elif self.__discardPile.name == "+4":
                # bug: mismo bug de skip
                self.__turn += 2
                # evento de 4 cartas el siguiente jugador
            elif self.__discardPile.name == "+2":
                # bug: mismo bug de skip
                self.__turn += 2
                # evento dar 2 cartas al siguiente jugador
            else:                
                # bug: mismo bug de skip
                self.__turn += 1

        else:
            raise Exception ("Invalid card")

        
    