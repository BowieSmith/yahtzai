import yahtzai_core as yc
import itertools

def ai_engine(player, rnd, turnNumber, dice):
    playedMovesBitString = player.playedMovesAsInt()
    playedMovesAsInt = int('0b' + playedMovesBitString, 2)

    diceStateAsString = dice.asString()

def initializeActionTable(numberPossibleMoves=6):
    actionDict = {}
    for playedMoves in range(0, 2 ** numberPossibleMoves):
        for diceCombination in itertools.combinations_with_replacement("123456", 5):
            for action in range(0, 2**5):
                actionDict[(playedMoves, ''.join(diceCombination), action)] = (0,0,0)
    return actionDict

def evaluateAction(diceString, action):
    dice = yc.Dice(diceString)
    actionString = bin(action)[2:].zfill(5)
    diceToReroll = []
    for idx,val in enumerate(list(actionString)):
        if (val == '1'):
            diceToReroll.append(idx + 1)
    dice.roll(*diceToReroll)
    return dice.asString()

def scoreAction(playedMovesBitString, prevDiceString, action, nextDiceString):

def scoreFunction(diceString, scoreEnum):
    bonusBias = 1.666666        # to boost top scores to reflect bonus
    fourOfKindBias = 10         # to boost fourOfKind over threeOfKind (since 4k is valid 3k)
    dice = yc.Dice(diceString)
    if (scoreEnum.value < 6):
        return yc.getScoreGivenDice(scoreEnum, dice) + (bonusBias * scoreEnum.value)
    if (scoreEnum == yc.ScoreEnum.FOUR_OF_K):
        return yc.getScoreGivenDice(scoreEnum, dice) + fourOfKindBias
