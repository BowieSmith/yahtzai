import yahtzai_core as yc
import itertools
import random
import pickle

def ai_engine(player, rnd, turnNumber, dice, actionTable, gameSize):
    if (turnNumber < 2):
        action = pickAction(actionTable,
                playedMovesBitStringToInt(player.playedMovesBitString()), dice.asString())
        return ('y', actionIntToRerollList(action))

    scoreValues = [scoreFunction(dice.asString(), yc.ScoreEnum(i)) for i in range(0, gameSize)]
    for idx,val in enumerate(player.playedMovesBitString()):
        if val == '1':
            scoreValues[idx] = -100
    maxScoreValueIndex = scoreValues.index(max(scoreValues))
    return ('n', yc.ScoreEnum(maxScoreValueIndex))

def initializeActionTable(gameSize):
    actionDict = {}
    for playedMoves in range(0, 2 ** gameSize):
        for diceCombination in itertools.combinations_with_replacement("123456", 5):
            for action in range(0, 2**5):
                actionDict[(playedMoves, ''.join(diceCombination), action)] = (0,0,0)
    return actionDict

def actionIntToRerollList(action):
    diceToReroll = []
    for idx,val in enumerate(list(bin(action)[2:].zfill(5))):
        if (val == '1'):
            diceToReroll.append(idx + 1)
    return diceToReroll
    
def diceAfterAction(diceString, action):
    dice = yc.Dice(diceString)
    diceToReroll = actionIntToRerollList(action)
    if len(diceToReroll) != 0:
        dice.roll(*diceToReroll)
    return dice.asString()

def scoreAction(playedMovesBitString, prevDiceString, nextDiceString):
    maxPrevScore = 0
    maxNextScore = 0
    for idx,played in enumerate(playedMovesBitString):
        maxPrevScore = max(maxPrevScore, -10 if played == '1' else scoreFunction(prevDiceString, yc.ScoreEnum(idx))) 
        maxNextScore = max(maxNextScore, -10 if played == '1' else scoreFunction(nextDiceString, yc.ScoreEnum(idx)))
    return maxNextScore - maxPrevScore

def scoreFunction(diceString, scoreEnum):
    bonusBias = 1.666666        # boost top scores to reflect bonus
    chanceBias = -10            # reduce appeal of chance (save for no other options)
    dice = yc.Dice(diceString)
    if (scoreEnum.value < 6):
        return yc.getScoreGivenDice(scoreEnum, dice) + (bonusBias * (scoreEnum.value + 1))
    if (scoreEnum == yc.ScoreEnum.CHANCE):
        return yc.getScoreGivenDice(scoreEnum, dice) + chanceBias
    return yc.getScoreGivenDice(scoreEnum, dice)

def playedMovesIntToBitString(playedMovesInt, gameSize):
    return bin(playedMovesInt)[2:].zfill(gameSize)

def playedMovesBitStringToInt(playedMovesBitString):
    return int('0b' + playedMovesBitString, 2)

def trial(actionTable, playedMoves, diceString, action, gameSize):
    prevDiceString = diceString
    nextDiceString = diceAfterAction(prevDiceString, action)
    score = scoreAction(playedMovesIntToBitString(playedMoves,gameSize), prevDiceString, nextDiceString)
    oldActionTableValue = actionTable[(playedMoves, diceString, action)]
    newSum = oldActionTableValue[0] + score
    newTotalGames = oldActionTableValue[1] + 1
    newAvg = newSum / newTotalGames
    actionTable[(playedMoves, diceString, action)] = (newSum, newTotalGames, newAvg)

def randomTrial(actionTable, gameSize):
    randomPlayedMoves = random.randint(0, 2**gameSize - 1)
    randomAction = random.randint(0, 2**5 - 1)
    randomDiceString = yc.Dice().asString()
    trial(actionTable, randomPlayedMoves, randomDiceString, randomAction, gameSize)
    return (randomPlayedMoves, randomDiceString, randomAction)

def pickAction(actionTable, playedMoves, diceString):
    maxAvg = -100
    bestAction = 0
    for action in range(0,32):
        tableEntry = actionTable[(playedMoves, diceString, action)]
        if (tableEntry[2] > maxAvg):
            maxAvg = tableEntry[2]
            bestAction = action
    return bestAction

def trainActionTable(actionTable, gameSize, numberTrials):
    for _ in range(0, numberTrials):
        randomTrial(actionTable, gameSize)

def saveActionTable(actionTable, name):
    with open(name, 'wb') as pfile:
        pickle.dump(actionTable, pfile)

def loadActionTable(name):
    with open(name, 'rb') as pfile:
        return pickle.load(pfile)
