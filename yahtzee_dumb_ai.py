import yahtzee_core

def dumb_ai_engine(player, rnd, turnNumber, dice):
    """ All engines return tuple. One of two:
        (rollAgain, vals)           Ex. ('y', [1, 2, 5])
        (rollAgain, scoreEnum)      Ex. ('n', yahtzee_core.ScoreEnum.ONES)
    """
    return ('n', getFirstUnplayedScoreEnum(player))


def getFirstUnplayedScoreEnum(player):
    scores = player.scores()
    for i in range(0,13):
        if scores[i] < 0:
            return yahtzee_core.ScoreEnum(i)
