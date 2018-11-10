import yahtzai_core as yc
import yahtzai_rl_ai as rl
import sys

yc.clearScreen()

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
yc.pressEnterToContinue()
                                                                        
yc.clearScreen()
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

if (aiPlayersCount > 0):
    while True:
        try:
            print("Choose an AI (enter integer):")
            print(" (1) Random AI (easy)")
            print(" (2) Expert System AI (medium)")
            print(" (3) Reinforcement Learning AI (hard)")
            aiNumber = int(input("--> "))
            if (aiNumber < 1 or aiNumber > 3):
                print("Enter an integer between 1 and 3!")
                continue
            aiType = 'ai-random' if aiNumber == 1 else 'ai-less-dumb' if aiNumber == 2 else 'ai-rl'
            break
        except ValueError:
            print("Enter an INTEGER!\n")

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
    players.append(yc.Player(name, 'human', gameSize=totalRounds))
    print()

# The second argument to Player constructor determines which AI Engine to use
actionTable = {}
if (aiType == 'ai-rl'):
    try:
        actionTable = rl.loadActionTable('at' + str(totalRounds) + '.p')
    except Exception:
        print(f'Action table "at{str(totalRounds)}.p" does not exist')
        sys.exit()

for p in range(1, aiPlayersCount + 1):
    players.append(yc.Player(f'AI Player {p}', aiType, gameSize=totalRounds))

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
    yc.pressEnterToContinue()
else:
    print("\nQuiet please. The AI is thinking...\n")

dice = yc.Dice()

# Main game loop
# 13 rounds. Each play gets up to three rolls each round.
for rnd in range(0, len(players[0].scores())):
    for player in players:
        dice.roll()
        for turnNo in range(0,3):
            rollAgain = yc.turn(player, rnd, turnNo, dice, actionTable, totalRounds)
            if not rollAgain:
                break

        if (automatePlay == 'n'):
            yc.clearScreen()
            print(f'\nRound {rnd + 1} scores:\n')
            yc.printScorecard(players)
            yc.pressEnterToContinue()
    
yc.printWinners(players, humanPlayersCount)
