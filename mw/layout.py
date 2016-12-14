import Tkinter as tk
import os
import PIL
from PIL import ImageTk, Image
from random import randint
import time
import copy


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
		pass
		
	def moveSet(self, x_pos, y_pos, neighbourHood, max_x, max_y):
		moveset = [self.POSSIBLE] * 4
		if (x_pos == 0):
			moveset[self.LEFT] = self.NOT_POSSIBLE
		if (x_pos == max_x):
			moveset[self.RIGHT] = self.NOT_POSSIBLE
		if (y_pos == 0):
			moveset[self.UP] = self.NOT_POSSIBLE
		if (y_pos == max_y):
			moveset[self.DOWN] = self.NOT_POSSIBLE
		return moveset
		
	def performMove(self, plane, src_x ,src_y, dest_x, dest_y):
		pass

class WolfRule(Rule):
	pass
		
class RabbitRule(Rule):	
	def performMove(self, plane, src_x, src_y, dest_x, dest_y):
		if plane.widgets[dest_x][dest_y].agent == None:	
			plane.widgets[dest_x][dest_y].agent = plane.widgets[src_x][src_y].agent
			plane.widgets[dest_x][dest_y].image = plane.widgets[src_x][src_y].image
			plane.widgets[dest_x][dest_y].configure(image = plane.widgets[src_x][src_y].image)
			plane.widgets[src_x][src_y].configure(image = '')
			plane.widgets[src_x][src_y].agent = None
			plane.widgets[src_x][src_y].image = None

class App(object):
	def __init__(self, master):
		self._master = master
		rabbit_path = os.getcwd() + '/static/rabbit.jpg'
		wolf_path = os.getcwd() + '/static/wolf.jpg'
		grass_path = os.getcwd() + '/static/grass.jpg'
		
		master.title("Multiagent systems - rabbitsWolfsGrassWeeds")
		master.minsize(width=800, height=800)
		
		basewidth = 30
		
		button = tk.Button(master, text="Initialize", command=lambda: self.initialize(t, t2))
		button.pack()
		
		button2 = tk.Button(master, text="Run simulation", command=lambda: self.run(t, t2, rabbit, wolf, grass))
		button2.pack()
		
		rabbit = Image.open(rabbit_path)
		grass = Image.open(grass_path)
		wolf = Image.open(wolf_path)
		
		rabbit = rabbit.resize((40, 40), PIL.Image.ANTIALIAS)
		rabbit = ImageTk.PhotoImage(rabbit)
		
		grass = grass.resize((40, 40), PIL.Image.ANTIALIAS)
		grass = ImageTk.PhotoImage(grass)
		
		wolf = wolf.resize((40, 40), PIL.Image.ANTIALIAS)
		wolf = ImageTk.PhotoImage(wolf)
		
		t = SimpleTable(master, 10, 10)
		t.pack(side="top", fill="x")
		
		t2 = SimpleTable(master, 10, 10)
		
		birthThreshold = 10
		energy_for_move = 0.5
		grass_energy = 1
		
		t2.randomPlacement(rabbit, 5, RabbitAgent(rabbit, RabbitRule(), birthThreshold, energy_for_move))
		t2.randomPlacement(grass, 5, GrassAgent(grass, None, grass_energy))
		t2.randomPlacement(wolf, 5, WolfAgent(wolf, WolfRule()))
		
		t.destroy()
		t2.pack()
		
		steps = 1
		
		#for i in range(0, steps):
		#	t2, t = t, t2
		#	t2 = SimpleTable(master, 10, 10)
		#
		#	t2.randomPlacement(rabbit, 5)
		#	t2.randomPlacement(grass, 5)
		#	t2.randomPlacement(wolf, 5)
		#	
		#	t.destroy()
		#	t2.pack()
	
	@property
	def master(self):
		return self._master
	
	def run(self, t, t2, rabbit, wolf, grass):
		print(self)
		steps = 3
		t2, t = t, t2
		for i in range(0, steps):
			
			for i in range(0, len(t.widgets)):
				for j in range(0, len(t.widgets[i])):
					if hasattr(t.widgets[i][j], 'image'):
						print(i, j)
						neighbours = [None] * 4
						if not (i == 0):
							neighbours[Rule.UP] = t.widgets[i-1][j].image
						if not (i == len(t.widgets) - 1):
							neighbours[Rule.DOWN] = t.widgets[i+1][j].image
						if not (j == 0):
							neighbours[Rule.LEFT] = t.widgets[i][j-1].image
						if not (j == len(t.widgets[i]) - 1):
							neighbours[Rule.RIGHT] = t.widgets[i][j+1].image
						if t.widgets[i][j].image == rabbit:
							t.widgets[i][j].agent.move(i, j, neighbours, len(t.widgets), len(t.widgets[i]), t)
						print('Row: ' + str(i) + ' Col: ' + str(j))
						
			#t2 = copy.deepcopy(t)		
			#t.destroy()
			#t2.pack()
			self.master.update()
			time.sleep(1)

class Agent(object):
	def __init__(self, image, rule):
		self._image = image
		self._moveRule = rule
		self._energy = 0
		
	@property
	def image(self):
		return self._image
		
	@property
	def rule(self):
		return self._moveRule
	
	@property
	def energy(self):
		return self._energy
	
	def move(self, x_pos, y_pos, neighbourHood, max_x, max_y, plane):
		pass
		
class RabbitAgent(Agent):
	def __init__(self, image, rule, birthThreshold, energy_for_move):
		super(RabbitAgent, self).__init__(image, rule)
		self._birthThreshold = birthThreshold
		self._energy_for_move = energy_for_move
	
	@property
	def birthThreshold(self):
		return self._birthThreshold
		
	@property
	def energy_for_move(self):
		return self._energy_for_move
	
	def reproduce(self):
		if (self.energy >= self.birthThreshold):
			return RabbitAgent(self.image, self.moveRule, self.birthThreshold)
		return None
	
	def move(self, x_pos, y_pos, neighbourHood, max_x, max_y, plane):
		moves = self.rule.moveSet(x_pos, y_pos, neighbourHood, max_x, max_y)
		movesCounter = 0
		for i in range(0, len(moves)):
			if not(moves[i] == Rule.NOT_POSSIBLE):
				movesCounter += 1
		
		move = None
		if movesCounter == 0:
			self.energy -= self.energy_for_move
		else:
			while True:
				rand = randint(0, len(moves) - 1)
				if not (moves[rand] == Rule.NOT_POSSIBLE):
					move = rand
					break
		
		if rand == Rule.UP:
			self.rule.performMove(plane, x_pos, y_pos, x_pos, y_pos - 1)
		if rand == Rule.DOWN:
			self.rule.performMove(plane, x_pos, y_pos, x_pos, y_pos + 1)
		if rand == Rule.LEFT:
			self.rule.performMove(plane, x_pos, y_pos, x_pos - 1, y_pos)
		if rand == Rule.RIGHT:
			self.rule.performMove(plane, x_pos, y_pos, x_pos + 1, y_pos)
	
	def die(self):
		if (self.energy < 0):
			return True
		return False
	
class WolfAgent(Agent):
	pass
	
class GrassAgent(Agent):
	def __init__(self, image, rule, energy):
		super(GrassAgent, self).__init__(image, None)
		self._energy = energy
		
	@property
	def energy(self):
		return self._energy
		
	def move(self):
		return None
			
class SimpleTable(tk.Frame):
	def __init__(self, parent, rows=10, columns=10):
		# use black background so it "peeks through" to 
		# form grid lines
		tk.Frame.__init__(self, parent, background="black")
		self._widgets = []
		self._rows = rows
		self._columns = columns
		for row in range(rows):
			current_row = []
			for column in range(columns):
				label = tk.Label(self, width=4, height=2)
				label.grid(row=row, column=column, sticky="nsew", padx=2, pady=2)
				label.image = None
				label.agent = None
				current_row.append(label)
			self._widgets.append(current_row)

		for column in range(columns):
			self.grid_columnconfigure(column, weight=1)

	@property
	def columns(self):
		return self._columns
		
	@property
	def rows(self):
		return self._rows
	
	@property
	def widgets(self):	
		return self._widgets
	
	def set(self, row, column, value):
		widget = self._widgets[row][column]
		widget.configure(text=value)	
	
	def randomPlacement(self, image, counter, agent):
		while (counter > 0):
			print('elo')
			randRow = randint(0, self.rows - 1)
			randCol = randint(0, self.columns - 1)
			if (self._widgets[randRow][randCol].image is None):
				self._widgets[randRow][randCol].configure(image = image)
				self._widgets[randRow][randCol].image = image
				self._widgets[randRow][randCol].agent = agent
				counter -= 1
	
if __name__ == "__main__":
	root = tk.Tk()
	app = App(root)
	root.mainloop()