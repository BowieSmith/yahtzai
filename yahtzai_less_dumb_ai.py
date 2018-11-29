import yahtzai_core as yc

# Expert system AI interface:
def ai_engine(player, rnd, turnNumber, dice):
    diceFreq = dice.freq()
    flatten = dice.flatten()
    remaining = player.remainingPlays()
    diceState = dice.view()

    # if dice are valid yahtzee and has not be played, then play
    if yc.validateScore(yc.ScoreEnum.YAHTZEE, dice) and (yc.ScoreEnum.YAHTZEE in remaining):
        return ('n', yc.ScoreEnum.YAHTZEE)

    # if dice are valid lg strt and has not be played, then play
    if yc.validateScore(yc.ScoreEnum.LG_STRT, dice) and (yc.ScoreEnum.LG_STRT in remaining):
        return ('n', yc.ScoreEnum.LG_STRT)
    
    # if dice are valid sm strt and has not be played, then play
    if yc.validateScore(yc.ScoreEnum.SM_STRT, dice) and (yc.ScoreEnum.SM_STRT in remaining):
        return ('n', yc.ScoreEnum.SM_STRT)

    # if dice are valid full house and has not be played, then play
    if yc.validateScore(yc.ScoreEnum.FULL_H, dice) and (yc.ScoreEnum.FULL_H in remaining):
        return ('n', yc.ScoreEnum.FULL_H)


    # only reroll dice when agent hasn't used both re-rolls
    if turnNumber < 2:
        # reroll all dice except those occuring with highest frequency
        for x in range(5, 1, -1):
            if (x in diceFreq):
                dieNum = max(idx for idx, freq in enumerate(diceFreq) if freq == x) + 1
                if (not yc.ScoreEnum(dieNum - 1) in remaining) and (dieNum <= 4) and (turnNumber <= 7):
                    break
                if ((not yc.ScoreEnum(dieNum - 1) in remaining) and
                   (not yc.ScoreEnum.FOUR_OF_K in remaining) and
                   (not yc.ScoreEnum.THREE_OF_K in remaining)):
                    break
                diceToReroll = []
                for idx, die in enumerate(diceState):
                    if die != dieNum:
                        diceToReroll.append(idx + 1)
                return ('y', diceToReroll)

        # if 4ofK and 2,3,4,5, re-roll duplicate to go for large straight
        if ((sum(flatten) == 4) and (yc.ScoreEnum.LG_STRT in remaining)
                             and (flatten[0] == 0 or flatten[5] == 0)):
            return ('y', [diceState.index(diceFreq.index(2) + 1) + 1])

        return ('y', [])



    # try to apply score against # with highest freq occurence
    for x in range(5, 1, -1):
        if (x in diceFreq):
            dieNum = max(idx for idx, freq in enumerate(diceFreq) if freq == x) + 1
            if (yc.ScoreEnum(dieNum - 1) in remaining):
                return ('n', yc.ScoreEnum(dieNum - 1))
            if ((yc.ScoreEnum.FOUR_OF_K in remaining) and
                (yc.validateScore(yc.ScoreEnum.FOUR_OF_K, dice))):
                return ('n', yc.ScoreEnum.FOUR_OF_K)
            if ((yc.ScoreEnum.THREE_OF_K in remaining) and
                (yc.validateScore(yc.ScoreEnum.THREE_OF_K, dice))):
                return ('n', yc.ScoreEnum.THREE_OF_K)

    # if nothing left, play chance
    if yc.ScoreEnum.CHANCE in remaining:
        return ('n', yc.ScoreEnum.CHANCE)
    # if nothing left, play ones
    if yc.ScoreEnum.ONES in remaining:
        return ('n', yc.ScoreEnum.ONES)
    # if nothing left, play yahtzee
    if yc.ScoreEnum.YAHTZEE in remaining:
        return ('n', yc.ScoreEnum.YAHTZEE)

    return ('n', player.remainingPlays()[0])
