import random
from datetime import datetime
from enum import Enum

class Color(Enum):
    BLUE = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
	
class Strategy(Enum):
	ALLC = 0
	ALLD = 1
	ETHNO = 2
	ANTIETHNO = 3

class EthnoCell(object):
	ARBITRARY_SEED = -1
	PLATFORM_DEFAULT_COLOR = 0
	EMPTY = 4
	
	def __init__(self, name):
		self.__random = random.seed(datetime.now())
		self.__randomSeed = ARBITRATY_SEED
		if not (name is None):
			self._name = name
	
	def initialize(self):
		self.__lastOccupant = [EMPTY] * 2
		self.__ALLCtoSame = [0] * 4
		self.__ALLCToDiff = [0] * 4
		self.__ALLDtoSame = [0] * 4
		self.__ALLDtoDiff = [0] * 4
		self.__ETHNOtoSame = [0] * 4
		self.__ETHNOtoDiff = [0] * 4
		self.__ANTIETHNOtoSame = [0] * 4
		self.__ANTIETHNOtoDiff = [0] * 4
	
	@property
	def name(self):
		return self._name

	@name.setter
	def name(self, name):
		self._name = name
	
	@property
	def scape(self):
		return self._scape
		
	@scape.setter
	def scape(self, scape):
		self._scape = scape
		
	@property
	def random(self):
		return self._random
		
	@random.setter
	def random(self, random):
		self._random = random
	
	def getRandomSeed(self):
		return self._lastRandomSeed
		
	def setRandomSeed(self, seed):
		self._randomSeed = seed
		reseed()
		
	def reseed(self):
		if (self._randomSeed != ARBITRARY_SEED):
			self.__lastRandomSeed = self.__randomSeed
		else:
			self.__lastRandomSeed = datetime.now()
		self.__random = random.seed(self.__lastRandomSeed)
		
	def randomInRangeInt(self, low, high):
		return random.randint(low, high)
		
	def randomInRangeDouble(self, low, high):
		return random.uniform(low, high)
		
	def updateCell(self):
		if (getIteration >= 1900):
			occupantStrategyOwn = self.getOccupant().getStrategyOwn()
			occupantStrategyOther = self.getOccupant().getStrategyOther()
			
			occupantTag = self.getOccupant().getTag()
			
			if (self.isAvailable()):
				print("UPDATING EMPTY CELL!")
				
			if (occupantStrategyOwn):
				if (occupantStrategyOther):
					occupantType = Strategy.ALLC
				else:
					occupantType = Strategy.ETHNO
			else:
				if (occupantStrategyOther):
					occupantType = Strategy.ANTIETHNO
				else:
					occupantType = Strategy.ALLD
					
			if (self.hasHadOccupant()):
				if (self._lastOccupant[0] == occupantTag):
					if self._lastOccupant[1] == Strategy.ALLC:
						ALLCtoDiff[occupantType] += 1
					if self._lastOccupant[1] == Strategy.ALLD:
						ALLDtoDiff[occupantType] += 1
					if self._lastOccupant[1] == Strategy.ETHNO:
						ETHNOtoDiff[occupantType] += 1
					if self._lastOccupant[1] == Strategy.ANTIETHNO:
						ANTIETHNOtoDiff[occupantType] += 1
			else:
				self._hasHadOccupant = True
				
			self._lastOccupant[0] = occupantTag
			self._lastOccupant[1] = occupantType
			
	def getAllCtoDiff(self, type):
		return self._ALLCtoDiff[type]
		
	def getAllDtoDiff(self, type):
		return self._ALLDtoDiff[type]
		
	def getETHNOtoDiff(self, type):
		return self._ETHNOtoDiff[type]
		
	def getANTIETHNOCtoDiff(self, type):
		return self._ANTIETHNOtoDiff[type]

	def getAllCtoSame(self, type):
		return self._ALLCtoSame[type]
		
	def getAllDtoSame(self, type):
		return self._ALLCtoSame[type]
		
	def getETHNOtoSame(self, type):
		return self._ALLCtoSame[type]
		
	def getANTIETHNOtoSame(self, type):
		return self._ALLCtoSame[type]