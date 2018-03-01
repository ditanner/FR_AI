import game
import numpy as np
import tensorflow as tf

from TensorNet import DeepQNetwork

print('TensorNet, 1 player game, R then S')

initial_cards = 7
max_recycle_deck = 7
cards_in_hand = 4
position = 1
on_right = 1
next_move = 1
qr_observation_count = (initial_cards + max_recycle_deck + cards_in_hand + position + on_right + next_move) * 2

num_episodes = 20000

# reward list
rList = []

RL = DeepQNetwork(n_actions=4, n_features=qr_observation_count,
                  learning_rate=0.01,
                  reward_decay=0.9,
                  e_greedy=0.9,
                  replace_target_iter=200,
                  memory_size=2000,
                  # output_graph=True
                  )


def play_game(is_learning):
    game.setup(1)

    rAll = 0
    d = False
    j = 0

    race_timer = 0
    is_race_over = False

    while j < 99:
        j += 1

        # choose an action by greedily (with noise) picking from Q table
        game.players[0].racers[1].draw_hand()
        s = game.current_observation()
        a1 = RL.choose_action(s)
        game.players[0].racers[1].select_move(a1)
        if not is_learning:
            game.print_cards_for_racer(game.players[0].racers[1])

        game.players[0].racers[0].draw_hand()
        s2 = game.current_observation()
        a2 = RL.choose_action(s2)
        game.players[0].racers[0].select_move(a2)
        if not is_learning:
            game.print_cards_for_racer(game.players[0].racers[0])

        result = game.make_move()

        if not is_learning:
            racers = []
            for player in game.players:
                racers = [*racers, *player.racers]
            racers.sort()
            racers.reverse()
            game.draw_course(racers)
            if result:
                print(j, 'turns taken')

        r = 0
        if result:
            r = 25-j

        s3 = game.current_observation()

        if is_learning:
            RL.store_transition(s, a1, r, s2)
            RL.store_transition(s2, a2, r, s3)
            if (counter > 200) and (counter % 10 == 0):
                RL.learn()

        rAll += r
        if result:
            break

    rList.append(rAll)


if __name__ == '__main__':
    counter = 0

    for i in range(num_episodes):
        play_game(True)

        counter += 1

        if counter % 200 == 0:
            #            print('Current Table')
            #           print(RL.q_table)
            print(i + 1, 'out of', num_episodes, 'episodes completed')

    print('Score over time: ' + str(sum(rList) / num_episodes))
    print('Final Q-Table Values')
    RL.plot_cost()

