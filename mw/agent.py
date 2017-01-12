import world as w
import itertools
from random import randint
from utils import random_number_generator

class resource_cl(object):
	newid = itertools.count().next
	def __init__(self):
		self._id = resource_cl.newid()
		
	@property
	def id(self):
		return self._id


class Agent(object):
	def __init__(self, image, rule):
		self._image = image
		self._moveRule = rule
		self._energy = 0
		self._id = resource_cl().id
		
	@property
	def id(self):
		return self._id
		
	@property
	def image(self):
		return self._image
		
	@property
	def rule(self):
		return self._moveRule
	
	@property
	def energy(self):
		return self._energy
	
	def move(self, x_pos, y_pos, neighbourHood, max_x, max_y, plane, movedMatrix):
		pass
		
	def die(self):
		if (self.energy < 0):
			return True
		return False
		
class RabbitAgent(Agent):
	def __init__(self, app, image, rule):
		super(RabbitAgent, self).__init__(image, rule)
		
		rabbitMean = int(w.RabbitInitialEnergyEntryMean.get()) if w.RabbitInitialEnergyEntryMean.get() <> '' else 10
		rabbitVariance = int(w.RabbitInitialEnergyEntryVariance.get()) if w.RabbitInitialEnergyEntryVariance.get() <> '' else 0
		rabbitEnergy = round(random_number_generator(rabbitMean, rabbitVariance))
		rabbitEnergy = 0 if rabbitEnergy < 0 else rabbitEnergy
		
		self._energy = rabbitEnergy
		self._app = app
		
		rabbitMean = int(w.birthdayRabbitThresholdEntryMean.get()) if w.birthdayRabbitThresholdEntryMean.get() <> '' else 10
		rabbitVariance = int(w.birthdayRabbitThresholdEntryVariance.get()) if w.birthdayRabbitThresholdEntryVariance.get() <> '' else 0
		rabbitThreshold = round(random_number_generator(rabbitMean, rabbitVariance))
		rabbitThreshold = 0 if rabbitThreshold < 0 else rabbitThreshold
		
		self._condition = rabbitThreshold
	
	@property
	def condition(self):
		return self._condition
	
	@property
	def app(self):
		return self._app
	
	def addEnergy(self, energy):
		self._energy += energy
		
	def reproduce(self, plane, row, column, max_row, max_column, movedMatrix):
		reproduce_set = []
		if row <> 0:
			if not plane.widgets[row - 1][column].image == self.rule.wolf and not plane.widgets[row - 1][column].image == self.rule.rabbit and not plane.widgets[row - 1][column].image == self.rule.wolf_in_grass:
				reproduce_set.append((row - 1, column))
		if row <> max_row:
			if not plane.widgets[row + 1][column].image == self.rule.wolf and not plane.widgets[row + 1][column].image == self.rule.rabbit and not plane.widgets[row + 1][column].image == self.rule.wolf_in_grass:
				reproduce_set.append((row + 1, column))
		if column <> 0:
			if not plane.widgets[row][column - 1].image == self.rule.wolf and not plane.widgets[row][column - 1].image == self.rule.rabbit and not plane.widgets[row][column - 1].image == self.rule.wolf_in_grass:
				reproduce_set.append((row, column - 1))			
		if column <> max_column:
			if not plane.widgets[row][column + 1].image == self.rule.wolf and not plane.widgets[row][column + 1].image == self.rule.rabbit and not plane.widgets[row][column + 1].image == self.rule.wolf_in_grass:
				reproduce_set.append((row, column + 1))
		
		if len(reproduce_set) == 0:
			return
		
		rand = randint(0, len(reproduce_set) - 1)
		
		if (self.energy >= self.condition):
			move_tuple = reproduce_set[rand]
			self.addEnergy(-0.5 * self.condition)
			plane.widgets[move_tuple[0]][move_tuple[1]].agent = RabbitAgent(self.app, self.image, self.rule)
			plane.widgets[move_tuple[0]][move_tuple[1]].image = self.rule.rabbit
			plane.widgets[move_tuple[0]][move_tuple[1]].configure(image = self.rule.rabbit)
			movedMatrix[move_tuple[0]][move_tuple[1]] = 1
			
	def move(self, x_pos, y_pos, neighbourHood, max_x, max_y, plane, movedMatrix):
		move_energy_mean = int(w.rabbitMoveCostEntryMean.get()) if w.rabbitMoveCostEntryMean.get() <> '' else 0.5
		move_energy_variance = int(w.rabbitMoveCostEntryVariance.get()) if w.rabbitMoveCostEntryVariance.get() <> '' else 0
		move_energy = random_number_generator(move_energy_mean, move_energy_variance)
		move_energy = 0 if move_energy < 0 else move_energy
		
		self._energy -= move_energy
		moves = self.rule.moveSet(x_pos, y_pos, neighbourHood, max_x, max_y)
		if self.die():
			self.rule.removeAgent(plane, x_pos, y_pos)
			return
		
		movesCounter = 0
		for i in range(0, len(moves)):
			if not(moves[i] == w.NOT_POSSIBLE):
				movesCounter += 1
		
		move = None
		if movesCounter == 0:
			return
		else:
			while True:
				rand = randint(0, len(moves) - 1)
				if not (moves[rand] == w.NOT_POSSIBLE):
					move = rand
					break
		
		if move == w.UP:
			self.rule.performMove(plane, x_pos, y_pos, x_pos - 1, y_pos)	
			x_pos = x_pos - 1
		if move == w.DOWN:
			self.rule.performMove(plane, x_pos, y_pos, x_pos + 1, y_pos)
			x_pos = x_pos + 1
		if move == w.LEFT:
			self.rule.performMove(plane, x_pos, y_pos, x_pos, y_pos - 1)
			y_pos = y_pos - 1
		if move == w.RIGHT:
			self.rule.performMove(plane, x_pos, y_pos, x_pos, y_pos + 1)
			y_pos = y_pos + 1
	
		movedMatrix[x_pos][y_pos] = 1
		self.reproduce(plane, x_pos, y_pos, max_x, max_y, movedMatrix)


class WolfAgent(Agent):
	def __init__(self, app, image, rule):
		super(WolfAgent, self).__init__(image, rule)
		self._app = app
		
		wolfMean = int(w.WolfInitialEnergyEntryMean.get()) if w.WolfInitialEnergyEntryMean.get() <> '' else 10
		wolfVariance = int(w.WolfInitialEnergyEntryVariance.get()) if w.WolfInitialEnergyEntryVariance.get() <> '' else 0
		wolfEnergy = round(random_number_generator(wolfMean, wolfVariance))
		wolfEnergy = 0 if wolfEnergy < 0 else wolfEnergy
		
		self._energy = wolfEnergy
		
		wolfMean = int(w.birthdayWolfThresholdEntryMean.get()) if w.birthdayWolfThresholdEntryMean.get() <> '' else 20
		wolfVariance = int(w.birthdayWolfThresholdEntryVariance.get()) if w.birthdayWolfThresholdEntryVariance.get() <> '' else 0
		wolfThreshold = round(random_number_generator(wolfMean, wolfVariance))
		wolfThreshold = 0 if wolfThreshold < 0 else wolfThreshold
		
		self._condition = wolfThreshold
		
	@property
	def condition(self):
		return self._condition
		
	@property
	def app(self):
		return self._app
		
	def move(self, x_pos, y_pos, neighbourHood, max_x, max_y, plane, movedMatrix):
		move_energy_mean = int(w.wolfMoveCostEntryMean.get()) if w.wolfMoveCostEntryMean.get() <> '' else 1
		move_energy_variance = int(w.wolfMoveCostEntryVariance.get()) if w.wolfMoveCostEntryVariance.get() <> '' else 0
		move_energy = round(random_number_generator(move_energy_mean, move_energy_variance))
		move_energy = 0 if move_energy < 0 else move_energy
		
		self._energy -= move_energy
		moves = self.rule.moveSet(x_pos, y_pos, neighbourHood, max_x, max_y)
		if self.die():
			self.rule.removeAgent(plane, x_pos, y_pos)
			return
		
		movesCounter = 0
		for i in range(0, len(moves)):
			if not(moves[i] == w.NOT_POSSIBLE):
				movesCounter += 1
		
		move = None
		if movesCounter == 0:
			return
		else:
			while True:
				rand = randint(0, len(moves) - 1)
				if not (moves[rand] == w.NOT_POSSIBLE):
					move = rand
					break
		
		if move == w.UP:
			self.rule.performMove(self.app, plane, x_pos, y_pos, x_pos - 1, y_pos)
			movedMatrix[x_pos - 1][y_pos] = 1
		if move == w.DOWN:
			self.rule.performMove(self.app, plane, x_pos, y_pos, x_pos + 1, y_pos)
			movedMatrix[x_pos + 1][y_pos] = 1
		if move == w.LEFT:
			self.rule.performMove(self.app, plane, x_pos, y_pos, x_pos, y_pos - 1)
			movedMatrix[x_pos][y_pos - 1] = 1
		if move == w.RIGHT:
			self.rule.performMove(self.app, plane, x_pos, y_pos, x_pos, y_pos + 1)
			movedMatrix[x_pos][y_pos + 1] = 1
			
		
	def reproduce(self, plane, row, column, max_row, max_column, movedMatrix):
		reproduce_set = []
		if row <> 0:
			if not plane.widgets[row - 1][column].image == self.rule.wolf and not plane.widgets[row - 1][column].image == self.rule.rabbit:
				reproduce_set.append((row - 1, column))
		if row <> max_row:
			if not plane.widgets[row + 1][column].image == self.rule.wolf and not plane.widgets[row + 1][column].image == self.rule.rabbit:
				reproduce_set.append((row + 1, column))
		if column <> 0:
			if not plane.widgets[row][column - 1].image == self.rule.wolf and not plane.widgets[row][column - 1].image == self.rule.rabbit:
				reproduce_set.append((row, column - 1))			
		if column <> max_column:
			if not plane.widgets[row][column + 1].image == self.rule.wolf and not plane.widgets[row][column + 1].image == self.rule.rabbit:
				reproduce_set.append((row, column + 1))
		
		if len(reproduce_set) == 0:
			return
		
		rand = randint(0, len(reproduce_set) - 1)
		
		if (self.energy >= self.condition):
			move_tuple = reproduce_set[rand]
			self.addEnergy(-0.5 * self.condition)
			plane.widgets[move_tuple[0]][move_tuple[1]].agent = WolfAgent(self.app, self.image, self.rule)
			plane.widgets[move_tuple[0]][move_tuple[1]].image = self.rule.wolf
			plane.widgets[move_tuple[0]][move_tuple[1]].configure(image = self.rule.wolf)
			movedMatrix[move_tuple[0]][move_tuple[1]] = 1


class GrassAgent(Agent):
	def __init__(self, app, image, rule):
		super(GrassAgent, self).__init__(image, None)
		self._app = app
		
		grassMean = int(w.grassEnergyEntryMean.get()) if w.grassEnergyEntryMean.get() <> '' else 1
		grassVariance = int(w.grassEnergyEntryVariance.get()) if w.grassEnergyEntryVariance.get() <> '' else 0
		grassEnergy = round(random_number_generator(grassMean, grassVariance))
		grassEnergy = 0 if grassEnergy < 0 else grassEnergy
		
		self._energy = grassEnergy
	
	@property
	def app(self):
		return self._app
	
	@property
	def energy(self):
		return self._energy
		
	def move(self):
		return None
