from time import sleep

import player
from square import Square

import os

def cls():
    #os.system('cls' if os.name=='nt' else 'clear')
    clear = "\n" * 100
    print (clear)

players = []


def setup():
    players.append(player.Player('Player 1', 1))
    players.append(player.Player('Player 2', 2))


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


def take_turn():
    racers = []
    # select next move
    for game_player in players:
        game_player.select_move()
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

    draw_state(reversed_racers)
    sleep(1)

    apply_slipstream(reversed_racers)
    #    print(racers)

    add_exhaustion(racers)

    draw_state(reversed_racers)

    return racers[0].token.distance_from_finish < 0


setup()
while not take_turn():
    print('Next Round')
    sleep(2)
