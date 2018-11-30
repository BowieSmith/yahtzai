# YAHTZAI -- That's Yahtzee, with AI -- Pronounced YAHTZ-AY!

## Brought to you by "Team Blue":
- Jason Gorelik
- Elwin Brown
- Bowie Smith
- Justin Wilmot

## Dependencies
- python3 (that's it!)

## Usage
python3 yahtzai.py [-a "actionTableName.p"]

The optional [-a "actionTableName.p"] parameter allows you to pass in a pickle
file representing a custom action table.
If no pickle file is specified with the -a parameter and a reinforcement learning
AI is chosen, the game defaults to a pickle file with the name "atn.p", where n
is the number of rounds for the chosen game.
If a RL AI is chosen and the default or custom action table does not exist, the
game will exit.

## Modules
- yahtzai.py                    Starting module implementing main game loop
- yahtzai\_core.py              Utility functions and implementation of game data structures

The following list gives the AI implementation and the module where they can be found:
- yahtzai\_less\_dumb\_ai.py    Expert System
- yahtzai\_rl\_ai.py            Reinforcement Learning
- yahtzai\_random\_ai.py        Not an AI, just a baseline
- yahtzai\_dumb\_ai.py          Not an AI, just specification of AI interface

## Training
The reinforcement learning AI requires that an action table be generated. In order
to generate an action table, you must use a python REPL, import the yahtzai\_rl\_ai
module, and perfrom the following tasks:

`>>> import yahtzai_rl_ai as rl`        # import reinforcement learning module

`>>> at6 = rl.initializeActionTable(6)` # initialize action table (this example is
                                        # for a 6-round game of Yahtzee)

`>>> rl.trainActionTable(at6, 6, 1000)` # train action table (this example trains
                                        # action table at6 on a 6-round game with 1000 trials)

`>>> rl.saveActionTable(at6, "at6.p")`  # save action table to disk (this example saves
                                        # the action table to the default name)

`>>> at6 = rl.loadActionTable("at6.p")` # load action table from disk (this is useful
                                        # to continue action table training in sessions
