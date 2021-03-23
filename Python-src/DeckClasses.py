import random
import json

class Card:
    def __init__(self, name = None, color = None, special = False, dicCard = None):
        if dicCard != None:
           self.dicToCard(dicCard) 
        else:
            self.name = name
            self.color = color
            self.special = special

    def __str__(self):
        if self.color == None:
            return self.name
        return "(%s) %s" % (self.color, self.name)
        
    def __repr__(self):
        return str(self)
        
    def dicToCard(self, dicCard):
        self.name = dicCard["name"]
        self.color = dicCard["color"]
        self.special = dicCard["special"]

class UnoDeck:
    __deck = []
    def __init__(self):
        self.genCards()
        self.shuffleDeck()

    def __str__(self):
        strDeck = ""
        for card in self.__deck:
            strDeck += str(card) + "; "
        return "Amount: %i \n  %s" % (len(self.__deck),strDeck)

    def genCards(self):
        colors = ['Red', 'Green', 'Blue', 'Yellow']
        specials = ["+2", "Skip", "Reverse", "+4", "Wild"]
        for color in colors:
            # 1-9 cards
            for i in range(1,10):
                self.__deck.append(Card(color = color, name = str(i)))
                self.__deck.append(Card(color = color, name = str(i)))
            # 0 cards
            self.__deck.append(Card(color = color, name = "0"))
            # special cards
            for special in specials:
                if special in ["+4", "Wild"]:
                    self.__deck.append(Card(name = special, color = None, special = True))
                else:
                    self.__deck.append(Card(name = special, color = color, special = True))  
                    self.__deck.append(Card(name = special, color = color, special = True))  

    def shuffleDeck(self):
        random.shuffle(self.__deck)

    def getCard(self):
        return self.__deck.pop(0)

    def putCardInDeck(self, card):
        if card.special and (card.name == "+4" or card.name == "Wild"):
            card.color = None
        self.__deck.insert(random.choice(range(0,len(self.__deck))),card)


 