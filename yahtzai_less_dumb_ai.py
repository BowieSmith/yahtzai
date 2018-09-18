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

    if turnNumber < 2:
        for x in range(5, 1, -1):
            if (x in diceFreq):
                dieNum = diceFreq.index(x) + 1
                diceToReroll = []
                for idx, die in enumerate(diceState):
                    if die != dieNum:
                        diceToReroll.append(idx)
                return ('y', diceToReroll)

    for x in range(5, 1, -1):
        if (x in diceFreq):
            dieNum = diceFreq.index(x) + 1
            if (yc.ScoreEnum(dieNum - 1) in remaining):
                return ('n', yc.ScoreEnum(dieNum - 1))

    return ('n', player.remainingPlays()[0])
