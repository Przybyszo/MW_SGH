import copy

from enum import Enum

class Color(Enum):
    BLUE = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
	
class Context(Enum):
	MEETOWN = 0
	MEETOTHER = 1
	DEFOTHER = 2
	COOPOWN = 3
	COOPOTHER = 4

class EthnoPlayer(CellOccupant):
	
	def initialize(self):
		super(EthnoPlayer, self).initialize()
		
		if (self.__scape.getModel().getOneTagOnly()):
			tag = Color.BLUE
		else:
			if (scape.getModel().getUseMoreColors()):
				numColors = scape.getModel().getNumColors()
				tag = randomInRange(0, numColors)
			else:
				if (randomIs()):
					tag = Color.BLUE
				else:
					tag = Color.RED
					
		self.__strategyToOwn = randomIs()
		self.__strategyToOther = randomIs()
	
	def copy(self):
		return copy.deepcopy(self)
	
	def scapeCreated(self):
		getScape().addInitialRule(MOVE_RANDOM_LOCATION_RULE)
		getScape().addRule(UPDATE_RULE)
		
		getScape().addRule(PLAY_NEIGHBOURS_RULE)
		
		getScape().addRule(FISSIONING_RULE)
		getScape().addRule(DEATH_RULE)
		
	def playRandomGlobal(self, agent):
		while True:
			index = randomToLimit(self.__scape.getSize())
			candidatePartner = self._scape.getCell(index)
			if candidatePartner != self:
				break
				4346
		if candidatePartner.getHostCell().isAvailable():
			print("EMPTY PARTNER!")
		
		agent.play(candidatePartner)
		
	def update(self):
		self.__currOTR = self._scape.getModel().getBaseOTR()
		
		if (self._scape.getModel().getUseDiscrimCost()):
			if (self.__strategyToOwn != self.__strategyToOther):
				self.__currOTR -= self._scape.getModel().getDiscrimCost()
				
	def fissionCondition(self):
		if (randomInRange(0.0, 1.0) < self._currOTR):
			return True
		return False
		
	def deathCondition(self):
		theDeathRate = self._scape.getModel().getDeathRate()
		
		if (randomInRange(0.0, 1.0) < theDeathRate):
			return True
		return False

	def fission(self):
		locateChildNear = self._scape.getModel().getLocateChildNear()
		
		if (locateChildNear):
			if (self.getHostCell().isNeighbourAvailable()):
				child = self.copy()
				self.getScape().addAgent(child)
				child.moveTo(self.getHostCell().findRandomAvailableNeighbour())
				
				if (getRandom() < self.scape.getModel().getMutationRate()):
					child.strategyToOwn(not self.strategyToOwn)
				else:
					child.strategyToOther(self.strategyToOther)
					
				if (self.scape.getModel().getOneTagOnly()):
					child.tag(self.tag)
				else:
					if (getRandom() < self.scape.model.mutationRate):
						if (self.scape.model.useMoreColors()):
							numColors = self.scape.model.numColors
							child.tag(randomInRange(0, numColors))
						
							while (child.tag == self.tag):
								child.tag(randomInRange(0, numColors))
						else:
							if (self.tag == Color.BLUE):
								self.tag = Color.RED
							else:
								self.tag = Color.BLUE
					else:
						child.tag(self.tag)
				
				child.hostCell().updateCell()
		else:
			if (self.scape.model.numPlayers < self.scape.model.maxAgents):
				potentialLoc = self.hostCell.scape.findRandomUnoccupiedCell()
				child = self.clone()
				self.scape.addAgent(child)
				child.moveTo(potentialLoc)
				
				if (getRandom() < self.scape.model.mutationRate):
					child.strategyToOwn(not self.strategyToOwn)
				else:
					child.strategyToOwn(self.strategyToOwn)
				
				if (getRandom() < self.scape.model.mutationRate):
					child.strategyToOther(not self.strategyToOther)
				else:
					child.strategyToOther(self.strategyToOther)
					
				if (self.scape.model.oneTagOnly):
					child.tag(self.tag)
				else:
					if (self.random < scape.model.mutationRate):
						if (scape.model.useMoreColors)
							numColors = scape.model.numColors
							child.tag = randomInRange(0, numColors)
							
							while (child.tag == self.tag):
								child.tag = randomInRage(0, numColors)
						else:
							if (self.tag == Color.BLUE):
								child.tag = Color.RED
							else:
								child.tag = Color.BLUE
				child.hostCell.updateCell()
				
	def play(self, partner):
		strategy = False
		partnerStrategy = False
		
		if (self.tag == partner.tag):
			strategy = self.strategyToOwn
			