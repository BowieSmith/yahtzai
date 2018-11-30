import yahtzai_core

# This is a test of the AI turn interface
def ai_engine(player, rnd, turnNumber, dice):
    """ All engines return tuple. One of two:
        (rollAgain, vals)           Ex. ('y', [1, 2, 5])
        (rollAgain, scoreEnum)      Ex. ('n', yahtzai_core.ScoreEnum.ONES)
    """
    return ('n', player.remainingPlays()[0])
