import random

class Card:
    def __init__(self, color, number):
        self.color = color
        self.number = number

    def __str__(self):
        return "%s, %s" % (self.color, self.number)

class SpecialCard:
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def __str__(self):
        if self.color == None:
            return self.name
        return "%s, %s" % (self.color, self.name)

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
                self.__deck.append(Card(color,i))
                self.__deck.append(Card(color,i))
            # 0 cards
            self.__deck.append(Card(color,0))
            # special cards
            for special in specials:
                if special in ["+4", "Wild"]:
                    self.__deck.append(SpecialCard(special,None))
                else:
                    self.__deck.append(SpecialCard(special,color))  
                    self.__deck.append(SpecialCard(special,color))  

    def shuffleDeck(self):
        random.shuffle(self.__deck)

    def getCard(self):
        return self.__deck.pop(0)

    def putCardInDeck(self, card):
        pass

a = UnoDeck()
print(a)
print(a.getCard())
print(a)
