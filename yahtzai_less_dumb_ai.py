import yahtzai_core as yc

def ai_engine(player, rnd, turnNumber, dice):
    diceFreq = dice.freq()
    flatten = dice.flatten()
    remaining = player.remainingPlays()
    diceState = dice.view()

    if yc.validateScore(yc.ScoreEnum.YAHTZEE, dice) and (yc.ScoreEnum.YAHTZEE in remaining):
        return ('n', yc.ScoreEnum.YAHTZEE)

    if yc.validateScore(yc.ScoreEnum.LG_STRT, dice) and (yc.ScoreEnum.LG_STRT in remaining):
        return ('n', yc.ScoreEnum.LG_STRT)

    if yc.validateScore(yc.ScoreEnum.SM_STRT, dice) and (yc.ScoreEnum.SM_STRT in remaining):
        return ('n', yc.ScoreEnum.SM_STRT)

    if yc.validateScore(yc.ScoreEnum.FULL_H, dice) and (yc.ScoreEnum.FULL_H in remaining):
        return ('n', yc.ScoreEnum.FULL_H)

    if yc.validateScore(yc.ScoreEnum.FOUR_OF_K, dice) and (yc.ScoreEnum.FOUR_OF_K in remaining):
        return ('n', yc.ScoreEnum.FOUR_OF_K)

    if yc.validateScore(yc.ScoreEnum.THREE_OF_K, dice) and (yc.ScoreEnum.THREE_OF_K in remaining):
        return ('n', yc.ScoreEnum.THREE_OF_K)

    # only reroll dice that don't match the highest freq occurence
    if turnNumber < 2:
        for x in range(5, 1, -1):
            if (x in diceFreq):
                dieNum = diceFreq.index(x) + 1
                diceToReroll = []
                for idx, die in enumerate(diceState):
                    if die != dieNum:
                        diceToReroll.append(idx)
                return ('y', diceToReroll)
        if ((sum(flatten) == 4) and (yc.ScoreEnum.LG_STRT in remaining)
                             and (flatten[0] == 0 or flatten[5] == 0)):
            return ('y', [diceState.index(diceFreq.index(2) + 1) + 1])


    # try to apply score against # with highest freq occurence
    for x in range(5, 1, -1):
        if (x in diceFreq):
            dieNum = diceFreq.index(x) + 1
            if (yc.ScoreEnum(dieNum - 1) in remaining):
                return ('n', yc.ScoreEnum(dieNum - 1))

    return ('n', player.remainingPlays()[0])
