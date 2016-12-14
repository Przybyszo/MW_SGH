import Tkinter as tk
import os
import PIL
from PIL import ImageTk, Image
from random import randint
import time
import copy
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure


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
	
	def __init__(self, rabbit, wolf, grass, wolf_in_grass, empty):
		self._rabbit = rabbit
		self._wolf = wolf
		self._grass = grass
		self._wolf_in_grass = wolf_in_grass
		self._empty = empty
		
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
	def moveset(self, x_pos, y_pos, neighbourHood, max_x, max_y, rabbit, wolf, grass):
		moveset = super(WolfRule, self).moveset(x_pos, y_pos, neighbourHood, max_x, max_y)
		for i in range(self.LEFT, self.DOWN + 1):
			if neighbour[i] == self.wolf:
				moveset[i] == NOT_POSSIBLE		
	
	def performMove(self, plane, src_x, src_y, dest_x, dest_y):
		if plane.widgets[dest_x][dest_y].agent == self.empty or plane.widgets[dest_x][dest_y].image == self.rabbit:	
			if plane.widgets[src_x][src_y].image == self.wolf_in_grass:
				plane.widgets[dest_x][dest_y].agent = plane.widgets[src_x][src_y].agent
				plane.widgets[dest_x][dest_y].image = self.wolf
				plane.widgets[dest_x][dest_y].configure(image = self.wolf)
				plane.widgets[src_x][src_y].configure(image = self.grass)
				#GRASS_ENERGY!!!
				grass_energy = 10
				plane.widgets[src_x][src_y].agent = GrassAgent(self.grass, None, grass_energy)
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
				#GRASS_ENERGY!!!
				grass_energy = 10
				plane.widgets[src_x][src_y].agent = GrassAgent(self.grass, None, grass_energy)
				plane.widgets[src_x][src_y].image = self.grass					
			else:
				plane.widgets[dest_x][dest_y].agent = plane.widgets[src_x][src_y].agent
				plane.widgets[dest_x][dest_y].image = self.wolf_in_grass
				plane.widgets[dest_x][dest_y].configure(image = self.wolf_in_grass)
				plane.widgets[src_x][src_y].configure(image = self.empty)
				plane.widgets[src_x][src_y].agent = None
				plane.widgets[src_x][src_y].image = self.empty
		
class RabbitRule(Rule):	
	def moveset(self, x_pos, y_pos, neighbourHood, max_x, max_y):
		moveset = super(RabbitRule, self).moveset(x_pos, y_pos, neighbourHood, max_x, max_y)
		for i in range(self.LEFT, self.DOWN + 1):
			if neighbour[i] == self.rabbit or neighbour[i] == self.wolf:
				moveset[i] == NOT_POSSIBLE		
		
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

class App(object):
	def __init__(self, master):
		self._master = master
		rabbit_path = os.getcwd() + '/static/rabbit.jpg'
		wolf_path = os.getcwd() + '/static/wolf.jpg'
		grass_path = os.getcwd() + '/static/grass.jpg'
		wolf_in_grass_path = os.getcwd() + '/static/wolf_in_grass.jpg'
		empty_path = os.getcwd() + '/static/black.jpg'
		
		master.title("Multiagent systems - rabbitsWolfsGrassWeeds")
		master.minsize(width=800, height=800)
		
		basewidth = 30
		
		grass_energy = 10
		
		button = tk.Button(master, text="Initialize", command=lambda: self.initialize(t, t2, rabbit, wolf, grass, wolf_in_grass, grass_energy, empty))
		button.pack()
		
		button2 = tk.Button(master, text="Run simulation", command=lambda: self.run(t, t2, rabbit, wolf, grass, wolf_in_grass, grass_energy, empty, a, canvas))
		button2.pack()
		
		rabbit = Image.open(rabbit_path)
		grass = Image.open(grass_path)
		wolf = Image.open(wolf_path)
		wolf_in_grass = Image.open(wolf_in_grass_path)
		empty = Image.open(empty_path)
		
		rabbit = rabbit.resize((40, 40), PIL.Image.ANTIALIAS)
		rabbit = ImageTk.PhotoImage(rabbit)
		
		grass = grass.resize((40, 40), PIL.Image.ANTIALIAS)
		grass = ImageTk.PhotoImage(grass)
		
		wolf = wolf.resize((40, 40), PIL.Image.ANTIALIAS)
		wolf = ImageTk.PhotoImage(wolf)
		
		wolf_in_grass = wolf_in_grass.resize((40, 40), PIL.Image.ANTIALIAS)
		wolf_in_grass = ImageTk.PhotoImage(wolf_in_grass)
		
		empty = empty.resize((40, 40), PIL.Image.ANTIALIAS)
		empty = ImageTk.PhotoImage(empty)
		
		t = SimpleTable(master, empty, 10, 10)
		t.pack(side="top", fill="x")
		
		t2 = SimpleTable(master, empty, 10, 10)
		
		t.destroy()
		t2.pack()
		
		f = Figure(figsize=(5, 5), dpi=100)
		a = f.add_subplot(111)
		a.set_xlim([0, 100])
		a.set_ylim([0, 50])
		canvas = FigureCanvasTkAgg(f, master)
		canvas.show()
		canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		
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
	
	def initialize(self, t, t2, rabbit, wolf, grass, wolf_in_grass, grass_energy, empty):
		birthThreshold = 10
		energy_for_move = 0.5
		rabbit_init_energy = 10
		
		t2.randomPlacement(rabbit, 5, RabbitAgent(rabbit, RabbitRule(rabbit, wolf, grass, wolf_in_grass, empty), birthThreshold, energy_for_move, rabbit_init_energy))
		t2.randomPlacement(grass, 5, GrassAgent(grass, None, grass_energy))
		t2.randomPlacement(wolf, 5, WolfAgent(wolf, WolfRule(rabbit, wolf, grass, wolf_in_grass, empty)))
	
	@property
	def master(self):
		return self._master
	
	def run(self, t, t2, rabbit, wolf, grass, wolf_in_grass, grass_energy, empty, a, canvas):
		
		x = [0]
		y = [5]
		
		steps = 200
		t2, t = t, t2
		for k in range(0, steps):
			movedMatrix = [[0 for m in range(0, len(t.widgets[n]))] for n in range(0, len(t.widgets))] 
			for i in range(0, len(t.widgets)):
				for j in range(0, len(t.widgets[i])):
					if hasattr(t.widgets[i][j], 'image'):
						neighbours = [None] * 4
						if not (i == 0):
							neighbours[Rule.UP] = t.widgets[i-1][j].image
						if not (i == len(t.widgets) - 1):
							neighbours[Rule.DOWN] = t.widgets[i+1][j].image
						if not (j == 0):
							neighbours[Rule.LEFT] = t.widgets[i][j-1].image
						if not (j == len(t.widgets[i]) - 1):
							neighbours[Rule.RIGHT] = t.widgets[i][j+1].image
						if t.widgets[i][j].image == rabbit or t.widgets[i][j].image == wolf or t.widgets[i][j].image == wolf_in_grass:
							if (movedMatrix[i][j] == 0):
								t.widgets[i][j].agent.move(i, j, neighbours, len(t.widgets) - 1, len(t.widgets[i]) - 1, t, movedMatrix)
						
			#t2 = copy.deepcopy(t)		
			#t.destroy()
			#t2.pack()
			rabbitsNo = self.countRabbits(t, rabbit)
			x.append(k + 1)
			y.append(rabbitsNo)
			print(x)
			print(y)
			print('---')
			a.clear()
			a.plot(x, y)
			if k <= 100:
				a.set_xlim([0, 100])
			else:
				a.set_xlim([k - 100, k])
			a.set_ylim([0, len(t.widgets[i]) * len(t.widgets)])
			canvas.draw()
			time.sleep(1)
			t.randomPlacement(grass, 5, GrassAgent(grass, None, grass_energy))
			#self.master.update()
			#time.sleep(0.001)
	
	def countRabbits(self, t, rabbit):
		counter = 0
		for i in range(0, len(t.widgets)):
				for j in range(0, len(t.widgets[i])):
					if hasattr(t.widgets[i][j], 'image'):
						if t.widgets[i][j].image == rabbit:
							counter += 1
		return counter

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
	
	def move(self, x_pos, y_pos, neighbourHood, max_x, max_y, plane, movedMatrix):
		pass
		
class RabbitAgent(Agent):
	def __init__(self, image, rule, birthThreshold, energy_for_move, energy):
		super(RabbitAgent, self).__init__(image, rule)
		self._birthThreshold = birthThreshold
		self._energy_for_move = energy_for_move
		self._energy = energy
	
	@property
	def birthThreshold(self):
		return self._birthThreshold
		
	def addEnergy(self, energy):
		self._energy += energy
		
	@property
	def energy_for_move(self):
		return self._energy_for_move
	
	def reproduce(self, plane, row, column, max_row, max_column, movedMatrix):
		reproduce_set = []
		if row == max_row:
			if not (plane.widgets[row - 1][column].image == self.rule.wolf or plane.widgets[row - 1][column].image == self.rule.rabbit):
				reproduce_set.append((row - 1, column))
		if row == 0:
			if not (plane.widgets[row + 1][column].image == self.rule.wolf or plane.widgets[row + 1][column].image == self.rule.rabbit):
				reproduce_set.append((row + 1, column))
		if column == max_column:
			if not (plane.widgets[row][column - 1].image == self.rule.wolf or plane.widgets[row][column - 1].image == self.rule.rabbit):
				reproduce_set.append((row, column - 1))			
		if column == 0:
			if not (plane.widgets[row][column + 1].image == self.rule.wolf or plane.widgets[row][column + 1].image == self.rule.rabbit):
				reproduce_set.append((row, column + 1))
		
		if len(reproduce_set) == 0:
			return
		
		rand = randint(0, len(reproduce_set) - 1)
		
		if (self.energy >= self.birthThreshold):
			move_tuple = reproduce_set[rand]
			#RABBIT DEFAULT ENERGY
			self.addEnergy(-self.birthThreshold)
			plane.widgets[move_tuple[0]][move_tuple[1]].agent = RabbitAgent(self.image, self.rule, self.birthThreshold, self.energy_for_move, 10)
			plane.widgets[move_tuple[0]][move_tuple[1]].image = self.rule.rabbit
			movedMatrix[move_tuple[0]][move_tuple[1]] = 1
			
	def move(self, x_pos, y_pos, neighbourHood, max_x, max_y, plane, movedMatrix):
		self._energy -= self.energy_for_move
		moves = self.rule.moveSet(x_pos, y_pos, neighbourHood, max_x, max_y)
		if self.die():
			self.rule.removeAgent(plane, x_pos, y_pos)
			return
		
		movesCounter = 0
		for i in range(0, len(moves)):
			if not(moves[i] == Rule.NOT_POSSIBLE):
				movesCounter += 1
		
		move = None
		if movesCounter == 0:
			return
		else:
			while True:
				rand = randint(0, len(moves) - 1)
				if not (moves[rand] == Rule.NOT_POSSIBLE):
					move = rand
					break
		
		if move == Rule.UP:
			self.rule.performMove(plane, x_pos, y_pos, x_pos - 1, y_pos)
			
			x_pos = x_pos - 1
		if move == Rule.DOWN:
			self.rule.performMove(plane, x_pos, y_pos, x_pos + 1, y_pos)
			x_pos = x_pos + 1
			
		if move == Rule.LEFT:
			self.rule.performMove(plane, x_pos, y_pos, x_pos, y_pos - 1)
			y_pos = y_pos - 1
		if move == Rule.RIGHT:
			self.rule.performMove(plane, x_pos, y_pos, x_pos, y_pos + 1)
			y_pos = y_pos + 1
	
		movedMatrix[x_pos][y_pos] = 1
		self.reproduce(plane, x_pos, y_pos, max_x, max_y, movedMatrix)
	
	def die(self):
		if (self.energy < 0):
			return True
		return False
	
class WolfAgent(Agent):
	def __init__(self, image, rule):
		super(WolfAgent, self).__init__(image, rule)
		
	def move(self, x_pos, y_pos, neighbourHood, max_x, max_y, plane, movedMatrix):
		moves = self.rule.moveSet(x_pos, y_pos, neighbourHood, max_x, max_y)
		
		movesCounter = 0
		for i in range(0, len(moves)):
			if not(moves[i] == Rule.NOT_POSSIBLE):
				movesCounter += 1
		
		move = None
		if movesCounter == 0:
			return
		else:
			while True:
				rand = randint(0, len(moves) - 1)
				if not (moves[rand] == Rule.NOT_POSSIBLE):
					move = rand
					break
		
		if move == Rule.UP:
			self.rule.performMove(plane, x_pos, y_pos, x_pos - 1, y_pos)
			movedMatrix[x_pos - 1][y_pos] = 1
		if move == Rule.DOWN:
			self.rule.performMove(plane, x_pos, y_pos, x_pos + 1, y_pos)
			movedMatrix[x_pos + 1][y_pos]
		if move == Rule.LEFT:
			self.rule.performMove(plane, x_pos, y_pos, x_pos, y_pos - 1)
			movedMatrix[x_pos][y_pos - 1]
		if move == Rule.RIGHT:
			self.rule.performMove(plane, x_pos, y_pos, x_pos, y_pos + 1)
			movedMatrix[x_pos][y_pos + 1]
	
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
	def __init__(self, parent, empty, rows=10, columns=10):
		# use black background so it "peeks through" to 
		# form grid lines
		tk.Frame.__init__(self, parent, background="black")
		self._widgets = []
		self._rows = rows
		self._columns = columns
		self._empty = empty
		for row in range(rows):
			current_row = []
			for column in range(columns):
				label = tk.Label(self, width=40, height=40, relief="ridge")
				label.grid(row=row, column=column, sticky="wnes", padx=2, pady=2)
				label.configure(image = self.empty)
				label.image = empty
				label.agent = None
				current_row.append(label)
			self._widgets.append(current_row)

		for column in range(columns):
			self.grid_columnconfigure(column, weight=4)

	@property
	def empty(self):
		return self._empty
			
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
		iterations = 1000
		while (counter > 0 and iterations > 0):
			iterations -= 1
			randRow = randint(0, self.rows - 1)
			randCol = randint(0, self.columns - 1)
			if (self._widgets[randRow][randCol].image == self.empty):
				self._widgets[randRow][randCol].configure(image = image)
				self._widgets[randRow][randCol].image = image
				self._widgets[randRow][randCol].agent = copy.copy(agent)
				counter -= 1
	
if __name__ == "__main__":
	root = tk.Tk()
	app = App(root)
	root.mainloop()