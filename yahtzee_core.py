import os
import random
import enum
import functools


class Die:
    """Holds mutable state of 6-sided die"""

    def __init__(self):
        self._value = random.randint(1,6)

    def roll(self):
        self._value = random.randint(1,6)

    def val(self):
        return self._value


class Dice:
    """Holds mutable state of 6 6-sided die"""

    def __init__(self):
        self._dice = (Die(), Die(), Die(), Die(), Die())

    def view(self):
        return tuple(map(lambda d: d.val(), self._dice))

    def freq(self):
        diceFreq = [0 for x in range(0,6)]
        for i in self.view():
            diceFreq[i - 1] += 1
        return tuple(diceFreq)

    def roll(self, *diceNums):
        if not diceNums:
            diceNums = list(range(0,5))
        for i in diceNums:
            self._dice[i].roll()


class ScoreEnum(enum.Enum):
    """Enum for indexing into scorecard list of scores"""

    ONES = 0
    TWOS = 1
    THREES = 2
    FOURS = 3
    FIVES = 4
    SIXES = 5
    THREE_OF_K = 6
    FOUR_OF_K = 7
    FULL_H = 8
    SM_STRT = 9
    LG_STRT = 10
    YAHTZEE = 11
    CHANCE = 12


class Player:
    """
    Holds player name and list of scores
    All 13 scores initialized with value -1 to indicate not yet used
    Score order: [1s, 2s, 3s, 4s, 5s, 6s, 3k, 4k, fh, ss, ls, y, ch]
    """

    def __init__(self, name):
        self._name = name
        self._scores = [-1 for x in range(0,13)]

    def total(self):
        s = list(map(lambda x: 0 if x < 0 else x, self._scores))
        return (sum(s) if sum(s[0:6]) < 63 else sum(s) + 35)

    def scores(self):
        return tuple(self._scores)

    def name(self):
        return self._name

    def setScore(self, ScoreEnum, val):
        self._scores[ScoreEnum.value] = val



def validateScore(scoreEnum, dice):
    diceFreq = dice.freq()
    flatten = list(map(lambda i: 1 if i > 0 else 0, diceFreq))

    if scoreEnum.name == 'THREE_OF_K':
        return (3 in diceFreq) or (4 in diceFreq) or (5 in diceFreq)
    elif scoreEnum.name == 'FOUR_OF_K':
        return (4 in diceFreq) or (5 in diceFreq)
    elif scoreEnum.name == 'FULL_H':
        return (3 in diceFreq) and (2 in diceFreq)
    elif scoreEnum.name == 'SM_STRT':
        return (flatten == [1, 1, 1, 1, 1, 0] or
                flatten == [0, 1, 1, 1, 1, 1] or
                flatten == [1, 1, 1, 1, 0, 0] or
                flatten == [1, 1, 1, 1, 0, 1] or
                flatten == [0, 1, 1, 1, 1, 0] or
                flatten == [0, 0, 1, 1, 1, 1] or
                flatten == [1, 0, 1, 1, 1, 1])
    elif scoreEnum.name == 'LG_STRT':
        return (flatten == [1, 1, 1, 1, 1, 0] or flatten == [0, 1, 1, 1, 1, 1])
    elif scoreEnum.name == 'YAHTZEE':
        return (5 in diceFreq)
    else:
        return True
            


def applyScore(player, scoreEnum, dice):
    if not validateScore(scoreEnum, dice):
        player.setScore(scoreEnum, 0)
    else:
        if scoreEnum.value in range(0,6):
            player.setScore(scoreEnum, sum(map(lambda x : x if x == (scoreEnum.value + 1) else 0, dice.view())))
        elif scoreEnum.name == 'FULL_H':
            player.setScore(scoreEnum, 25)
        elif scoreEnum.name == 'SM_STRT':
            player.setScore(scoreEnum, 30)
        elif scoreEnum.name == 'LG_STRT':
            player.setScore(scoreEnum, 40)
        elif scoreEnum.name == 'YAHTZEE':
            player.setScore(scoreEnum, 50)
        else:
            player.setScore(scoreEnum, sum(dice.view()))


def turn(player, rnd, turnNumber, dice):
    clearScreen()
    print()
    print(f'Round {rnd}. Player {player.name()}\'s turn:')
    print()
    printScorecard([player])

    print(f'{turnNumber} Roll: {dice.view()}')
    if turnNumber != 'Third':
        print("Roll Again? (y/n)")
        again = input("--> ").lower()
        if again == 'y':
            print("Enter dice to reroll in a space delimited list (Ex. '1 4 5'):")
            rerollVals = list(map(lambda s : int(s), input("--> ").split()))
            dice.roll(*(list(map(lambda i: i - 1, rerollVals))))
            return True
    print("What score do you want to apply your dice to?")
    print("Indicate which score using the integer key provided on the scorecard")
    print("If the dice are not valid for the requested score, you will receive a 0 in that row.")
    print("(Ex. '0' for ONES, '1' for TWOS, etc)")
    scoreKey = int(input("--> "))
    while player.scores()[scoreKey] != -1:
        print("You already have a score for", ScoreEnum(scoreKey).name)
        print("Enter a different integer to indicate a score which you have NOT already entered.")
        scoreKey = int(input("--> "))
    scoreEnum = ScoreEnum(scoreKey)
    applyScore(player, scoreEnum, dice)

    clearScreen();
    print(f'\nRound {rnd}. Player {player.name()} results:\n')
    printScorecard([player])
    input("Press any key to continue...")

    return False


def printScorecard(players):
    print()
    print("*" * 70)
    print('                    ', end='')
    playerNames = list(map(lambda p: p.name(), players))
    for name in playerNames:
        print(f'{name:12} ', end='')
    print('\n')
    for scoreEnum in ScoreEnum:
        print(f'({scoreEnum.value:2}) {scoreEnum.name:10}  :  ', end='')
        for player in players:
            scoreVal = player.scores()[scoreEnum.value] if player.scores()[scoreEnum.value] >= 0 else "__"
            print(f'{scoreVal:<13}', end='')
        print()
    print('\n     TOTAL       :  ', end='')
    for player in players:
        print(f'{player.total():<13}', end='')
    print()
    print("*" * 70)
    print()


def getWinners(players):
    winners = [players[0]]
    for player in players[1:]:
        if player.total() > winners[0].total():
            winners = [player]
        elif player.total() == winner.total():
            winners.append(player)
    return winners

def printWinners(winners):
    if len(winners) > 1:
        print("It's a tie! Out winners are:")
        for winner in winners:
            print(f'  - {winner.name()}')
    else:
        print(f'Our winner is... {winners[0].name()}!')

def clearScreen():
    os.system('clear') if os.name == 'posix' else os.system('cls')

def pressKeyToContinue():
    input("Press any key to continue...")
