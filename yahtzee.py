import yahtzee_core


print("How many human players?");
humanPlayersCount = int(input("--> "));
print()

print("How many AI nemeses?");
aiPlayersCount = int(input("--> "));
print()

players = []

for p in range(0, humanPlayersCount):
    print(f'Player {p + 1} name:')
    name = input("--> ")
    players.append(yahtzee_core.Player(name))
    print()

for p in range(1, aiPlayersCount + 1):
    players.append(yahtzee_core.Player(f'AI Player {p}'))

print("\nAll set! Our players are:")
for p in players:
    print(p.name())
print()

dice = yahtzee_core.Dice()

for rnd in range(0,13):
    for player in players:
        print()
        yahtzee_core.printScorecard([player])
        print()
        dice.roll()

        again = yahtzee_core.turn(player, "First", dice)
        if again == False:
            yahtzee_core.printScorecard([player])
            break

        again = yahtzee_core.turn(player, "Second", dice)
        if again == False:
            yahtzee_core.printScorecard([player])
            break

        yahtzee_core.turn(player, "Third", dice)
        yahtzee_core.printScorecard([player])

    print()
    print(f'Round {rnd} scores:\n')
    yahtzee_core.printScorecard(players)

