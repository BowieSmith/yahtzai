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
        humanPlayersCount = int(input("--> "))
        break
    except ValueError:
        print("Enter an INTEGER!\n")
print()

while True:
    try:
        print("How many AI nemeses?");
        aiPlayersCount = int(input("--> "))
        break
    except ValueError:
        print("Enter an INTEGER!\n")
print()

while True:
    try:
        print("How many rounds? (Pressing enter gives a standard 13-round yahtzee game)");
        totalRounds = input("--> ")
        if (totalRounds == ""):
            totalRounds = 13
        else:
            totalRounds = int(totalRounds)
            if (totalRounds < 2 or totalRounds > 13):
                print("Enter an integer between 1 and 13!")
                continue
        break
    except ValueError:
        print("Enter an INTEGER!\n")
print()

players = []

for p in range(0, humanPlayersCount):
    print(f'Player {p + 1} name:')
    name = input("--> ")
    players.append(yahtzai_core.Player(name, 'human', gameSize=totalRounds))
    print()

# The second argument to Player constructor determines which AI Engine to use
for p in range(1, aiPlayersCount + 1):
    players.append(yahtzai_core.Player(f'AI Player {p}', 'ai-less-dumb', gameSize=totalRounds))

if humanPlayersCount != 0:
    automatePlay = 'n'
else:
    while True:
        print("Automate gameplay? (y/n)");
        automatePlay = input("--> ").lower()
        if (automatePlay != 'y' and automatePlay != 'n'):
            print("Enter 'y' or 'n'!\n")
        else:
            break

if automatePlay == 'n':
    print("\nAll set! Our players are:")
    for p in players:
        print("  -",p.name())
    print()
    yahtzai_core.pressEnterToContinue()
else:
    print("\nQuiet please. The AI is thinking...\n")

dice = yahtzai_core.Dice()

# Main game loop
# 13 rounds. Each play gets up to three rolls each round.
for rnd in range(0, len(players[0].scores())):
    for player in players:
        dice.roll()
        for turnNo in range(0,3):
            rollAgain = yahtzai_core.turn(player, rnd, turnNo, dice)
            if not rollAgain:
                break

        if (automatePlay == 'n'):
            yahtzai_core.clearScreen()
            print(f'\nRound {rnd + 1} scores:\n')
            yahtzai_core.printScorecard(players)
            yahtzai_core.pressEnterToContinue()
    
yahtzai_core.printWinners(players, humanPlayersCount)
