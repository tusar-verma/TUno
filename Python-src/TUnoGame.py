import DeckClasses
import random

class TUnoGame:
    
    __maxPlayers = 4
    __deck = DeckClasses.UnoDeck()
    __discardPile = None 
    __turn = -1
    __reverse = False
    __addingCards = False
    __amountToDraw = 0

    # [[playerId, handSize];...,[playerId, handSize]]
    players = []
    handSize = 7
    password = ""
    winner = None    

    def __init__(self, maxPlayers, password):
        if self.checkValidGame(maxPlayers):
           self.maxPlayers = maxPlayers
           self.password = password
           self.__firstGameCard()
        else:
           raise Exception("The maximum number of players is invalid")
        
    def checkValidGame(self, maxPlayers):
        return maxPlayers <= 4 and maxPlayers > 1
    
    def checkPassword(self, password):
        return self.password == password
    
    def addPlayerToGame(self, player):
        if len(self.players) < self.__maxPlayers:                
            if player not in self.players:
                self.players.append([player, 1])
                return (True, None)
            else:
                return (False, "Player already in game")
        else:
            return (False, "Full room")

    # 0: removido, 1: No existe jugador en juego, 2: removido y borrar juego por falta de jugadores
    def removePlayer(self, playerToRemove):
        for player, handSize in self.players:
            if player == playerToRemove:
                self.players = [[player, handSize] for player, handSize in self.players if player != playerToRemove]
                if len(self.players) <= 1:
                    # borrar el juego ya que no hay suficientes jugadores
                    return 2
                else:
                    # borrado el jugador y se puede continuar jugando
                    return 0
                break
        # jugador no estaba en el juego
        return 1
    
    def restartGame(self):
        self.__deck = DeckClasses.UnoDeck()

    def getStartingCards(self):
        return [self.__deck.getCard().__dict__ for i in range(self.handSize)]
    
    def setInitRandomTurn(self):
        self.__turn = random.randint(0,len(self.players)-1)
    
    def getNextPlayerToPlay(self):
        return self.players[self.__turn][0]
        
    def __firstGameCard(self):
        card = self.__deck.getCard()
        while card.special:
            self.__deck.putCardInDeck(card)
            card = self.__deck.getCard()

        self.__discardPile = card
    
    def __validateCardToPlay(self, card):
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
        if self.winner != None: return (False, f"Game finished, winner: {self.winner}")
        if self.__validateCardToPlay(card):
            self.__deck.putCardInDeck(self.__discardPile)
            self.__discardPile = card
            self.players[self.__turn][1] -= 1
            self.__checkForWinner()
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
                return (True, None)
        else:
            return (False,"Invalid card")

    def __checkForWinner(self):
        for player, handSize in self.players:
            if handSize == 0:
                self.winner = player
    
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
    def eatCards(self):
        cardsToDraw = []
        # Si no hay que tomar cartas se devuelve una lista vacia y no se pasa de turno
        if self.__amountToDraw == 0:
            return None

        for i in range(self.__amountToDraw):
            cardsToDraw.append(self.__deck.getCard().__dict__)
        
        self.players[self.__turn][1] += self.__amountToDraw
        self.__amountToDraw = 0
        self.__addingCards = False
        self.__pasoDeTurno(1)

        return cardsToDraw

    def getCard(self):
        self.players[self.__turn][1] += 1
        self.__pasoDeTurno(1)
        return self.__deck.getCard().__dict__

    def getGameState(self):
        return gameStatus(self.__discardPile, self.getNextPlayerToPlay(), self.__reverse, self.__addingCards, self.__amountToDraw, self.players, self.winner)
        
    
class gameStatus:
    lastCardPlayed = None
    nextPlayerToPlay = None
    isReversed = None
    isAddingCards = None
    players = []
    amountToDraw = 0
    winner = None

    def __init__(self, last, nextP, isRev, isAdd, amDraw, players, winner):
        self.lastCardPlayed = last.__dict__
        self.nextPlayerToPlay = nextP
        self.isReversed = isRev
        self.isAddingCards = isAdd
        self.amountToDraw = amDraw
        self.players = players
        self.winner = winner

    def __str__(self):
        string = (f"last card played:  {self.lastCardPlayed}\n" 
                f"next player: {self.nextPlayerToPlay}\n"
                f"is round going backwards: {self.isReversed}\n"
                f"is adding cards: {self.isAddingCards}\n"
                f"amount to draw: {self.amountToDraw}\n"
                f"players: {self.players}\n"
                f"winner: {self.winner}\n"
        )
        return string
        