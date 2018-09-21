import yahtzai_core

yahtzai_core.clearScreen()

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
yahtzai_core.pressEnterToContinue()
                                                                        
yahtzai_core.clearScreen()
while True:
    try:
        print("How many human players?");
        humanPlayersCount = int(input("--> "));
        break
    except ValueError:
        print("Enter an INTEGER!\n")
print()

while True:
    try:
        print("How many AI nemeses?");
        aiPlayersCount = int(input("--> "));
        break
    except ValueError:
        print("Enter an INTEGER!\n")
print()

players = []

for p in range(0, humanPlayersCount):
    print(f'Player {p + 1} name:')
    name = input("--> ")
    players.append(yahtzai_core.Player(name, 'human'))
    print()

# The second argument to Player constructor determines which AI Engine to use
for p in range(1, aiPlayersCount + 1):
    players.append(yahtzai_core.Player(f'AI Player {p}', 'ai-random'))

print("\nAll set! Our players are:")
for p in players:
    print("  -",p.name())
print()
yahtzai_core.pressEnterToContinue()

dice = yahtzai_core.Dice()

# Main game loop
# 13 rounds. Each play gets up to three rolls each round.
for rnd in range(0,13):
    for player in players:
        dice.roll()
        for turnNo in range(0,3):
            rollAgain = yahtzai_core.turn(player, rnd, turnNo, dice)
            if not rollAgain:
                break

    yahtzai_core.clearScreen()
    print(f'\nRound {rnd + 1} scores:\n')
    yahtzai_core.printScorecard(players)

    # comment this out and set 0 humans to n AI for automatic play
    yahtzai_core.pressEnterToContinue()
    
yahtzai_core.printWinners(players)
