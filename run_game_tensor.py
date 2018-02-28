import game
import numpy as np
import tensorflow as tf

from SarsaLambda import SarsaLambdaTable

print('SarsaLambda, 1 player game, R then S')

initial_cards = 15
max_recycle_deck = 15
cards_in_hand = 4
position = 1
on_right = 1
next_move = 1
qr_observation_count = (initial_cards + max_recycle_deck + cards_in_hand + position + on_right + next_move) * 2

num_episodes = 2000

# reward list
rList = []

RL = SarsaLambdaTable(actions=list(range(0, 4)))


def play_game(is_learning):
    game.setup(1)

    rAll = 0
    d = False
    j = 0

    race_timer = 0
    is_race_over = False

    game.players[0].racers[1].draw_hand()

    RL.new_turn_init()

    # choose an action by greedily (with noise) picking from Q table
    s = game.current_observation()
    a1 = RL.choose_action(str(s))
    game.players[0].racers[1].select_move(a1)

    while j < 99:
        j += 1

        game.players[0].racers[0].draw_hand()
        s2 = game.current_observation()
        a2 = RL.choose_action(str(s2))
        game.players[0].racers[0].select_move(a2)

        result = game.make_move()

        if not is_learning:
            racers = []
            for player in game.players:
                racers = [*racers, *player.racers]
            racers.sort()
            racers.reverse()
            game.print_cards()
            game.draw_course(racers)
            if result:
                print(j, 'turns taken')

        r = 0
        if result:
            r = 1
            s3 = 'terminal'
        else:
            game.players[0].racers[1].draw_hand()
            s3 = game.current_observation()

        if is_learning:
            RL.learn(str(s), a1, r, str((s2)),a2)

        rAll += r
        if result:
            break

        # choose an action by greedily (with noise) picking from Q table
        s = game.current_observation()
        a1 = RL.choose_action(str(s))
        game.players[0].racers[1].select_move(a1)

        if is_learning:
            RL.learn(str(s2), a2, r, str((s3)),a1)

    rList.append(rAll)


if __name__ == '__main__':
    counter = 0

    for i in range(num_episodes):
        play_game(True)

        counter += 1

        if counter == 200:
            print('Current Table')
            print(RL.q_table)
            print(i+1, 'out of', num_episodes, 'episodes completed')
            counter = 0

    print('Score over time: ' + str(sum(rList) / num_episodes))
    print('Final Q-Table Values')
    print(RL.q_table)
