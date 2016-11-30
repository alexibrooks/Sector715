#Exploring the possibility of organizing the pieces on the board into groups
#There can be up to 19x19 different groups (if we checkerboarded the board).

EMPTY = "."
CONTESTED = " "
ERRORLOG = []

##############################################################################
class Pos:
  def __init__(self,row,col):
    self.r = row
    self.c = col

class Group:
  #numbers = range(19*19)
  def __init__(self,color,number):
    self.color = color
    self.number = number #min(Group.numbers)
    #Group.numbers.remove(self.number)
    self.members = []

  def add(self,pos):
    self.members.append(pos)

#  def delete(self):
#    #To be used after a group is captured to free up space in numbers
#    Group.numbers.append(self.number)

  def __lt__(self,other):
    return self.number < other.number
  def __gt__(self,other):
    return self.number > other.number
##############################################################################

##############################################################################
class Board:
  def __init__(self,size):
    self.size = size #Standard dimensions of a GO board is 19x19
    self.groups = [] #There are initially no groups TODO presently unused? Implicit
    self.unused = range(size*size) #We will make no more than size^2 groups
    self.emptygroup = Group(EMPTY,None)
    self.board = [[self.emptygroup for i in range(self.size)] for j in range(self.size)]

  def set(self,pos,grp):
    self.board[pos.r][pos.c] = grp
    grp.add(pos)

  def get(self,pos):
    return self.board[pos.r][pos.c]

  def printBoard(self):
    top = ""
    for i in range(self.size):
      if i<10:
        top += " " + str(i)
      elif i%2==0:
        top += " ."
      else:
        top += str(i)
    print top
    print "+"+"-"*(self.size*2-1)+"+"
    rownum = 0
    for row in self.board:
      s = "|"
      for c in row:
        s += c.color + " "
      print s[:-1]+"|",rownum
      rownum+=1
    print "+"+"-"*(self.size*2-1)+"+"

  def printGroups(self):
    top = ""
    for i in range(self.size):
      if i<10:
        top += " " + str(i)
      elif i%2==0:
        top += " ."
      else:
        top += str(i)
    print top
    print "+"+"-"*(self.size*2-1)+"+"
    rownum = 0
    for row in self.board:
      s = "|"
      for c in row:
        s += str(c.number) + " "
      print s[:-1]+"|",rownum
      rownum+=1
    print "+"+"-"*(self.size*2-1)+"+"

  def addPiece(self,pos,color,scoring=False):
    #Add a piece of the given color at the given position and conduct group
    #updates and capturing. If scoring is True, then no capturing is done.
    if pos.r<0 or pos.r>=self.size or pos.c<0 or pos.c>=self.size:
      ERRORLOG.append("addPiece Failure: position out of bounds.")
      return False
    if self.get(pos) != self.emptygroup:
      ERRORLOG.append("addPiece Failure: position already occupied.")
      return False
    #self.board[pos.r][pos.c] = color
    self.updateGroups(pos,color)
    if scoring:
      return True
    vulnGroups = self.getAdjacentGroups(pos,color,"other")
    toCapture = [not self.checkLiberties(grp) for grp in vulnGroups]
    for i in range(len(vulnGroups)):
      if toCapture[i]:
        self.capture(vulnGroups[i])
    if not self.checkLiberties(self.get(pos)):
      self.capture(self.get(pos))
    return True

  def getAdjacentGroups(self,pos,color,mode):
    ans = []
    if mode == "match":
      if pos.r>0 and self.board[pos.r-1][pos.c].color == color:
        ans.append(self.board[pos.r-1][pos.c])
      if pos.r<self.size-1 and self.board[pos.r+1][pos.c].color == color:
        ans.append(self.board[pos.r+1][pos.c])
      if pos.c>0 and self.board[pos.r][pos.c-1].color == color:
        ans.append(self.board[pos.r][pos.c-1])
      if pos.c<self.size-1 and self.board[pos.r][pos.c+1].color == color:
        ans.append(self.board[pos.r][pos.c+1])
      return ans
    elif mode == "other":
      if pos.r>0 and self.board[pos.r-1][pos.c].color != color:
        ans.append(self.board[pos.r-1][pos.c])
      if pos.r<self.size-1 and self.board[pos.r+1][pos.c].color != color:
        ans.append(self.board[pos.r+1][pos.c])
      if pos.c>0 and self.board[pos.r][pos.c-1].color != color:
        ans.append(self.board[pos.r][pos.c-1])
      if pos.c<self.size-1 and self.board[pos.r][pos.c+1].color != color:
        ans.append(self.board[pos.r][pos.c+1])
      return ans
    else:
      print "Mode",mode,"not implemented."
      return False

  def checkLiberties(self,grp):
    #Return True if a group has liberties, False otherwise
    for i in grp.members:
      if self.adjacent(i,self.emptygroup):
        return True
    return False

  def adjacent(self,pos,grp):
    #Return True if grp is adjacent to pos, False otherwise
    if pos.r>0 and self.board[pos.r-1][pos.c] == grp:
      return True
    if pos.r<self.size-1 and self.board[pos.r+1][pos.c] == grp:
      return True
    if pos.c>0 and self.board[pos.r][pos.c-1] == grp:
      return True
    if pos.c<self.size-1 and self.board[pos.r][pos.c+1] == grp:
      return True
    return False

  def adjacentColor(self,pos,color):
    #Return True if grp is adjacent to pos, False otherwise
    if pos.r>0 and self.board[pos.r-1][pos.c].color == color:
      return True
    if pos.r<self.size-1 and self.board[pos.r+1][pos.c].color == color:
      return True
    if pos.c>0 and self.board[pos.r][pos.c-1].color == color:
      return True
    if pos.c<self.size-1 and self.board[pos.r][pos.c+1].color == color:
      return True
    return False

  def capture(self,grp):
    for r in range(self.size):
      for c in range(self.size):
        p = Pos(r,c)
        if self.get(p) == grp:
          self.set(p,self.emptygroup)
    self.unused.append(grp.number)

  def updateGroups(self,pos,color):
    adj = self.getAdjacentGroups(pos,color,"match")
    if adj == []: #If no adjacent matching groups, make a new one
      minunused = min(self.unused)
      g = Group(color,minunused)
      self.unused.remove(minunused)
      self.set(pos,g)
      return
    n = min(adj) #Otherwise, consolidate
    adj.remove(n)
    self.set(pos,n)
    for r in range(self.size):
      for c in range(self.size):
        p = Pos(r,c)
        if self.get(p) in adj:
          self.set(p,n)
    for x in adj:
      self.unused.append(x.number)

  def computeScore(self):
    #This version makes an actual temporary board
    nonecolor = "NONE" #Bit of a kludge here. Need to not match with this.
    scoreboard = Board(self.size)
    scoreboard.emptygroup.color = nonecolor
    for r in range(self.size):
      for c in range(self.size):
        p = Pos(r,c)
        scoreboard.addPiece(p,self.get(p).color,True)
    #Create the relevant groups
    emptygrps = []
    colors = []
    for r in range(self.size):
      for c in range(self.size):
        g = scoreboard.get(Pos(r,c))
        if g.color==EMPTY and g not in emptygrps:
          emptygrps.append(g)
        elif g.color != EMPTY and g.color not in colors:
          colors.append(g.color)
    #Mark the empty groups according to adjacency
    for g in emptygrps:
      notadjcolors = list(colors)
      adjcolors = []
      for p in g.members:
        toRemove = []
        for c in notadjcolors:
          if scoreboard.adjacentColor(p,c):
            toRemove.append(c)
            adjcolors.append(c)
        for x in toRemove:
          notadjcolors.remove(x)
      if len(adjcolors) == 1:
        g.color = adjcolors[0] #Recolor for later score display/calculation
      else:
        g.color = CONTESTED
    #Calculate color scores
    scores = {}
    for c in colors:
      scores[c] = 0
    scores[CONTESTED] = 0
    for r in range(self.size):
      for c in range(self.size):
        scores[scoreboard.get(Pos(r,c)).color] += 1
    #Display scores
    self.displayScore(scores,scoreboard)

  def displayScore(self,scores,scoreboard):
    scoreboard.printBoard()
    contested = scores.pop(CONTESTED)
    print "SCORES:"
    for player in scores:
      print player,"scores",scores[player],"points."
    print "There are",contested,"contested spaces."

##############################################################################

##############################################################################
class Game:
  def __init__(self,size):
    self.players = ["X","O"]
    self.board = Board(size)
    self.passCount = 0

  def getInputs(self):
    raw = raw_input("plays in position... ")
    if raw == "pass":
      return None
    try:
      ans = [int(x) for x in raw.split()]
      if len(ans) != 2:
        print "Invalid input."
        print "Try '[row] [col]' or 'pass'."
        return self.getInputs()
      return ans
    except ValueError:
      print "Invalid input."
      print "Try '[row] [col]' or 'pass'."
      return self.getInputs()

  def takeATurn(self,player):
    self.board.printBoard()
    print "Player",player,
    inputs = self.getInputs()
    if None == inputs: #Pass
      return False
    while not self.board.addPiece(Pos(inputs[0],inputs[1]),player):
      print ERRORLOG[-1]
      inputs = self.getInputs()
      if None == inputs: #Pass
        return False
    return True #Played successfully

  def scoreGame(self):
    self.board.computeScore()
##############################################################################

##############################################################################
if __name__=="__main__":
  testgame = Game(19)
  turn = 0
  while True:
    played = testgame.takeATurn(testgame.players[turn%2])
    if not played:
      print "Player",testgame.players[turn%2],"passes."
      testgame.passCount+=1
      if testgame.passCount >= len(testgame.players):
        print "All players have passed. Game over."
        break
    else:
      testgame.passCount = 0
    turn += 1
