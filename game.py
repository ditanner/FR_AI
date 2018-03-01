from time import sleep

import player
from square import Square

from colorama import Fore

from collections import Counter

import numpy as np

players = []


def cls():
    clear = "\n" * 100
    print(clear)


def setup(number_of_players):
    players.clear()
    players.append(player.Player('Player 1', 1, Fore.RED))
    if number_of_players > 1:
        players.append(player.Player('Player 2', 2, Fore.YELLOW))


def current_observation():
    results = []
    for player in players:
        for racer in player.racers:
            deck = [i.value for i in racer.deck.cards]
            c = Counter(deck)
            deck = [c[2], c[3], c[4], c[5], c[6], c[7], c[9]]
            recycle_deck = [i.value for i in racer.recycle_deck.cards]
            c = Counter(recycle_deck)
            recycle_deck = [c[2], c[3], c[4], c[5], c[6], c[7], c[9]]
            hand = [i.value for i in racer.hand_selection]
            next_move = -1
            if racer.next_move is not None:
                next_move = racer.next_move.value
            results = [*results, *deck, *recycle_deck,
                       *(hand + [-1] * 4)[:4], next_move, racer.token.distance_from_finish,
                       racer.token.on_right]

    return np.asarray(results)



def current_state():
    current_leading_player = ''
    current_leading_token = ''
    current_leading_position = 10000
    for game_player in players:
        for racer in game_player.racers:
            print(racer.name, racer.type, racer.token.distance_from_finish, racer.token.on_right)
            if racer.token.on_right and racer.token.distance_from_finish < current_leading_position:
                current_leading_player = game_player.name
                current_leading_token = racer.token
                current_leading_position = racer.token.distance_from_finish

    print(current_leading_player, current_leading_token.name, 'is leading the race at position',
          current_leading_position)


def apply_slipstream(reversed_racers):
    current_group = []
    front_of_group = 10000
    in_group = False
    for racer in reversed_racers:
        if not in_group:
            in_group = True
        elif front_of_group == racer.token.distance_from_finish + 2:
            # print('Slipstreaming', current_group)
            for group_member in current_group:
                group_member.token.distance_from_finish -= 1
        elif front_of_group > racer.token.distance_from_finish + 2:
            current_group = []

        current_group.append(racer)
        front_of_group = racer.token.distance_from_finish


def add_exhaustion(racers):
    for i in reversed(list(range(len(racers)))):
        racer = racers[i]
        if i == 0:
            racer.add_exhaustion()
            continue
        next_racer = racers[i - 1]
        next_next_racer = next_racer
        if i > 1:
            next_next_racer = racers[i - 2]

        if not (
                racer.token.distance_from_finish == next_racer.token.distance_from_finish + 1 and racer.token.on_right == next_racer.token.on_right) and not (
                racer.token.distance_from_finish == next_next_racer.token.distance_from_finish + 1 and racer.token.on_right == next_next_racer.token.on_right):
            racer.add_exhaustion()


def draw_state(reversed_racers):
    squares = []
    current_square = Square(reversed_racers[0].token.distance_from_finish)
    squares.append(current_square)
    for racer in reversed_racers:
        while True:
            if racer.token.distance_from_finish == current_square.position:
                if racer.token.on_right:
                    current_square.right_token = racer.label
                else:
                    current_square.left_token = racer.label
                break
            else:
                current_square = Square(current_square.position - 1)
                squares.append(current_square)

    cls()

    for square in squares:
        square.print_left_token()
    print('')
    for square in squares:
        square.print_right_token()
    print('')
    for square in squares:
        print('  ', end='')
    print(squares[len(squares) - 1].position)


def draw_course(reversed_racers):
    start_track_position = 75
    track_position = start_track_position
    for current_racer in reversed_racers:
        if current_racer.token.distance_from_finish < track_position:
            for i in range(track_position, current_racer.token.distance_from_finish, -1):
                print('  ', end=' ')
                track_position -= 1
        if current_racer.token.distance_from_finish == track_position:
            if current_racer.token.on_right == 0:
                print(current_racer.colour + current_racer.label, end=' ')
            else:
                print('  ', end=' ')

            track_position -= 1

        # print('  ', end=' ')

    print(Fore.RESET)

    track_position = start_track_position
    for current_racer in reversed_racers:
        if current_racer.token.distance_from_finish < track_position:
            for i in range(track_position, current_racer.token.distance_from_finish, -1):
                print('  ', end=' ')
                track_position -= 1
        if current_racer.token.distance_from_finish == track_position:
            if current_racer.token.on_right == 1:
                print(current_racer.colour + current_racer.label, end=' ')
                track_position -= 1
            else:
                continue

        # print('  ', end=' ')

    print(Fore.RESET)

    for i in range(start_track_position, 0, -1):
        print('{:2d}'.format(i), end=' ')

    print('F')


def print_cards():
    for player in players:
        for i in range(0, 2):
            print_cards_for_racer(player.racers[i])


def print_cards_for_racer(racer):
    print(racer.colour + racer.name, 'Deck:', end=' ')
    for card in racer.deck.cards:
        print(card.value, end=' ')

    print('Recycle:', end=' ')

    for card in racer.recycle_deck.cards:
        print(card.value, end=' ')

    print('Hand:', end=' ')

    for card in racer.hand_selection:
        print(card.value, end=' ')

    if racer.next_move is not None:
        print('Card to play:', racer.next_move.value, end=' ')

    print(Fore.RESET)


def make_move():
    ready_to_go = True
    for game_player in players:
        for racer in game_player.racers:
            if racer.next_move is None:
                ready_to_go = False

    if not ready_to_go:
        return

    racers = []
    # select next move
    for game_player in players:
        #        game_player.select_move()
        racers = [*racers, *game_player.racers]

    #    print(racers)
    # move, front racer first
    racers.sort()
    #    print(racers)
    for racer in racers:
        remaining_racers = racers.copy()
        remaining_racers.remove(racer)
        remaining_racers.sort()
        racer.take_move(remaining_racers)

    racers.sort()
    #    print(racers)

    reversed_racers = racers.copy()
    reversed_racers.reverse()

    #    draw_state(reversed_racers)
    #    sleep(1)

    apply_slipstream(reversed_racers)
    #    print(racers)

    add_exhaustion(racers)

    # draw_state(reversed_racers)

    # draw_course(reversed_racers)
    if racers[0].token.distance_from_finish < 0:
        return racers[0]
    else:
        return False
