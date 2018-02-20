import random


class Card:
    def __init__(self, value=0):
        self.value = value

    def __str__(self):
        return "Card (" + str(self.value) + ")"

    def __repr__(self):
        return "Card (" + str(self.value) + ")"


class Deck:
    def __init__(self, racer_type):
        self.racer_type = racer_type
        self.cards = [Card(2), Card(3), Card(4)]

    def __repr__(self):
        return self.racer_type + str(self.cards)

    def draw(self, number_of_cards=1):
        result = [];
        while number_of_cards>0:
            result.append(self.cards.pop());
            number_of_cards -= 1

        return result;

    def shuffle(self):
        random.shuffle(self.cards)


deck = Deck("test")
print(deck)
deck.shuffle()
print(deck)
print (deck.draw(1))
print(deck)



