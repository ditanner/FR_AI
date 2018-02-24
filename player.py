from FR_enums import Racer_Type

import deck


class Player:
    def __init__(self, name, number):
        self.name = name

        sprinteur_racer = Racer(name, Racer_Type.SPRINTEUR, ((8 * 6) + (12 * 2)) + number, 1)
        rouleur_racer = Racer(name, Racer_Type.ROULEUR, ((8 * 6) + (12 * 2)) + number, 0)
        self.racers = (sprinteur_racer, rouleur_racer)

    def select_move(self):
        for racer in self.racers:
            racer.select_move()


class Racer:
    def __init__(self, name, type, starting_position, on_right):
        self.name = name + ' ' + type.name
        self.type = type
        self.label = name[len(name)-1] + type.name[0]
        self.token = Token(self.name, starting_position, on_right)
        self.deck = deck.getDeck(self.type)
        self.recycle_deck = deck.Deck('Recycle Deck')
        self.next_move = ''


        self.deck.shuffle()

    def select_move(self):
        hand_selection = self.deck.draw(1)

        # select which card to use
        self.next_move = hand_selection[0]

        hand_selection.remove(self.next_move)
        self.recycle_deck.cards = [*self.recycle_deck.cards, *hand_selection]

    def move_token(self, places, others):
        self.token.distance_from_finish -= places
        self.token.on_right = 1
        for other in others:
            if self.token.distance_from_finish < other.token.distance_from_finish:
                break
            if self.token.distance_from_finish == other.token.distance_from_finish:
                if other.token.on_right == 0:
                    self.token.distance_from_finish += 1
                    self.token.on_right = 1
                    continue
                else:
                    self.token.on_right = 0
                    continue

    def take_move(self, others):
        self.move_token(self.next_move.value, others)

    def add_exhaustion(self):
    #    print('Exhaustion', self.name)
        self.recycle_deck.cards.append(deck.Card(2))

    def __repr__(self):
        return self.token.__repr__()

    def __lt__(self, other):
        if self.token.distance_from_finish != other.token.distance_from_finish:
            return self.token.distance_from_finish < other.token.distance_from_finish
        else:
            return self.token.on_right > other.token.on_right


class Token:
    def __init__(self, name, starting_position, on_right):
        self.name = name
        self.distance_from_finish = starting_position
        self.on_right = on_right

    def has_passed_finish_line(self):
        if self.distance_from_finish < 0:
            return self.distance_from_finish
        return 0

    def __repr__(self):
        return self.name + ' ' + str(self.distance_from_finish) + ' ' + str(self.on_right)
