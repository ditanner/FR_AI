import game
import numpy as np
import tensorflow as tf

from TensorNet import DeepQNetwork

print('TensorNet, 2 player game, R then S')

initial_cards = 7
max_recycle_deck = 7
cards_in_hand = 4
position = 1
on_right = 1
next_move = 1
qr_observation_count = (initial_cards + max_recycle_deck + cards_in_hand + position + on_right + next_move) * 4


num_episodes = 10000

# reward list
rList = []

RL = DeepQNetwork(n_actions=4, n_features=qr_observation_count,
                  learning_rate=0.01,
                  reward_decay=0.9,
                  e_greedy=0.9,
                  replace_target_iter=20,
                  memory_size=200000,
                  # output_graph=True
                  )

def play_racer_RL(racer, is_learning):
    racer.draw_hand()
    s = game.current_observation()
    a1 = RL.choose_action(s)
    while not racer.is_valid_move(a1):
#        RL.store_transition(s, a1, -0.1, s)
        a1 = RL.choose_action(s)

    racer.select_move(a1)
    if not is_learning:
        game.print_cards_for_racer(racer)

    return s, a1

def play_racer_max(racer):
    racer.draw_hand()
    racer.select_move(len(racer.hand_selection)-1)


def play_game(is_learning):
    game.setup(2)

    if not is_learning:
        racers = []
        for player in game.players:
            racers = [*racers, *player.racers]
        racers.sort()
        racers.reverse()
        game.draw_course(racers)


    rAll = 0
    d = False
    j = 0

    race_timer = 0
    is_race_over = False

    while j < 99:
        j += 1

        s, a1 = play_racer_RL(game.players[0].racers[1], is_learning)

        s2, a2 = play_racer_RL(game.players[0].racers[0], is_learning)

        play_racer_max(game.players[1].racers[0])
        play_racer_max(game.players[1].racers[1])

        if not is_learning:
            game.print_cards_for_racer(game.players[1].racers[1])
            game.print_cards_for_racer(game.players[1].racers[0])


        result = game.make_move()

        if not is_learning:
            racers = []
            for player in game.players:
                racers = [*racers, *player.racers]
            racers.sort()
            racers.reverse()
            game.draw_course(racers)
            if result:
                print(result.name, ' won,', j, 'turns taken')


        r = 0
        if result and (result == game.players[0].racers[0] or result == game.players[0].racers[1]):
            r = 1
        elif result:
            r = -1

        s3 = game.current_observation()

        if is_learning:
            RL.store_transition(s, a1, r, s2)
            RL.store_transition(s2, a2, r, s3)
            if (counter > 500) and (counter % 10 == 0):
                RL.learn()

        rAll += r
        if result:
            break

    if rAll == 0:
        racers = []
        for player in game.players:
            racers = [*racers, *player.racers]
        racers.sort()
        racers.reverse()
        game.print_cards()
        game.draw_course(racers)
        print(j)
        print()
        pass

    rList.append(rAll)

def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


if __name__ == '__main__':
    counter = 0

    for i in range(num_episodes):
        play_game(True)

        counter += 1

        if counter % 200 == 0:
            #            print('Current Table')
            #           print(RL.q_table)
            print(i + 1, 'out of', num_episodes, 'episodes completed')

    RL.plot_cost()
    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(np.arange(len(rList)), rList)
#    ax.yaxis.label = 'Result'
#    ax.xaxis.label = 'episode'

    plt.ion()
    plt.show()

    lines = ax.plot(np.arange(len(rList)-19), moving_average(rList, 20), 'r-', lw=1)
    print('Score over time: ' + str(sum(rList) / num_episodes))
    plt.pause(0.1)


