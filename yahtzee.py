import yahtzee_core

yahtzee_core.clearScreen()

print('''
  ___    ___ ________  ___  ___  _________  ________  ________  ___     
 |\  \  /  /|\   __  \|\  \|\  \|\___   ___\\\_____  \|\   __  \|\  \    
 \ \  \/  / | \  \|\  \ \  \\\\\\  \|___ \  \_|\|___/  /\ \  \|\  \ \  \   
  \ \    / / \ \   __  \ \   __  \   \ \  \     /  / /\ \   __  \ \  \  
   \/  /  /   \ \  \ \  \ \  \ \  \   \ \  \   /  /_/__\ \  \ \  \ \  \ 
 __/  / /      \ \__\ \__\ \__\ \__\   \ \__\ |\________\ \__\ \__\ \__\ 
|\___/ /        \|__|\|__|\|__|\|__|    \|__|  \|_______|\|__|\|__|\|__|
\|___|/                                                                 
''')
print("\n" * 20)
yahtzee_core.pressKeyToContinue()
                                                                        
yahtzee_core.clearScreen()
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
    print("  -",p.name())
print()
yahtzee_core.pressKeyToContinue()

dice = yahtzee_core.Dice()

for rnd in range(0,13):
    for player in players:
        dice.roll()

        again = yahtzee_core.turn(player, rnd, "First", dice)
        if again == False:
            continue

        again = yahtzee_core.turn(player, rnd, "Second", dice)
        if again == False:
            continue

        yahtzee_core.turn(player, rnd, "Third", dice)

    yahtzee_core.clearScreen()
    print(f'\nRound {rnd} scores:\n')
    yahtzee_core.printScorecard(players)
    yahtzee_core.pressKeyToContinue()
    
yahtzee_core.printWinners(yahtzee_core.getWinners(players))
