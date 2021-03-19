import DeckClasses


class TUnoGame:
    
    __maxPlayers = 4
    __deck = DeckClasses.UnoDeck()
    __discardPile = None 
    __turn = 0
    __reverse = False
    __addingCards = False
    __amountToDraw = 0

    password = ""    
    players = []
    handSize = 7

    def __init__(self, maxPlayers, password):
        if self.checkValidGame(maxPlayers):
           self.maxPlayers = maxPlayers
           self.password = password
        else:
           raise Exception("The maximum number of players is invalid")
        
    def checkValidGame(self, maxPlayers):
        return maxPlayers <= 4 and maxPlayers > 1
    
    def checkPassword(self, password):
        return self.password == password
    
    def addPlayerToGame(self, player):
        if len(self.players) < self.__maxPlayers:                
            if player not in self.players:
                self.players.append(player)
                return "added player"
            else:
                return "player already in game"
        else:
            return "full room"

    
    def restartGame(self):
        self.__deck = DeckClasses.UnoDeck()

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
        if self.__addingCards:
            return card.name == "+4" or card.name == "+2"

        if card.color == self.__discardPile.color:
            return True
        elif card.name == self.__discardPile.name:
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

            # Caso de jugada de una carta especial
            if self.__discardPile.name == "Reverse":
                self.__reverse = not self.__reverse
                self.__pasoDeTurno(1)
            elif self.__discardPile.name == "Skip":
                self.__pasoDeTurno(2)
            elif self.__discardPile.name == "Wild": 
                self.__pasoDeTurno(1)
            elif self.__discardPile.name == "+4":
                self.__pasoDeTurno(1)
                self.__addingCards = True
                self.__amountToDraw += 4
            elif self.__discardPile.name == "+2":
                self.__pasoDeTurno(1)
                self.__addingCards = True
                self.__amountToDraw += +2
            else:             
                # Si no es una especial, es un numero   
                self.__pasoDeTurno(1)
        else:
            raise Exception ("Invalid card")
    
    def __pasoDeTurno(self, cantidad):
        for i in range(cantidad):
            if self.__reverse: 
                self.__turn -= 1           
                if self.__turn < 0:
                    self.__turn = self.__maxPlayers - 1
            else:
                self.__turn += 1                
                if self.__turn >= self.__maxPlayers:
                    self.__turn = 0
    # Si luego de que se haya tirado una combinacion de +4 o +2 y el siguiente jugador
    # no tenga para sumar, tomara las cartas sumadas. Esto consiste en que el cliente le avisa
    # al servidor y este llama al siguiente metodo que actualiza el amountToDraw y el addingCards
    def drawCards(self):
        cardsToDraw = []
        for i in range(self.__amountToDraw):
            cardsToDraw.append(self.__deck.getCard())
        
        self.__amountToDraw = 0
        self.__addingCards = False
        self.__pasoDeTurno(1)

        return cardsToDraw

    def getCard(self):
        self.__pasoDeTurno(1)
        return self.__deck.getCard()

        
    