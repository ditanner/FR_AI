import game
import numpy as np

print('Q-Table, 1 player game, R then S')

initial_cards = 15
max_recycle_deck = 15
cards_in_hand = 4
position = 1
on_right = 1
next_move = 1
qr_observation_count = (initial_cards + max_recycle_deck + cards_in_hand + position + on_right + next_move) * 2

# Init tables with all zeros
Q = np.zeros([qr_observation_count, 4])

lr = 0.8
y = 0.95
num_episodes = 2000

# reward list
rList = []

for i in range(num_episodes):
    game.setup(1)

    rAll = 0
    d = False
    j = 0

    race_timer = 0
    is_race_over = False

    game.players[0].racers[1].draw_hand()

    while j < 99:
        j += 1
        # choose an action by greedily (with noise) picking from Q table
        s = game.current_observation()
        a1 = np.argmax(Q[s, :] + np.random.randn(1, 4) * (1. / (i + 1)))
        game.players[0].racers[1].select_move(a1)

        game.players[0].racers[0].draw_hand()
        s2 = game.current_observation()
        a2 = np.argmax(Q[s2, :] + np.random.randn(1, 4) * (1. / (i + 1)))
        game.players[0].racers[0].select_move(a2)

        result = game.make_move()
        r = 0
        if result:
            r = 1

        game.players[0].racers[1].draw_hand()
        s3 = game.current_observation()

        Q[s,a1] = Q[s,a1] + lr*(r+y*np.max(Q[s3,:]) - Q[s,a1])
        Q[s2,a2] = Q[s2,a2] + lr*(r+y*np.max(Q[s3,:]) - Q[s2,a2])
        rAll += r
        if result:
            break
    rList.append(rAll)

print ('Score over time: ' + str(sum(rList) / num_episodes))
print ('Final Q-Table Values')
print (Q)