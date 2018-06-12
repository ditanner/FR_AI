import game as g
import numpy as np
import tensorflow as tf

#from TensorNet import DeepQNetwork
#from PolicyGradient import PolicyGradient
from PrioritisedDQN import DQNPrioritizedReplay

print('TensorNet, 1 player game, R then S, scenario 2')

initial_cards = 7
max_recycle_deck = 7
cards_in_hand = 4
position = 1
on_right = 1
next_move = 1
num_players = 1
qr_observation_count = (initial_cards + max_recycle_deck + cards_in_hand + position + on_right + next_move) * (2 * num_players)
#qr_observation_count = (position + on_right + next_move) * (2 * num_players)
game = g.Game()

num_episodes = 30000


MEMORY_SIZE = 10000

RL = DQNPrioritizedReplay(
        n_actions=4, n_features=qr_observation_count, memory_size=MEMORY_SIZE,
        e_greedy_increment=0.00005, sess=None, prioritized=True, output_graph=True,
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
    racer.select_move(len(racer.hand_selection) - 1)


def train_game(rList):
    game.setup(1, starting_distance=18, training_scenario=2)

    run_game(True, rList, True)

def play_game(is_learning, rList, use_RL=True):
    game.setup(1, starting_distance=18, training_scenario=2)
    run_game(is_learning, rList, use_RL)

def run_game(is_learning, rList, use_RL=True):
    global counter
    if 'counter' not in globals():
        counter = 0

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

        if use_RL:
            s, a1 = play_racer_RL(game.players[0].racers[1], is_learning)
            s2, a2 = play_racer_RL(game.players[0].racers[0], is_learning)
        else:
            play_racer_max(game.players[0].racers[0])
            play_racer_max(game.players[0].racers[1])

        if not is_learning and num_players > 1:
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
            if j==3:
                r=1
            else:
                r = 3 - j
        elif result:
            r = -1

        s3 = game.current_observation()

        if is_learning and use_RL:
            RL.store_transition(s, a1, r, s3)
            RL.store_transition(s2, a2, r, s3)
#            RL.store_transition(s, a1, r)
#            RL.store_transition(s2, a2, r)
            if (counter > MEMORY_SIZE): # and (counter % 10 == 0):
                RL.learn()
                #pass

        counter += 1
        rAll += r
        if result:
            break

    # if rAll == 0:
    #     racers = []
    #     for player in game.players:
    #         racers = [*racers, *player.racers]
    #     racers.sort()
    #     racers.reverse()
    #     game.print_cards()
    #     game.draw_course(racers)
    #     print(j)
    #     print()
    #     pass

    rList.append(rAll)


def moving_average(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n



# def train(RL):
#     total_steps = 0
#     steps = []
#     episodes = []
#     for i_episode in range(20):
#         observation = env.reset()
#         while True:
#             # env.render()
#
#             action = RL.choose_action(observation)
#
#             observation_, reward, done, info = env.step(action)
#
#             if done: reward = 10
#
#             RL.store_transition(observation, action, reward, observation_)
#
#             if total_steps > MEMORY_SIZE:
#                 RL.learn()
#
#             if done:
#                 print('episode ', i_episode, ' finished')
#                 steps.append(total_steps)
#                 episodes.append(i_episode)
#                 break
#
#             observation = observation_
#             total_steps += 1
#     return np.vstack((episodes, steps))



if __name__ == '__main__':
    counter = 0
    r_list = []
    r_m_list = []
    for i in range(num_episodes):
        train_game(r_list)
#        play_game(True, r_m_list, use_RL=False)


        if i % 1000 == 0:
            #            print('Current Table')
            #           print(RL.q_table)
            print(i + 1, 'out of', num_episodes, 'episodes completed')

#    RL.plot_cost()
    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(np.arange(len(r_list)), r_list)
    #    ax.yaxis.label = 'Result'
    #    ax.xaxis.label = 'episode'

    plt.ion()
    plt.show()
    mov_ave_cnt = 50

    lines = ax.plot(np.arange(len(r_list) - (mov_ave_cnt-1)), moving_average(r_list, mov_ave_cnt), 'r-', lw=1)
 #   lines = ax.plot(np.arange(len(r_m_list) - (mov_ave_cnt-1)), moving_average(r_m_list, mov_ave_cnt), 'g-', lw=1)
    print('Score over time: ' + str(sum(r_list) / num_episodes))
    plt.pause(0.1)
