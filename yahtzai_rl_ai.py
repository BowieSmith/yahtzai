import yahtzai_core as yc
import itertools
import random
import pickle

# Reinforcement Learning AI interface
def ai_engine(player, rnd, turnNumber, dice, actionTable, gameSize):
    # Choose re-roll action if both re-rolls have not been used
    if (turnNumber < 2):
        action = pickAction(actionTable,
                playedMovesBitStringToInt(player.playedMovesBitString()), dice.asString())
        return ('y', actionIntToRerollList(action))

    # Choose best action if both re-rolls have been used
    scoreValues = [scoreFunction(dice.asString(), yc.ScoreEnum(i)) for i in range(0, gameSize)]
    for idx,val in enumerate(player.playedMovesBitString()):
        if val == '1':
            scoreValues[idx] = -100
    maxScoreValueIndex = scoreValues.index(max(scoreValues))
    return ('n', yc.ScoreEnum(maxScoreValueIndex))

# Build out initial action table for given game size
# This is similar to a set of Q-values
def initializeActionTable(gameSize):
    actionDict = {}
    for playedMoves in range(0, (2 ** gameSize) - 1):
        for diceCombination in itertools.combinations_with_replacement("123456", 5):
            for action in range(0, 2**5):
                actionDict[(playedMoves, ''.join(diceCombination), action)] = (0,0,0)
    return actionDict

# Given decimal action integer, return list of dice indices to re-roll
def actionIntToRerollList(action):
    diceToReroll = []
    # enumerate decimale action integer as binary number
    for idx,val in enumerate(list(bin(action)[2:].zfill(5))):
        # for given actions "1", add index to re-roll list
        if (val == '1'):
            diceToReroll.append(idx + 1)
    return diceToReroll
    
# given dicestring and action, return dice state after action (stochastic event)
# This is our delta function. Given a dice string and action, it returns the next state.
def diceAfterAction(diceString, action):
    dice = yc.Dice(diceString)
    diceToReroll = actionIntToRerollList(action)
    if len(diceToReroll) != 0:
        dice.roll(*diceToReroll)
    return dice.asString()

# given game state, score transition from prev dice state to new dice state
# This is our reward function.
def scoreAction(playedMovesBitString, prevDiceString, nextDiceString):
    maxPrevScore = 0
    maxNextScore = 0
    for idx,played in enumerate(playedMovesBitString):
        maxPrevScore = max(maxPrevScore, -10 if played == '1' else scoreFunction(prevDiceString, yc.ScoreEnum(idx))) 
        maxNextScore = max(maxNextScore, -10 if played == '1' else scoreFunction(nextDiceString, yc.ScoreEnum(idx)))
    return maxNextScore - maxPrevScore

# given dice string and desired score, given resulting score
# Helper function to reward function.
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

# Given an action table, the state of the game, and an action, this performs a
# trial and updates the action table(Q-values) with the results.
def trial(actionTable, playedMoves, diceString, action, gameSize):
    prevDiceString = diceString
    nextDiceString = diceAfterAction(prevDiceString, action)
    score = scoreAction(playedMovesIntToBitString(playedMoves,gameSize), prevDiceString, nextDiceString)
    oldActionTableValue = actionTable[(playedMoves, diceString, action)]
    newSum = oldActionTableValue[0] + score
    newTotalGames = oldActionTableValue[1] + 1
    newAvg = newSum / newTotalGames
    actionTable[(playedMoves, diceString, action)] = (newSum, newTotalGames, newAvg)

# This wraps the trial function to perform random trials.
def randomTrial(actionTable, gameSize):
    randomPlayedMoves = random.randint(0, 2**gameSize - 1)
    randomAction = random.randint(0, 2**5 - 1)
    randomDiceString = yc.Dice().asString()
    trial(actionTable, randomPlayedMoves, randomDiceString, randomAction, gameSize)
    return (randomPlayedMoves, randomDiceString, randomAction)

# Our policy function. Given an action table and a game state, it returns the best action.
# Loops through all 32 possible actions, finding the one with the highest expected reward.
def pickAction(actionTable, playedMoves, diceString):
    maxAvg = -100
    bestAction = 0
    for action in range(0,32):
        tableEntry = actionTable[(playedMoves, diceString, action)]
        if (tableEntry[2] > maxAvg):
            maxAvg = tableEntry[2]
            bestAction = action
    return bestAction

# Trains given action table with given number of trials
def trainActionTable(actionTable, gameSize, numberTrials):
    for _ in range(0, numberTrials):
        randomTrial(actionTable, gameSize)

# Saves action table to disk with given name (as a pickle file)
def saveActionTable(actionTable, name):
    with open(name, 'wb') as pfile:
        pickle.dump(actionTable, pfile)

# Loads action table from disk by depickling given file name
def loadActionTable(name):
    with open(name, 'rb') as pfile:
        return pickle.load(pfile)

# Helper function to count total trials in given action table
def sumTotalGames(actionTable):
    sum = 0
    for key,value in actionTable.items():
        sum += value[1]
    return sum
