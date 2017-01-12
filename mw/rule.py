import world
from agent import WolfAgent, RabbitAgent, GrassAgent

class Rule(object):
	LEFT = 0
	RIGHT = 1
	UP = 2
	DOWN = 3
	
	WOLF = 1
	RABBIT = 2
	GRASS = 3
	
	POSSIBLE = 1
	NOT_POSSIBLE = 2
	COVER = 3
	EAT = 4
	
	def __init__(self):
		print(world.rabbit)
		self._rabbit = world.rabbit
		self._wolf = world.wolf
		self._grass = world.grass
		self._wolf_in_grass = world.wolf_in_grass
		self._empty = world.empty
		
	@property
	def empty(self):
		return self._empty
		
	@property
	def grass(self):
		return self._grass
		
	@property
	def wolf(self):
		return self._wolf
		
	@property
	def rabbit(self):
		return self._rabbit
		
	@property
	def wolf_in_grass(self):
		return self._wolf_in_grass
		
	def moveSet(self, x_pos, y_pos, neighbourHood, max_x, max_y):
		moveset = [self.POSSIBLE] * 4
		if (x_pos == 0):
			moveset[self.UP] = self.NOT_POSSIBLE
		if (x_pos == max_x):
			moveset[self.DOWN] = self.NOT_POSSIBLE
		if (y_pos == 0):
			moveset[self.LEFT] = self.NOT_POSSIBLE
		if (y_pos == max_y):
			moveset[self.RIGHT] = self.NOT_POSSIBLE
		return moveset
		
	def performMove(self, plane, src_x ,src_y, dest_x, dest_y):
		pass
		
	def removeAgent(self, plane, x, y):
		plane.widgets[x][y].configure(image = self.empty)
		plane.widgets[x][y].agent = None
		plane.widgets[x][y].image = self.empty

class WolfRule(Rule):
	def moveSet(self, x_pos, y_pos, neighbourHood, max_x, max_y):
		moveset = super(WolfRule, self).moveSet(x_pos, y_pos, neighbourHood, max_x, max_y)
		for i in range(self.LEFT, self.DOWN + 1):
			if neighbourHood[i] == self.wolf:
				moveset[i] == self.NOT_POSSIBLE		
		return moveset
	
	def performMove(self, app, plane, src_x, src_y, dest_x, dest_y):
		if plane.widgets[dest_x][dest_y].image == self.empty or plane.widgets[dest_x][dest_y].image == self.rabbit:	
			if plane.widgets[src_x][src_y].image == self.wolf_in_grass:
				plane.widgets[dest_x][dest_y].agent = plane.widgets[src_x][src_y].agent
				plane.widgets[dest_x][dest_y].image = self.wolf
				plane.widgets[dest_x][dest_y].configure(image = self.wolf)
				plane.widgets[src_x][src_y].configure(image = self.grass)
				plane.widgets[src_x][src_y].agent = GrassAgent(app, self.grass, None)
				plane.widgets[src_x][src_y].image = self.grass			
			else:
				plane.widgets[dest_x][dest_y].agent = plane.widgets[src_x][src_y].agent
				plane.widgets[dest_x][dest_y].image = plane.widgets[src_x][src_y].image
				plane.widgets[dest_x][dest_y].configure(image = plane.widgets[src_x][src_y].image)
				plane.widgets[src_x][src_y].configure(image = self.empty)
				plane.widgets[src_x][src_y].agent = None
				plane.widgets[src_x][src_y].image = self.empty
		elif plane.widgets[dest_x][dest_y].image == self.grass:
			if plane.widgets[src_x][src_y].image == self.wolf_in_grass:
				plane.widgets[dest_x][dest_y].agent = plane.widgets[src_x][src_y].agent
				plane.widgets[dest_x][dest_y].image = self.wolf_in_grass
				plane.widgets[dest_x][dest_y].configure(image = self.wolf_in_grass)
				plane.widgets[src_x][src_y].configure(image = self.grass)
				plane.widgets[src_x][src_y].agent = GrassAgent(app, self.grass, None)
				plane.widgets[src_x][src_y].image = self.grass					
			else:
				plane.widgets[dest_x][dest_y].agent = plane.widgets[src_x][src_y].agent
				plane.widgets[dest_x][dest_y].image = self.wolf_in_grass
				plane.widgets[dest_x][dest_y].configure(image = self.wolf_in_grass)
				plane.widgets[src_x][src_y].configure(image = self.empty)
				plane.widgets[src_x][src_y].agent = None
				plane.widgets[src_x][src_y].image = self.empty
		
class RabbitRule(Rule):	
	def moveSet(self, x_pos, y_pos, neighbourHood, max_x, max_y):
		moveset = super(RabbitRule, self).moveSet(x_pos, y_pos, neighbourHood, max_x, max_y)
		for i in range(self.LEFT, self.DOWN + 1):
			if neighbourHood[i] == self.rabbit or neighbourHood[i] == self.wolf:
				moveset[i] == self.NOT_POSSIBLE		
		return moveset
	
	def performMove(self, plane, src_x, src_y, dest_x, dest_y):
		if plane.widgets[dest_x][dest_y].image == self.empty:
			plane.widgets[dest_x][dest_y].agent = plane.widgets[src_x][src_y].agent
			plane.widgets[dest_x][dest_y].image = plane.widgets[src_x][src_y].image
			plane.widgets[dest_x][dest_y].configure(image = plane.widgets[src_x][src_y].image)
			plane.widgets[src_x][src_y].configure(image = self.empty)
			plane.widgets[src_x][src_y].agent = None
			plane.widgets[src_x][src_y].image = self.empty
		if plane.widgets[dest_x][dest_y].image == self.grass:
			plane.widgets[src_x][src_y].agent.addEnergy(plane.widgets[dest_x][dest_y].agent.energy)
			plane.widgets[dest_x][dest_y].agent = plane.widgets[src_x][src_y].agent
			plane.widgets[dest_x][dest_y].image = plane.widgets[src_x][src_y].image
			plane.widgets[dest_x][dest_y].configure(image = plane.widgets[src_x][src_y].image)
			plane.widgets[src_x][src_y].configure(image = self.empty)
			plane.widgets[src_x][src_y].agent = None
			plane.widgets[src_x][src_y].image = self.empty
