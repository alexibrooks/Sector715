# Sector715
A collection of ASCII strategy games.
To play a game, navigate to the main Sector715 directory and enter the
appropriate python command to launch the game.

##Go
python StandardGo.py
A more-or-less standard Go implementation. Players are X and O. To play a
piece, enter row-space-column into the prompt and hit enter.
e.g.
`Player X plays in position... 0 3`
The game ends when both players consecutively pass. To pass, enter "pass"
into the prompt instead of a position.

##Small Board Go
python SmallBoardGo.py
A more-or-less standard Go implementation on a 9x9 board.

##Barbarian Go
python BarbarianGo.py
A solitaire mode. The barbarian opponent plays randomly, but gets extra turns
to compensate. The game ends when the human player passes.
