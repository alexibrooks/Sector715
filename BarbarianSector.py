import Sector as go
import random

def playBarb(game):
  played = False
  while not played:
    r = random.randint(0,size-1)
    c = random.randint(0,size-1)
    p = go.Pos(r,c)
    adj = game.board.getAdjacentGroups(p,game.players[1],"other")
    if len(adj) > 0:
      played = game.board.addPiece(p,game.players[1]) #True iff add succeeded
      

def getDiff():
  #Easy = 2, Medium = 3, Hard = 4
  inp = raw_input("Enter a difficulty number: ")
  if inp.lower() == "easy":
    return 2
  if inp.lower() == "medium":
    return 3
  if inp.lower() == "hard":
    return 4
  try:
    diff = int(inp)
    if diff < 1:
      print "Invalid difficulty."
      return getDiff()
    return diff
  except ValueError:
    print "Invalid difficulty."
    return getDiff()

size = 9
mygame = go.Game(size)
print "Welcome to BARBARIAN GO (SECTOR STYLE)"
print "a solitaire game based on the strategy game Go."
print ""
print "Barbarians play randomly, but they get to play more than you do!"
print "Difficulty is based on how many times the barbarian plays between each"
print "of your plays. EASY (2), MEDIUM (3), HARD (4)."
print "Note that you will only be able to play within a certain range of your"
print "existing groups."
diff = getDiff()
while True:
  played = mygame.takeATurn(mygame.players[0]) #Human player is first player
  if not played:
      print "Human player passed. Game over."
      mygame.scoreGame()
      break
  else:
    for i in range(diff):
      playBarb(mygame)
