import os
import random
import enum
import functools
import time
import yahtzai_dumb_ai
import yahtzai_less_dumb_ai
import yahtzai_random_ai
import yahtzai_rl_ai


class Dice:
    """Holds state of 5 6-sided die"""

    def __init__(self, diceString=''):
        if (len(diceString) != 5):
            diceList = []
            for i in range(0,5):
                diceList.append(random.randint(1,6))
        else:
            diceList = [int(i) for i in list(diceString)]
        self._dice = Dice.normalize(diceList)
    
    def view(self):
        """Returns state of 5 die as 5-tuple of ints"""
        return tuple(self._dice)

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
            self._dice[i - 1] = random.randint(1,6);
        self._dice = Dice.normalize(self._dice)

    def asString(self):
        return ''.join([str(d) for d in self.view()])
    
    @staticmethod
    def normalize(dice):
        """View dice in normalized form"""
        normalized = []
        for i in range(1,7):
            for d in dice:
                if (d == i):
                    normalized.append(d)
        return normalized


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

    # playerType is used to control gameplay. "human" for interactive play.
    #   "aiTypeName" for given AI type. See documentation in yahtzai.py
    # gameSize controls size of game. 13 rounds for standard yahtzee game.
    #   Can choose 6 for "small" game, using only 1s,2s,3s,4s,5s,6s as scoring options.
    def __init__(self, name, playerType, gameSize=13):
        self._name = name
        self._scores = [-1 for _ in range(0,gameSize)]
        self._type = playerType
        self._remainingPlays = [ScoreEnum(x) for x in range(0,gameSize)]
        self._playerId = int(time.time() * 1000000)

    def total(self):
        # Maps any -1 scores to 0 before totaling
        s = [0 if x < 0 else x for x in self._scores]
        # Returns sum of map. Includes 35 bonus calculation if upper section >= 63
        return (sum(s) if sum(s[0:6]) < 63 else sum(s) + 35)

    def scores(self):
        return tuple(self._scores)

    def playedMovesBitString(self):
        return "".join(["1" if i >= 0 else "0" for i in self.scores()])

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
            


def getScoreGivenDice(scoreEnum, dice):
    """
    Given scoreEnum and dice, return score value when dice applied to scoreEnum
    """

    if not validateScore(scoreEnum, dice):
        return 0
    else:
        if scoreEnum.value in range(0,6):
            return sum(map(lambda x : x if x == (scoreEnum.value + 1) else 0, dice.view()))
        elif scoreEnum.name == 'FULL_H':
            return 25
        elif scoreEnum.name == 'SM_STRT':
            return 30
        elif scoreEnum.name == 'LG_STRT':
            return 40
        elif scoreEnum.name == 'YAHTZEE':
            return 50
        else:
            return sum(dice.view())



def applyScore(player, scoreEnum, dice):
    """
    Given player, scoreEnum, and dice, assigns score to player
    """

    player.setScore(scoreEnum, getScoreGivenDice(scoreEnum, dice))
    player.removeFromRemaining(scoreEnum)



# Turn Path for human players (requiring terminal I/O)
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
                        for value in rerollVals:
                            if value < 1 or value > 5:
                                raise ValueError("Reroll values must be 1, 2, 3, 4, or 5")
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
            print(f'\nEnter an INTEGER! 0 - {len(player.scores())}.')



def turn(player, rnd, turnNumber, dice, actionTable, gameSize):
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
    elif player.type() == 'ai-rl':
        decision = yahtzai_rl_ai.ai_engine(player, rnd, turnNumber, dice, actionTable, gameSize)

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

        return False #Indicating to NOT roll again
    else:
        dice.roll(*decision[1])
        return True  #Indicating to roll again



def printScorecard(players):
    print()
    print("*" * 70)
    print('                    ', end='')
    playerNames = list(map(lambda p: p.name(), players))
    for name in playerNames:
        print(f'{name:12} ', end='')
    print('\n')
    for scoreEnum in (ScoreEnum(i) for i in range(0, len(players[0].scores()))):
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


# Calculate winners (may be multiple in list if tie)
def getWinners(players):
    winners = [players[0]]
    for player in players[1:]:
        if player.total() > winners[0].total():
            winners = [player]
        elif player.total() == winners[0].total():
            winners.append(player)
    return winners

def printWinners(players, humanPlayersCount):
    winners = getWinners(players)
    clearScreen()
    print("\nFinal scores:\n")
    printScorecard(players)
    print()
    if len(winners) > 1:
        print("It's a tie! Out winners are:")
        for winner in winners:
            print(f'  - {winner.name()}')
        print(f'With a score of {winners[0].total()}')
    else:
        print(f'Our winner is... {winners[0].name()}, with a score of {winners[0].total()}!')
    if humanPlayersCount == 0:
        print(f'\nThe average score of the AI is... {sum(player.total() for player in players) / len(players)}\n')
    print("\nGoodbye!\n")

def clearScreen():
    os.system('clear') if os.name == 'posix' else os.system('cls')

def pressEnterToContinue():
    input("Press enter to continue...")
