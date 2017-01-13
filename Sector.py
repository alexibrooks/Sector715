import GoBackend as go


#############################################################################

#############################################################################

class Pos(go.Pos):
  pass

class Group(go.Group):
  pass

#############################################################################

#############################################################################

class Sector(go.Board):
  #A Sector is like a Board, but there is an added restriction that players
  #cannot play too far away from their existing pieces.
  def __init__(self,size):
    go.Board.__init__(self,size)
    self.supplyCache = {} #Map color to a matrix indicating where that 
                          #color can legally play.
    self.toUpdateSupply = [] #List of the colors which need supply updates.

  def updateSupplyCache(self,color):
    #This is the thorough, time-consuming option.
    self.supplyCache[color] = [[False for i in range(self.size)] for j in range(self.size)]
    anysup = False
    for g in self.groups:
      if g.color == color:
        n = len(g.members) #Supply range from this group
        for p in g.members:
          for row in range(max(0,p.r-n),min(self.size,p.r+n+1)):
            for col in range(max(0,p.c-n),min(self.size,p.c+n+1)):
              self.supplyCache[color][row][col] = True
              anysup = True
    if not anysup: #A player with no supply presence can play anywhere
      del self.supplyCache[color]

  def inRange(self,pos,color):
    #Determine whether pos is close enough to existing pieces of color for
    #legal play. Supply range is determined by the size of the supplying
    #group. Supply along a diagonal is allowed.
    #If a color has not yet played, everything is in range.
    if color not in self.supplyCache:
      return True
    return self.supplyCache[color][pos.r][pos.c]

  def addPiece(self,pos,color,scoring=False):
    #Check whether we need to update supply ranges first
    if color in self.toUpdateSupply:
      self.toUpdateSupply.remove(color)
      self.updateSupplyCache(color)
    #Check range
    if pos.r<0 or pos.r>=self.size or pos.c<0 or pos.c>=self.size:
      go.ERRORLOG.append("addPiece Failure: position out of bounds.")
      return False
    if self.get(pos) != self.emptygroup:
      go.ERRORLOG.append("addPiece Failure: position already occupied.")
      return False
    if not scoring and not self.inRange(pos,color):
      go.ERRORLOG.append("addPiece Failure: position out of supply range.")
      return False
    self.updateGroups(pos,color) #Set toUpdateSupply at end, not here
    if scoring:
      return True
    vulnGroups = self.getAdjacentGroups(pos,color,"other") #TODO dups?
    vulnGroups = [grp for grp in vulnGroups if grp != self.emptygroup]
    toCapture = [not self.checkLiberties(grp) for grp in vulnGroups]
    for i in range(len(vulnGroups)):
      if toCapture[i]: #TODO does capture interfere?
        self.capture(vulnGroups[i])
        if vulnGroups[i].color not in self.toUpdateSupply:  
          self.toUpdateSupply.append(vulnGroups[i].color)
    if not self.checkLiberties(self.get(pos)):
      self.capture(self.get(pos))
    if color not in self.toUpdateSupply:
      self.toUpdateSupply.append(color)
    return True

#############################################################################

#############################################################################

class Game(go.Game):
  def __init__(self,size):
    self.players = ["X","O"]
    self.passCount = 0
    self.board = Sector(size)

  def takeATurn(self,player):
    return go.Game.takeATurn(self,player)

