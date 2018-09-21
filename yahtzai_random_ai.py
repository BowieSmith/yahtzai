import yahtzai_core as yc
import random

def ai_engine(player, rnd, turnNumber, dice):
    # roll again. Choose dice to reroll at random
    if random.randint(1,2) == 1 and turnNumber < 2:
        randomDice = [x + 1 for x in range(0,5)]
        for i in range(0, random.randint(0,5)):
            del randomDice[random.randint(0, len(randomDice) - 1)]
        return ('y', randomDice)

    # play random score
    else:
        return('n', player.remainingPlays()[random.randint(0, len(player.remainingPlays()) - 1)])
