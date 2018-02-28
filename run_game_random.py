import game

print('Random selection, 2 player game')

game.setup(2)
counter = 0
race_timer = 0
race_over = False
while not race_over:
    if counter == 5:
        counter = 0
        game.print_cards()

    for player in game.players:
        for racer in player.racers:
            racer.draw_hand()
            racer.select_move(0)

    race_over = game.make_move()
    print('Next Round')
    counter += 1
    race_timer += 1
    # sleep(2)

game.print_cards()
print('Finished in', race_timer, 'turns')
