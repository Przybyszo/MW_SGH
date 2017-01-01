import Tkinter as tk
import os
import PIL
from PIL import ImageTk, Image
from random import randint
import time
import copy
import matplotlib
import configparser
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import itertools
import world
import random


def random_number_generator(mean, variance):
	if world.distribution == 'NORMAL':
		return random.gauss(mean, variance)
	return None

class resource_cl(object):
	newid = itertools.count().next
	def __init__(self):
		self._id = resource_cl.newid()
		
	@property
	def id(self):
		return self._id


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

def stop_simulation(run_button, stop_button):
	run_button['state'] = 'active'
	stop_button['state'] = 'disabled'
	world.simulation_stop = True
			
class App(object):
	def __init__(self, master):
		self._master = master
		world.app = self
		config = configparser.ConfigParser()
		config_path = os.getcwd() + '/config/config.ini'
		config.read(config_path)
		
		world.distribution = config.get('SIMULATION', 'DISTRIBUTION')
		rabbit_path = os.getcwd() + config.get('RABBIT', 'RELATIVE_PATH')
		wolf_path = os.getcwd() + config.get('WOLF', 'RELATIVE_PATH')
		grass_path = os.getcwd() + config.get('GRASS', 'RELATIVE_PATH')
		wolf_in_grass_path = os.getcwd() + config.get('WOLF_IN_GRASS', 'RELATIVE_PATH')
		empty_path = os.getcwd() + config.get('EMPTY', 'RELATIVE_PATH')
		
		master.title("Multiagent systems - rabbitsWolfsGrass")
		master.minsize(width=800, height=800)
		
		up = tk.Frame(master)

		up.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		up_left = tk.Frame(master)
		up_left.pack(in_=up, side=tk.LEFT, fill=tk.BOTH, expand=True)
		up_center = tk.Frame(master)
		up_center.pack(in_=up, side=tk.LEFT, fill=tk.BOTH, expand=True)
		
		up_right = tk.Frame(master)
		up_right.pack(in_=up, side=tk.RIGHT, fill=tk.BOTH)
		
		button = tk.Button(master, height=4, width=20, text="Initialize", command=lambda: self.initialize(button2, t, t2, rabbit, wolf, grass, wolf_in_grass, empty))
		button.pack(in_=up_right, fill='x', padx=200, pady=50)
		
		button2 = tk.Button(master, height=4, width=20, state='disabled', text="Run simulation", command=lambda: self.run(button2, button3, t, t2, rabbit, wolf, grass, wolf_in_grass, empty, a, canvas, a2, canvas2, a3, canvas3))
		button2.pack(in_=up_right, fill='x', padx=200, pady=50)
		
		button3 = tk.Button(master, height=4, width=20, text="Stop simulation", command=lambda: stop_simulation(button2, button3), state='disabled')
		button3.pack(in_=up_right, fill='x', padx=200, pady=50)
		
		up_left_first = tk.Frame(master, bd=1, relief='sunken')
		up_left_first.pack(in_=up_left, fill='x')
		
		mean = tk.StringVar()
		mean.set("Mean:")
		
		variance = tk.StringVar()
		variance.set("Variance:")
		
		rabbitInitText = tk.StringVar()
		rabbitInitText.set("Enter initial number of rabbits")
		rabbitInitLabel=tk.Label(master, textvariable=rabbitInitText, height=2)
		rabbitInitLabel.grid(row=2, sticky='w')
		rabbitInitLabel.pack(in_=up_left_first, side="left")

		rabbitInitLabel2=tk.Label(master, textvariable=mean, height=2)
		rabbitInitLabel2.grid(row=2, sticky='w')
		rabbitInitLabel2.pack(in_=up_left_first, side="left", padx=10)
		
		rabbitInitEntry=tk.Entry(master,textvariable=tk.StringVar(None),width=10)
		rabbitInitEntry.grid(row=2, sticky='w')
		rabbitInitEntry.pack(in_=up_left_first, side="left")

		rabbitInitLabel3=tk.Label(master, textvariable=variance, height=2)
		rabbitInitLabel3.grid(row=2, sticky='w')
		rabbitInitLabel3.pack(in_=up_left_first, side="left", padx=10)
		
		rabbitInitEntry2=tk.Entry(master,textvariable=tk.StringVar(None),width=10)
		rabbitInitEntry2.grid(row=2, sticky='w')
		rabbitInitEntry2.pack(in_=up_left_first, side="left")
		
		self._rabbitInitEntry = rabbitInitEntry
		world.rabbitInitEntryMean = rabbitInitEntry
		world.rabbitInitEntryVariance = rabbitInitEntry2
		
		up_left_first_2 = tk.Frame(master, bd=1, relief='sunken')
		up_left_first_2.pack(in_=up_left, fill='x')
		
		wolfInitText = tk.StringVar()
		wolfInitText.set("Enter initial number of wolfs")
		wolfInitLabel=tk.Label(master, textvariable=wolfInitText, height=2)
		wolfInitLabel.grid(row=2, column=3)
		wolfInitLabel.pack(in_=up_left_first_2, side="left", fill='x')

		wolfInitLabel2=tk.Label(master, textvariable=mean, height=2)
		wolfInitLabel2.grid(row=2, sticky='w')
		wolfInitLabel2.pack(in_=up_left_first_2, side="left", padx=10)
		
		wolfInitEntry=tk.Entry(master,textvariable=tk.StringVar(None),width=10)
		wolfInitEntry.grid(row=2, sticky='w')
		wolfInitEntry.pack(in_=up_left_first_2, side="left")		
		
		wolfInitLabel3=tk.Label(master, textvariable=variance, height=2)
		wolfInitLabel3.grid(row=2, sticky='w')
		wolfInitLabel3.pack(in_=up_left_first_2, side="left", padx=10)
		
		wolfInitEntry2=tk.Entry(master,textvariable=tk.StringVar(None),width=10)
		wolfInitEntry2.grid(row=2, sticky='w')
		wolfInitEntry2.pack(in_=up_left_first_2, side="left")
		
		self._wolfInitEntry = wolfInitEntry
		world.wolfInitEntryMean = wolfInitEntry
		world.wolfInitEntryVariance = wolfInitEntry2
		
		up_left_second = tk.Frame(master, bd=1, relief='sunken')
		up_left_second.pack(in_=up_left, fill='x')
		
		grassInitText = tk.StringVar()
		grassInitText.set("Enter grass growing rate per step")
		grassInitLabel=tk.Label(master, textvariable=grassInitText, height=2)
		grassInitLabel.pack(in_=up_left_second, side="left")

		grassInitLabel2=tk.Label(master, textvariable=mean, height=2)
		grassInitLabel2.grid(row=2, sticky='w')
		grassInitLabel2.pack(in_=up_left_second, side="left", padx=10)
		
		grassInitEntry=tk.Entry(master,textvariable=tk.StringVar(None),width=10)
		grassInitEntry.pack(in_=up_left_second, side="left")

		grassInitLabel3=tk.Label(master, textvariable=variance, height=2)
		grassInitLabel3.grid(row=2, sticky='w')
		grassInitLabel3.pack(in_=up_left_second, side="left", padx=10)
		
		grassInitEntry2=tk.Entry(master,textvariable=tk.StringVar(None),width=10)
		grassInitEntry2.grid(row=2, sticky='w')
		grassInitEntry2.pack(in_=up_left_second, side="left")
		
		self._grassInitEntry = grassInitEntry
		world.grassInitEntryMean = grassInitEntry
		world.grassInitEntryVariance = grassInitEntry2
		
		up_left_second_2= tk.Frame(master, bd=1, relief='sunken')
		up_left_second_2.pack(in_=up_left, fill='x')
		
		birthdayRabbitThresholdText = tk.StringVar()
		birthdayRabbitThresholdText.set("Enter the rabbit birthday energy threshold")
		birthdayRabbitThresholdLabel=tk.Label(master, textvariable=birthdayRabbitThresholdText, height=2)
		birthdayRabbitThresholdLabel.pack(in_=up_left_second_2, side="left")

		birthdayRabbitThresholdLabel2=tk.Label(master, textvariable=mean, height=2)
		birthdayRabbitThresholdLabel2.grid(row=2, sticky='w')
		birthdayRabbitThresholdLabel2.pack(in_=up_left_second_2, side="left", padx=10)
		
		birthdayRabbitThresholdEntry=tk.Entry(master,textvariable=tk.StringVar(None),width=10)
		birthdayRabbitThresholdEntry.pack(in_=up_left_second_2, side="left")	

		birthdayRabbitThresholdLabel3=tk.Label(master, textvariable=variance, height=2)
		birthdayRabbitThresholdLabel3.grid(row=2, sticky='w')
		birthdayRabbitThresholdLabel3.pack(in_=up_left_second_2, side="left", padx=10)
		
		birthdayRabbitThresholdEntry2=tk.Entry(master,textvariable=tk.StringVar(None),width=10)
		birthdayRabbitThresholdEntry2.grid(row=2, sticky='w')
		birthdayRabbitThresholdEntry2.pack(in_=up_left_second_2, side="left")
		
		self._birthdayRabbitThresholdEntry = birthdayRabbitThresholdEntry
		world.birthdayRabbitThresholdEntryMean = birthdayRabbitThresholdEntry
		world.birthdayRabbitThresholdEntryVariance = birthdayRabbitThresholdEntry2
		
		up_left_third = tk.Frame(master, bd=1, relief='sunken')
		up_left_third.pack(in_=up_left, fill='x')
		
		rabbitMoveCostText = tk.StringVar()
		rabbitMoveCostText.set("Enter rabbit energy cost for movement")
		rabbitMoveCostLabel=tk.Label(master, textvariable=rabbitMoveCostText, height=2)
		rabbitMoveCostLabel.pack(in_=up_left_third, side="left")

		rabbitMoveCostLabel2=tk.Label(master, textvariable=mean, height=2)
		rabbitMoveCostLabel2.grid(row=2, sticky='w')
		rabbitMoveCostLabel2.pack(in_=up_left_third, side="left", padx=10)
		
		rabbitMoveCostEntry=tk.Entry(master,textvariable=tk.StringVar(None),width=10)
		rabbitMoveCostEntry.pack(in_=up_left_third, side="left")

		rabbitMoveCostLabel3=tk.Label(master, textvariable=variance, height=2)
		rabbitMoveCostLabel3.grid(row=2, sticky='w')
		rabbitMoveCostLabel3.pack(in_=up_left_third, side="left", padx=10)
		
		rabbitMoveCostEntry2=tk.Entry(master,textvariable=tk.StringVar(None),width=10)
		rabbitMoveCostEntry2.grid(row=2, sticky='w')
		rabbitMoveCostEntry2.pack(in_=up_left_third, side="left")
		
		self._rabbitMoveCostEntry = rabbitMoveCostEntry
		world.rabbitMoveCostEntryMean = rabbitMoveCostEntry
		world.rabbitMoveCostEntryVariance = rabbitMoveCostEntry2
		
		up_left_third_2 = tk.Frame(master, bd=1, relief='sunken')
		up_left_third_2.pack(in_=up_left, fill='x')
		
		RabbitInitialEnergyText = tk.StringVar()
		RabbitInitialEnergyText.set("Enter the rabbit initial energy")
		RabbitInitialEnergyLabel=tk.Label(master, textvariable=RabbitInitialEnergyText, height=2)
		RabbitInitialEnergyLabel.pack(in_=up_left_third_2, side="left")

		RabbitInitialEnergyLabel2=tk.Label(master, textvariable=mean, height=2)
		RabbitInitialEnergyLabel2.grid(row=2, sticky='w')
		RabbitInitialEnergyLabel2.pack(in_=up_left_third_2, side="left", padx=10)
		
		RabbitInitialEnergyEntry=tk.Entry(master,textvariable=tk.StringVar(None),width=10)
		RabbitInitialEnergyEntry.pack(in_=up_left_third_2, side="left")	

		RabbitInitialEnergyLabel3=tk.Label(master, textvariable=variance, height=2)
		RabbitInitialEnergyLabel3.grid(row=2, sticky='w')
		RabbitInitialEnergyLabel3.pack(in_=up_left_third_2, side="left", padx=10)
		
		RabbitInitialEnergyEntry2=tk.Entry(master,textvariable=tk.StringVar(None),width=10)
		RabbitInitialEnergyEntry2.grid(row=2, sticky='w')
		RabbitInitialEnergyEntry2.pack(in_=up_left_third_2, side="left")
		
		self._RabbitInitialEnergyEntry = RabbitInitialEnergyEntry
		world.RabbitInitialEnergyEntryMean = RabbitInitialEnergyEntry
		world.RabbitInitialEnergyEntryVariance = RabbitInitialEnergyEntry2
		
		up_left_forth = tk.Frame(master, bd=1, relief='sunken')
		up_left_forth.pack(in_=up_left, fill='x')
		
		grassEnergyText = tk.StringVar()
		grassEnergyText.set("Enter grass energy boost")
		grassEnergyLabel=tk.Label(master, textvariable=grassEnergyText, height=2)
		grassEnergyLabel.pack(in_=up_left_forth, side="left")

		grassEnergyLabel2=tk.Label(master, textvariable=mean, height=2)
		grassEnergyLabel2.grid(row=2, sticky='w')
		grassEnergyLabel2.pack(in_=up_left_forth, side="left", padx=10)
		
		grassEnergyEntry=tk.Entry(master,textvariable=tk.StringVar(None),width=10)
		grassEnergyEntry.pack(in_=up_left_forth, side="left")
		
		grassEnergyLabel3=tk.Label(master, textvariable=variance, height=2)
		grassEnergyLabel3.grid(row=2, sticky='w')
		grassEnergyLabel3.pack(in_=up_left_forth, side="left", padx=10)
		
		grassEnergyEntry2=tk.Entry(master,textvariable=tk.StringVar(None),width=10)
		grassEnergyEntry2.grid(row=2, sticky='w')
		grassEnergyEntry2.pack(in_=up_left_forth, side="left")
		
		self._grassEnergyEntry = grassEnergyEntry
		world.grassEnergyEntryMean = grassEnergyEntry
		world.grassEnergyEntryVariance = grassEnergyEntry2
		
		up_left_forth_2 = tk.Frame(master, bd=1, relief='sunken')
		up_left_forth_2.pack(in_=up_left, fill='x')
		
		stepsText = tk.StringVar()
		stepsText.set("Enter number of steps")
		stepsLabel=tk.Label(master, textvariable=stepsText, height=2)
		stepsLabel.pack(in_=up_left_forth_2, side="left")

		stepsEntry=tk.Entry(master,textvariable=tk.StringVar(None),width=10)
		stepsEntry.pack(in_=up_left_forth_2, side="left")

		self._stepsEntry = stepsEntry
		world.stepsEntry = stepsEntry
		
		up_left_fifth = tk.Frame(master, bd=1, relief='sunken')
		up_left_fifth.pack(in_=up_left, fill='x')
		
		WolfInitialEnergyText = tk.StringVar()
		WolfInitialEnergyText.set("Enter initial wolf energy")
		WolfInitialEnergyLabel=tk.Label(master, textvariable=WolfInitialEnergyText, height=2)
		WolfInitialEnergyLabel.pack(in_=up_left_fifth, side="left")
		
		WolfInitialEnergyLabel2=tk.Label(master, textvariable=mean, height=2)
		WolfInitialEnergyLabel2.grid(row=2, sticky='w')
		WolfInitialEnergyLabel2.pack(in_=up_left_fifth, side="left", padx=10)
		
		WolfInitialEnergyEntry=tk.Entry(master, textvariable=tk.StringVar(None), width=10)
		WolfInitialEnergyEntry.pack(in_=up_left_fifth, side="left")

		WolfInitialEnergyLabel3=tk.Label(master, textvariable=variance, height=2)
		WolfInitialEnergyLabel3.grid(row=2, sticky='w')
		WolfInitialEnergyLabel3.pack(in_=up_left_fifth, side="left", padx=10)
		
		WolfInitialEnergyEntry2=tk.Entry(master,textvariable=tk.StringVar(None),width=10)
		WolfInitialEnergyEntry2.grid(row=2, sticky='w')
		WolfInitialEnergyEntry2.pack(in_=up_left_fifth, side="left")
		
		self._WolfInitialEnergyEntry = WolfInitialEnergyEntry
		world.WolfInitialEnergyEntryMean = WolfInitialEnergyEntry
		world.WolfInitialEnergyEntryVariance = WolfInitialEnergyEntry2
		
		up_left_fifth_2= tk.Frame(master, bd=1, relief='sunken')
		up_left_fifth_2.pack(in_=up_left, fill='x')
		
		birthdayWolfThresholdText = tk.StringVar()
		birthdayWolfThresholdText.set("Enter the wolf birthday energy threshold")
		birthdayWolfThresholdLabel=tk.Label(master, textvariable=birthdayWolfThresholdText, height=2)
		birthdayWolfThresholdLabel.pack(in_=up_left_fifth_2, side="left")

		birthdayWolfThresholdLabel2=tk.Label(master, textvariable=mean, height=2)
		birthdayWolfThresholdLabel2.grid(row=2, sticky='w')
		birthdayWolfThresholdLabel2.pack(in_=up_left_fifth_2, side="left", padx=10)
		
		birthdayWolfThresholdEntry=tk.Entry(master,textvariable=tk.StringVar(None),width=10)
		birthdayWolfThresholdEntry.pack(in_=up_left_fifth_2, side="left")	
		
		birthdayWolfThresholdLabel3=tk.Label(master, textvariable=variance, height=2)
		birthdayWolfThresholdLabel3.grid(row=2, sticky='w')
		birthdayWolfThresholdLabel3.pack(in_=up_left_fifth_2, side="left", padx=10)
		
		birthdayWolfThresholdEntry2=tk.Entry(master,textvariable=tk.StringVar(None),width=10)
		birthdayWolfThresholdEntry2.grid(row=2, sticky='w')
		birthdayWolfThresholdEntry2.pack(in_=up_left_fifth_2, side="left")
		
		self._birthdayWolfThresholdEntry = birthdayWolfThresholdEntry
		world.birthdayWolfThresholdEntryMean = birthdayWolfThresholdEntry
		world.birthdayWolfThresholdEntryVariance = birthdayWolfThresholdEntry2
		
		up_left_sixth = tk.Frame(master, bd=1, relief='sunken')
		up_left_sixth.pack(in_=up_left, fill='x')
		
		wolfMoveCostText = tk.StringVar()
		wolfMoveCostText.set("Enter wolf energy cost for movement")
		wolfMoveCostLabel=tk.Label(master, textvariable=wolfMoveCostText, height=2)
		wolfMoveCostLabel.pack(in_=up_left_sixth, side="left")

		wolfMoveCostLabel2=tk.Label(master, textvariable=mean, height=2)
		wolfMoveCostLabel2.grid(row=2, sticky='w')
		wolfMoveCostLabel2.pack(in_=up_left_sixth, side="left", padx=10)
		
		wolfMoveCostEntry=tk.Entry(master,textvariable=tk.StringVar(None),width=10)
		wolfMoveCostEntry.pack(in_=up_left_sixth, side="left")

		wolfMoveCostLabel3=tk.Label(master, textvariable=variance, height=2)
		wolfMoveCostLabel3.grid(row=2, sticky='w')
		wolfMoveCostLabel3.pack(in_=up_left_sixth, side="left", padx=10)
		
		wolfMoveCostEntry2=tk.Entry(master,textvariable=tk.StringVar(None),width=10)
		wolfMoveCostEntry2.grid(row=2, sticky='w')
		wolfMoveCostEntry2.pack(in_=up_left_sixth, side="left")
		
		self._wolfMoveCostEntry = wolfMoveCostEntry
		world.wolfMoveCostEntryMean = wolfMoveCostEntry
		world.wolfMoveCostEntryVariance = wolfMoveCostEntry2
		
		rabbit = Image.open(rabbit_path)
		grass = Image.open(grass_path)
		wolf = Image.open(wolf_path)
		wolf_in_grass = Image.open(wolf_in_grass_path)
		empty = Image.open(empty_path)
		
		rabbit = rabbit.resize((40, 40), PIL.Image.ANTIALIAS)
		rabbit = ImageTk.PhotoImage(rabbit)
		world.rabbit = rabbit
		
		grass = grass.resize((40, 40), PIL.Image.ANTIALIAS)
		grass = ImageTk.PhotoImage(grass)
		world.grass = grass
		
		wolf = wolf.resize((40, 40), PIL.Image.ANTIALIAS)
		wolf = ImageTk.PhotoImage(wolf)
		world.wolf = wolf
		
		wolf_in_grass = wolf_in_grass.resize((40, 40), PIL.Image.ANTIALIAS)
		wolf_in_grass = ImageTk.PhotoImage(wolf_in_grass)
		world.wolf_in_grass = wolf_in_grass
		
		empty = empty.resize((40, 40), PIL.Image.ANTIALIAS)
		empty = ImageTk.PhotoImage(empty)
		world.empty = empty
		
		t = SimpleTable(master, empty, 10, 10)
		t.pack(side="top", fill="x")
		
		t2 = SimpleTable(master, empty, 10, 10)
		
		t.destroy()
		t2.pack(in_=up_center)
		
		bottom = tk.Frame(master)
		bottom.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
		
		f = Figure(figsize=(5, 5), dpi=100)
		a = f.add_subplot(111)
		a.set_title("Number of rabbits per iteration step")
		a.set_xlabel('Step no')
		a.set_ylabel('Number of rabbits')
		a.set_xlim([0, 100])
		a.set_ylim([0, len(t.widgets[0]) * len(t.widgets)])
			
		canvas = FigureCanvasTkAgg(f, master)
		canvas.show()
		canvas.get_tk_widget().pack(in_=bottom, side=tk.LEFT, expand=True)
		
		f2 = Figure(figsize=(5, 5), dpi=100)
		a2 = f2.add_subplot(111)
		a2.set_title("Amount of grass per iteration step")
		a2.set_xlabel('Step no')
		a2.set_ylabel('Amount of grass')
		a2.set_xlim([0, 100])
		a2.set_ylim([0, len(t.widgets[0]) * len(t.widgets)])
		
		canvas2 = FigureCanvasTkAgg(f2, master)
		canvas2.show()
		canvas2.get_tk_widget().pack(in_=bottom, side=tk.LEFT, expand=True)
		
		f3 = Figure(figsize=(5, 5), dpi=100)
		a3 = f3.add_subplot(111)
		a3.set_title("Number of wolfs per iteration step")
		a3.set_xlabel('Step no')
		a3.set_ylabel('Number of wolfs')
		a3.set_xlim([0, 100])
		a3.set_ylim([0, len(t.widgets[0]) * len(t.widgets)])
		
		canvas3 = FigureCanvasTkAgg(f3, master)
		canvas3.show()
		canvas3.get_tk_widget().pack(in_=bottom, side=tk.LEFT, expand=True)
		
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
	
	def initialize(self, run_button, t, t2, rabbit, wolf, grass, wolf_in_grass, empty):	
		run_button['state'] = 'active'
		t2.reset(empty)
	
		rabbitMean = int(world.rabbitInitEntryMean.get()) if world.rabbitInitEntryMean.get() <> '' else 5
		rabbitVariance = int(world.rabbitInitEntryVariance.get()) if world.rabbitInitEntryVariance.get() <> '' else 0
		rabbitNo = round(random_number_generator(rabbitMean, rabbitVariance))
		rabbitNo = 0 if rabbitNo < 0 else rabbitNo
		
		wolfMean = int(world.wolfInitEntryMean.get()) if world.wolfInitEntryMean.get() <> '' else 5
		wolfVariance = int(world.wolfInitEntryVariance.get()) if world.wolfInitEntryVariance.get() <> '' else 0
		wolfNo = round(random_number_generator(wolfMean, wolfVariance))
		wolfNo = 0 if wolfNo < 0 else wolfNo
		
		grassMean = int(world.grassInitEntryMean.get()) if world.grassInitEntryMean.get() <> '' else 5
		grassVariance = int(world.grassInitEntryVariance.get()) if world.grassInitEntryVariance.get() <> '' else 0
		grassNo = round(random_number_generator(grassMean, grassVariance))
		grassNo = 0 if grassNo < 0 else grassNo
		
		t2.randomPlacement(rabbit, rabbitNo)
		t2.randomPlacement(wolf, wolfNo)
		t2.randomPlacement(grass, grassNo)
	
	@property
	def master(self):
		return self._master
	
	def run(self, run_button, stop_button, t, t2, rabbit, wolf, grass, wolf_in_grass, empty, a, canvas, a2, canvas2, a3, canvas3):
		run_button['state'] = 'disabled'
		stop_button['state'] = 'active'
		x = [0]
		y = [int(self._rabbitInitEntry.get()) if self._rabbitInitEntry.get() <> '' else 5]
		z = [int(self._grassInitEntry.get()) if self._grassInitEntry.get() <> '' else 5]
		w = [int(self._wolfInitEntry.get()) if self._wolfInitEntry.get() <> '' else 10]
		
		t2, t = t, t2
		for k in range(0, int(self._stepsEntry.get()) if self._stepsEntry.get() <> '' else 200):
			if (world.simulation_stop == True):
				world.simulation_stop = False
				world.x = x
				world.y = y
				world.z = z
				world.w = w
				run_button['state'] = 'active'
				stop_button['state'] = 'disabled'
				break
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
						
			rabbitsNo = self.countRabbits(t, rabbit)
			grassNo = self.countGrass(t, grass, wolf_in_grass)
			wolfNo = self.countWolf(t, wolf, wolf_in_grass)
			x.append(k + 1)
			y.append(rabbitsNo)
			z.append(grassNo)
			w.append(wolfNo)
			a.clear()
			a2.clear()
			a3.clear()
			a.plot(x, y)
			a.set_title("Number of rabbits per iteration step")
			a.set_xlabel('Step no')
			a.set_ylabel('Number of rabbits')
			a2.plot(x, z)
			a2.set_title("Amount of grass per iteration step")
			a2.set_xlabel('Step no')
			a2.set_ylabel('Amount of grass')
			a3.plot(x, w)
			a3.set_title("Number of wolfs per iteration step")
			a3.set_xlabel('Step no')
			a3.set_ylabel('Number of wolfs')
			if k <= 100:
				a.set_xlim([0, 100])
				a2.set_xlim([0, 100])
				a3.set_xlim([0, 100])
			else:
				a.set_xlim([k - 100, k])
				a2.set_xlim([k - 100, k])
				a3.set_xlim([k - 100, k])
			a.set_ylim([0, len(t.widgets[i]) * len(t.widgets)])
			a2.set_ylim([0, len(t.widgets[i]) * len(t.widgets)])
			a3.set_ylim([0, len(t.widgets[i]) * len(t.widgets)])
			canvas.draw()
			canvas2.draw()
			canvas3.draw()
			time.sleep(world.sleep_time)
			
			grassMean = int(world.grassInitEntryMean.get()) if world.grassInitEntryMean.get() <> '' else 5
			grassVariance = int(world.grassInitEntryVariance.get()) if world.grassInitEntryVariance.get() <> '' else 0
			grassNo = round(random_number_generator(grassMean, grassVariance))
			grassNo = 0 if grassNo < 0 else grassNo
			
			t.randomPlacement(grass, grassNo)
			self.master.update()
			
	def countRabbits(self, t, rabbit):
		counter = 0
		for i in range(0, len(t.widgets)):
				for j in range(0, len(t.widgets[i])):
					if hasattr(t.widgets[i][j], 'image'):
						if t.widgets[i][j].image == world.rabbit:
							counter += 1
		return counter

	def countGrass(self, t, grass, wolf_in_grass):
		counter = 0
		for i in range(0, len(t.widgets)):
			for j in range(0, len(t.widgets[i])):
				if hasattr(t.widgets[i][j], 'image'):
					if t.widgets[i][j].image == world.grass or t.widgets[i][j].image == world.wolf_in_grass:
						counter += 1
		return counter
		
	def countWolf(self, t, wolf, wolf_in_grass):
		counter = 0
		for i in range(0, len(t.widgets)):
			for j in range(0, len(t.widgets[i])):
				if hasattr(t.widgets[i][j], 'image'):
					if t.widgets[i][j].image == world.wolf or t.widgets[i][j].image == world.wolf_in_grass:
						counter += 1
		return counter
		
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
		self._energy = int(app._RabbitInitialEnergyEntry.get()) if app._RabbitInitialEnergyEntry.get() <> '' else 5
		self._app = app
		self.condition = int(app._birthdayRabbitThresholdEntry.get()) if app._birthdayRabbitThresholdEntry.get() <> '' else 10
	
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
		self._energy -= int(self.app._rabbitMoveCostEntry.get()) if self.app._rabbitMoveCostEntry.get() <> '' else 0.5
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


class WolfAgent(Agent):
	def __init__(self, app, image, rule):
		super(WolfAgent, self).__init__(image, rule)
		self._app = app
		
		wolfMean = int(world.WolfInitialEnergyEntryMean.get()) if world.WolfInitialEnergyEntryMean.get() <> '' else 5
		wolfVariance = int(world.WolfInitialEnergyEntryVariance.get()) if world.WolfInitialEnergyEntryVariance.get() <> '' else 0
		wolfNo = round(random_number_generator(wolfMean, wolfVariance))
		wolfNo = 0 if wolfNo < 0 else wolfNo
		
		self._energy = int(app._WolfInitialEnergyEntry.get()) if app._WolfInitialEnergyEntry.get() <> '' else 10
		
	@property
	def app(self):
		return self._app
		
	def move(self, x_pos, y_pos, neighbourHood, max_x, max_y, plane, movedMatrix):
		self._energy -= int(self.app._wolfMoveCostEntry.get()) if self.app._wolfMoveCostEntry.get() <> '' else 1
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
			self.rule.performMove(self.app, plane, x_pos, y_pos, x_pos - 1, y_pos)
			movedMatrix[x_pos - 1][y_pos] = 1
		if move == Rule.DOWN:
			self.rule.performMove(self.app, plane, x_pos, y_pos, x_pos + 1, y_pos)
			movedMatrix[x_pos + 1][y_pos] = 1
		if move == Rule.LEFT:
			self.rule.performMove(self.app, plane, x_pos, y_pos, x_pos, y_pos - 1)
			movedMatrix[x_pos][y_pos - 1] = 1
		if move == Rule.RIGHT:
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
		
		condition = int(app._birthdayWolfThresholdEntry.get()) if app._birthdayWolfThresholdEntry.get() <> '' else 20
		
		if (self.energy >= condition):
			move_tuple = reproduce_set[rand]
			self.addEnergy(-0.5 * condition)
			plane.widgets[move_tuple[0]][move_tuple[1]].agent = WolfAgent(self.app, self.image, self.rule)
			plane.widgets[move_tuple[0]][move_tuple[1]].image = self.rule.wolf
			plane.widgets[move_tuple[0]][move_tuple[1]].configure(image = self.rule.wolf)
			movedMatrix[move_tuple[0]][move_tuple[1]] = 1


class GrassAgent(Agent):
	def __init__(self, app, image, rule):
		super(GrassAgent, self).__init__(image, None)
		self._app = app
	
	@property
	def app(self):
		return self._app
	
	@property
	def energy(self):
		return int(self.app._grassEnergyEntry.get()) if self.app._grassEnergyEntry.get() <> '' else 1
		
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
	
	def getFreePlaces(self):
		places = []
		for i in range(0, self.rows):
			for j in range(0, self.columns):
				if self._widgets[i][j].image == self.empty:
					places.append((i, j))
		return places
		
	def randomPlacement(self, image, counter):
		empty = self.getFreePlaces()			
		while (counter > 0 and len(empty) > 0):
			randPlace = randint(0, len(empty) - 1)
			self._widgets[empty[randPlace][0]][empty[randPlace][1]].configure(image = image)
			self._widgets[empty[randPlace][0]][empty[randPlace][1]].image = image
			if (image == world.rabbit):
				self._widgets[empty[randPlace][0]][empty[randPlace][1]].agent = RabbitAgent(world.app, image, RabbitRule())
			elif (image == world.grass):
				self._widgets[empty[randPlace][0]][empty[randPlace][1]].agent = GrassAgent(world.app, image, None)	
			elif (image == world.wolf):
				self._widgets[empty[randPlace][0]][empty[randPlace][1]].agent = WolfAgent(world.app, image, WolfRule())	
			empty.remove(empty[randPlace])
			counter -= 1
	
	def reset(self, empty):
		for i in range(0, self._rows):
			for j in range (0, self.columns):
				self._widgets[i][j].configure(image=empty)
				self._widgets[i][j].image = empty
				self._widgets[i][j].agent = None
	
if __name__ == "__main__":
	root = tk.Tk()
	app = App(root)
	root.mainloop()