import random

from FR_enums import Racer_Type


class Card:
    def __init__(self, value=0):
        self.value = value

    def __str__(self):
        return "Card (" + str(self.value) + ")"

    def __repr__(self):
        return "Card (" + str(self.value) + ")"


class Deck:
    def __init__(self, name):
        self.rename = name
        self.cards = []

    def __repr__(self):
        return self.rename + str(self.cards)

    def draw(self, number_of_cards=1):
        result = [];
        while number_of_cards > 0:
            result.append(self.cards.pop());
            number_of_cards -= 1

        return result;

    def shuffle(self):
        random.shuffle(self.cards)

    def addCard(self, card):
        self.cards.append(card)


class SprinteurDeck(Deck):
    def __init__(self):
        super().__init__('Sprinteur')
        self.cards = [Card(2), Card(2), Card(2),
                      Card(3), Card(3), Card(3),
                      Card(4), Card(4), Card(4),
                      Card(5), Card(5), Card(5),
                      Card(9), Card(9), Card(9)]


class RouleurDeck(Deck):
    def __init__(self):
        super().__init__('Rouleur')
        self.cards = [Card(3), Card(3), Card(3),
                      Card(4), Card(4), Card(4),
                      Card(5), Card(5), Card(5),
                      Card(6), Card(6), Card(6),
                      Card(7), Card(7), Card(7)]


def getDeck(racer_type):
    if racer_type == Racer_Type.SPRINTEUR:
        return SprinteurDeck()
    else:
        return RouleurDeck()

# deck = SprinteurDeck()
# print(deck)
# deck.shuffle()
# print(deck)
# print (deck.draw(1))
# print(deck)
