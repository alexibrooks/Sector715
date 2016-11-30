import GoBackend as go

mygame = go.Game(19)
turn = 0
while True:
  played = mygame.takeATurn(mygame.players[turn%2])
  if not played:
    print "Player",mygame.players[turn%2],"passes."
    mygame.passCount+=1
    if mygame.passCount >= len(mygame.players):
      print "All players have passed. Game over."
      mygame.scoreGame()
      break
  else:
    mygame.passCount = 0
  turn += 1
