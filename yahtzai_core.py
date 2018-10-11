import os
import random
import enum
import functools
import time
import yahtzai_dumb_ai
import yahtzai_less_dumb_ai
import yahtzai_random_ai


class Die:
    """Holds mutable state of 6-sided die"""

    def __init__(self):
        self._value = random.randint(1,6)

    def roll(self):
        self._value = random.randint(1,6)

    def val(self):
        return self._value


class Dice:
    """Holds mutable state of 5 6-sided die"""

    def __init__(self):
        self._dice = (Die(), Die(), Die(), Die(), Die())

    
    def view(self):
        """Returns state of 5 die as 5-tuple of ints"""
        return tuple(map(lambda d: d.val(), self._dice))

    def freq(self):
        """Returns 6-tuple with frequency of each dice from current state"""
        diceFreq = [0 for x in range(0,6)]
        for i in self.view():
            diceFreq[i - 1] += 1
        return tuple(diceFreq)

    def flatten(self):
        """Maps frequency tuple to 1's for positive values, 0 stays 0
           Useful for detecting straights"""
        return tuple(map(lambda i: 1 if i > 0 else 0, self.freq()))


    def roll(self, *diceNums):
        """With no args, reroll all. Else roll dice nums given in int list
            diceNums is indexed starting at 1 (ex [1,3,5])"""
        if not diceNums:
            diceNums = list(range(0,5))
        for i in diceNums:
            self._dice[i - 1].roll()



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
    Also holds set of "remaining plays".
    """

    def __init__(self, name, playerType):
        self._name = name
        self._scores = [-1 for x in range(0,13)]
        self._type = playerType
        self._remainingPlays = [ScoreEnum(x) for x in range(0,13)]
        self._playerId = int(time.time() * 1000000)

    def total(self):
        # Maps any -1 scores to 0 before totaling
        s = list(map(lambda x: 0 if x < 0 else x, self._scores))
        # Returns sum of map. Includes 35 bonus calculation if upper section >= 63
        return (sum(s) if sum(s[0:6]) < 63 else sum(s) + 35)

    def scores(self):
        return tuple(self._scores)

    def name(self):
        return self._name

    def setScore(self, ScoreEnum, val):
        self._scores[ScoreEnum.value] = val

    def type(self):
        return self._type

    def removeFromRemaining(self, i):
        self._remainingPlays.remove(i)

    def remainingPlays(self):
        return self._remainingPlays

    def playerId(self):
        return self._playerId


def validateScore(scoreEnum, dice):
    """
    Given a scoreEnum and 5 dice, validates whether dice meet scoring condition.
    If dice meet condition, return True. Else return False.
    For scoreEnums with no condition (Ex. CHANCE) True is returned.
    """
    
    diceFreq = dice.freq()
    flatten = dice.flatten()

    if scoreEnum.name == 'THREE_OF_K':
        return (3 in diceFreq) or (4 in diceFreq) or (5 in diceFreq)
    elif scoreEnum.name == 'FOUR_OF_K':
        return (4 in diceFreq) or (5 in diceFreq)
    elif scoreEnum.name == 'FULL_H':
        return (3 in diceFreq) and (2 in diceFreq)
    elif scoreEnum.name == 'SM_STRT':
        return (flatten == (1, 1, 1, 1, 1, 0) or
                flatten == (0, 1, 1, 1, 1, 1) or
                flatten == (1, 1, 1, 1, 0, 0) or
                flatten == (1, 1, 1, 1, 0, 1) or
                flatten == (0, 1, 1, 1, 1, 0) or
                flatten == (0, 0, 1, 1, 1, 1) or
                flatten == (1, 0, 1, 1, 1, 1))
    elif scoreEnum.name == 'LG_STRT':
        return (flatten == (1, 1, 1, 1, 1, 0) or flatten == (0, 1, 1, 1, 1, 1))
    elif scoreEnum.name == 'YAHTZEE':
        return (5 in diceFreq)
    else:
        return True
            


def applyScore(player, scoreEnum, dice):
    """
    Given player, scoreEnum, and dice, assigns score to player
    """

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
    player.removeFromRemaining(scoreEnum)


def interactiveTurn(player, rnd, turnNumber, dice):
    turnNumberString = "First" if turnNumber == 0 else "Second" if turnNumber == 1 else "Third"
    clearScreen()
    print(f'\nRound {rnd + 1} -- {player.name()}\'s turn:\n')
    printScorecard([player])
    print(f'{turnNumberString} Roll: {dice.view()}')

    if turnNumber < 2:
        while True:
            print("Roll Again? (y/n)")
            again = input("--> ").lower()
            if again == 'y':
                while True:
                    try:
                        print("Enter dice to reroll in a space delimited list (Ex. '1 4 5'):")
                        rerollVals = list(map(lambda s : int(s), input("--> ").split()))
                        return ('y', rerollVals)
                    except:
                        print("\nONLY INTEGERS! 1 - 5. (Or press enter to reroll all dice)")
            elif again == 'n':
                print()
                break
            else:
                print("Enter 'y' or 'n' !\n")



    print("What score do you want to apply your dice to?")
    print("Indicate which score using the integer key provided on the scorecard")
    print("If the dice are not valid for the requested score, you will receive a 0 in that row.")
    print("(Ex. '0' for ONES, '1' for TWOS, etc)")
    
    while True:
        try:
            scoreKey = int(input("--> "))
            while player.scores()[scoreKey] != -1:
                print(f'\nYou already have a score for {ScoreEnum(scoreKey).name}!')
                print("Enter a different integer to indicate a score which you have NOT already entered.")
                scoreKey = int(input("--> "))
            return ('n', ScoreEnum(scoreKey))
        except:
            print("\nEnter an INTEGER! 0 - 12.")



def turn(player, rnd, turnNumber, dice):
    """
    Delegates logic of each turn to other functions based on player type.
    Humans given interactive path. AIs directed to AI automated path.
    BOTH INTERACTIVE AND AUTOMATED AI PATH RETURN SAME 'DECISION' INTERFACE.
        Either: ('n', scoreEnum)      -- "No, don't roll again, apply this score"
        or:     ('y', [dice num list] -- "Yes, roll again, with this list of dice"
    """

    if player.type() == 'human':
        decision = interactiveTurn(player, rnd, turnNumber, dice)
    elif player.type() == 'ai-dumb':
        decision = yahtzai_dumb_ai.ai_engine(player, rnd, turnNumber, dice)
    elif player.type() == 'ai-less-dumb':
        decision = yahtzai_less_dumb_ai.ai_engine(player, rnd, turnNumber, dice)
    elif player.type() == 'ai-random':
        decision = yahtzai_random_ai.ai_engine(player, rnd, turnNumber, dice)

    # LOG GAME PLAY -- comma separated values for each turn, newline separating turns
    # LOG SYNTAX:  playerName, type, id, scores, roundNumber, turnNumber, dice, decision, returnVal
    # EXAMPLE:     player1, human, 2314123.12341, (-1, -1, 6, ...), 4, 2, (2, 2, 2, 3, 3), n, ScoreEnum.FULL_H
    with open('gamelog', 'a+') as f:
        f.write(f'{player.name()},{player.type()},{player.playerId()},')
        f.write(f'{"(" + ",".join(str(i) for i in player.scores()) + ")"},')
        f.write(f'{rnd},{turnNumber},{"(" + ",".join(str(i) for i in dice.view()) + ")"},')
        f.write(f'{decision[0]},{decision[1]}\n')

    if (decision[0] == 'n'):
        applyScore(player, decision[1], dice)

        if (player.type() == 'human'):
            clearScreen()
            print(f'\nRound {rnd}. Player {player.name()} results:\n')
            printScorecard([player])
            pressEnterToContinue()

        return False
    else:
        dice.roll(*decision[1])
        return True



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
        elif player.total() == winners[0].total():
            winners.append(player)
    return winners

def printWinners(players):
    winners = getWinners(players)
    clearScreen()
    print("\nFinal scores:\n")
    printScorecard(players)
    print()
    if len(winners) > 1:
        print("It's a tie! Out winners are:")
        for winner in winners:
            print(f'  - {winner.name()}')
    else:
        print(f'Our winner is... {winners[0].name()}, with a score of {winners[0].total()}!')
    print("\nGoodbye!\n")

def clearScreen():
    os.system('clear') if os.name == 'posix' else os.system('cls')

def pressEnterToContinue():
    input("Press enter to continue...")
