"""This module generates a rabbit-wolf-grass simulation
with a simple GUI."""

import Tkinter as tk
import world as w
import PIL
import time
import matplotlib
from random import randint
from os import getcwd
from configparser import ConfigParser
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from rule import RabbitRule, WolfRule
from agent import WolfAgent, RabbitAgent, GrassAgent
from utils import random_number_generator
from PIL import ImageTk, Image

def stop_simulation(run_button, stop_button, pause_button, resume_button, init_button):
    """Stops the currently running simulation."""
    run_button['state'] = 'disabled'
    stop_button['state'] = 'disabled'
    pause_button['state'] = 'disabled'
    resume_button['state'] = 'disabled'
    init_button['state'] = 'active'
    w.simulation_stop = True
    w.simulation_resume = False
    w.simulation_pause = False
    
def pause_simulation(pause_button, resume_button):
    pause_button['state'] = 'disabled'
    resume_button['state'] = 'active'
    w.simulation_pause = True
    w.simulation_resume = False

def resume_simulation(pause_button, resume_button, button_start, button_end, button_init, table,
                      rabbit_plot, rabbit_canvas, grass_plot, grass_canvas, wolf_plot, wolf_canvas, app):
    pause_button['state'] = 'active'
    resume_button['state'] = 'disabled'
    w.simulation_pause = False
    w.simulation_resume = True
    app.run(button_start, button_end, pause_button, button_init, table,
            rabbit_plot, rabbit_canvas, grass_plot, grass_canvas, wolf_plot, wolf_canvas)


class App(object):
    def __init__(self, master):
        self._master = master
        w.app = self
        config = ConfigParser()
        config_path = getcwd() + '/config/config.ini'
        config.read(config_path)

        self.prepare_images(config)

        master.title("Multiagent systems - rabbitsWolfsGrass")
        master.minsize(width=800, height=800)

        frame = tk.Frame(master)

        table = SimpleTable(master, w.empty, 10, 10)

        self.setup(frame, master, table)

    def prepare_images(self, config):
        """Prepares images for agents that are used in the simulation."""
        w.distribution = config.get('SIMULATION', 'DISTRIBUTION')
        rabbit_path = getcwd() + config.get('RABBIT', 'RELATIVE_PATH')
        wolf_path = getcwd() + config.get('WOLF', 'RELATIVE_PATH')
        grass_path = getcwd() + config.get('GRASS', 'RELATIVE_PATH')
        wolf_in_grass_path = getcwd() + config.get('WOLF_IN_GRASS', 'RELATIVE_PATH')
        empty_path = getcwd() + config.get('EMPTY', 'RELATIVE_PATH')

        rabbit = Image.open(rabbit_path)
        grass = Image.open(grass_path)
        wolf = Image.open(wolf_path)
        wolf_in_grass = Image.open(wolf_in_grass_path)
        empty = Image.open(empty_path)

        rabbit = rabbit.resize((40, 40), PIL.Image.ANTIALIAS)
        rabbit = ImageTk.PhotoImage(rabbit)
        w.rabbit = rabbit

        grass = grass.resize((40, 40), PIL.Image.ANTIALIAS)
        grass = ImageTk.PhotoImage(grass)
        w.grass = grass

        wolf = wolf.resize((40, 40), PIL.Image.ANTIALIAS)
        wolf = ImageTk.PhotoImage(wolf)
        w.wolf = wolf

        wolf_in_grass = wolf_in_grass.resize((40, 40), PIL.Image.ANTIALIAS)
        wolf_in_grass = ImageTk.PhotoImage(wolf_in_grass)
        w.wolf_in_grass = wolf_in_grass

        empty = empty.resize((40, 40), PIL.Image.ANTIALIAS)
        empty = ImageTk.PhotoImage(empty)
        w.empty = empty

    def put_entry_option(self, master, left_side, text):
        box = tk.Frame(master, bd=1, relief='sunken')
        box.pack(in_=left_side, fill='x')

        mean = tk.StringVar()
        mean.set("Mean:")

        variance = tk.StringVar()
        variance.set("Variance:")

        init_text = tk.StringVar()
        init_text.set(text)
        init_label=tk.Label(master, textvariable=init_text, height=2)
        init_label.grid(row=2, sticky='w')
        init_label.pack(in_=box, side="left")

        mean_label=tk.Label(master, textvariable=mean, height=2)
        mean_label.grid(row=2, sticky='w')
        mean_label.pack(in_=box, side="left", padx=10)

        mean_entry=tk.Entry(master,textvariable=tk.StringVar(None),width=10)
        mean_entry.grid(row=2, sticky='w')
        mean_entry.pack(in_=box, side="left")

        variance_label=tk.Label(master, textvariable=variance, height=2)
        variance_label.grid(row=2, sticky='w')
        variance_label.pack(in_=box, side="left", padx=10)

        variance_entry = tk.Entry(master,textvariable=tk.StringVar(None),width=10)
        variance_entry.grid(row=2, sticky='w')
        variance_entry.pack(in_=box, side="left")

        return mean_entry, variance_entry

    def setup(self, frame, master, table):
        frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        left_side = tk.Frame(master)
        left_side = tk.Frame(master)
        left_side.pack(in_=frame, side=tk.LEFT, fill=tk.BOTH, expand=True)

        center = tk.Frame(master)
        center.pack(in_=frame, side=tk.LEFT, fill=tk.BOTH, expand=True)

        right = tk.Frame(master)
        right.pack(in_=frame, side=tk.RIGHT, fill=tk.BOTH)

        button_init = tk.Button(master, height=4, width=20, text="Initialize",
                                command=lambda: self.initialize(button_start, table))
        button_init.pack(in_=right, fill='x', padx=100, pady=10)

        button_start = tk.Button(master, height=4, width=20, state='disabled',
                                 text="Run simulation",
                                 command=lambda: self.run(button_start, button_end, button_pause, button_init, table,
                                                          rabbit_plot, rabbit_canvas, grass_plot,
                                                          grass_canvas, wolf_plot, wolf_canvas))
        button_start.pack(in_=right, fill='x', padx=100, pady=10)

        button_end = tk.Button(master, height=4, width=20, text="Stop simulation",
                               command=lambda: stop_simulation(button_start, button_end, button_pause, button_resume, button_init),
                               state='disabled')
        button_end.pack(in_=right, fill='x', padx=100, pady=10)

        button_pause = tk.Button(master, height=4, width=20, text="Pause simulation",
                                 command=lambda: pause_simulation(button_pause, button_resume),
                                 state='disabled')
        button_pause.pack(in_=right, fill='x', padx=100, pady=10)

        button_resume = tk.Button(master, height=4, width=20, text="Resume simulation",
                                  command=lambda: resume_simulation(button_pause, button_resume, button_start, button_end, button_init, table,
                                                          rabbit_plot, rabbit_canvas, grass_plot,
                                                          grass_canvas, wolf_plot, wolf_canvas, self),
                                  state='disabled')
        button_resume.pack(in_=right, fill='x', padx=100, pady=10)

        w.rabbitInitEntryMean, w.rabbitInitEntryVariance = self.put_entry_option(master, left_side, "Enter initial number of rabbits")
        w.wolfInitEntryMean, w.wolfInitEntryVariance = self.put_entry_option(master, left_side, "Enter initial number of wolfs")
        w.grassInitEntryMean, w.grassInitEntryVariance = self.put_entry_option(master, left_side, "Enter grass growing rate per step")
        w.birthdayRabbitThresholdEntryMean, w.birthdayRabbitThresholdEntryVariance = self.put_entry_option(master, left_side, "Enter the rabbit birthday energy threshold")
        w.rabbitMoveCostEntryMean, w.rabbitMoveCostEntryVariance = self.put_entry_option(master, left_side, "Enter rabbit energy cost for movement")
        w.RabbitInitialEnergyEntryMean, w.RabbitInitialEnergyEntryVariance = self.put_entry_option(master, left_side, "Enter the rabbit initial energy")
        w.grassEnergyEntryMean, w.grassEnergyEntryVariance = self.put_entry_option(master, left_side, "Enter grass energy boost")
        w.WolfInitialEnergyEntryMean, w.WolfInitialEnergyEntryVariance = self.put_entry_option(master, left_side, "Enter initial wolf energy")
        w.birthdayWolfThresholdEntryMean, w.birthdayWolfThresholdEntryVariance = self.put_entry_option(master, left_side, "Enter the wolf birthday energy threshold")
        w.wolfMoveCostEntryMean, w.wolfMoveCostEntryVariance = self.put_entry_option(master, left_side, "Enter wolf energy cost for movement")

        up_left_forth_2 = tk.Frame(master, bd=1, relief='sunken')
        up_left_forth_2.pack(in_=left_side, fill='x')

        stepsText = tk.StringVar()
        stepsText.set("Enter number of steps")
        stepsLabel=tk.Label(master, textvariable=stepsText, height=2)
        stepsLabel.pack(in_=up_left_forth_2, side="left")

        stepsEntry=tk.Entry(master,textvariable=tk.StringVar(None),width=10)
        stepsEntry.pack(in_=up_left_forth_2, side="left")

        self._stepsEntry = stepsEntry
        w.stepsEntry = stepsEntry

        table.pack(side="top", fill="x")
        table2 = SimpleTable(master, w.empty, 10, 10)

        table.destroy()
        table2.pack(in_=center)
        table = table2

        bottom = tk.Frame(master)
        bottom.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        rabbit_figure = Figure(figsize=(5, 5), dpi=100)
        rabbit_plot = rabbit_figure.add_subplot(111)
        rabbit_plot.set_title("Number of rabbits per iteration step")
        rabbit_plot.set_xlabel('Step no')
        rabbit_plot.set_ylabel('Number of rabbits')
        rabbit_plot.set_xlim([0, 100])
        rabbit_plot.set_ylim([0, len(table.widgets[0]) * len(table.widgets)])

        rabbit_canvas = FigureCanvasTkAgg(rabbit_figure, master)
        rabbit_canvas.show()
        rabbit_canvas.get_tk_widget().pack(in_=bottom, side=tk.LEFT, expand=True)

        grass_figure = Figure(figsize=(5, 5), dpi=100)
        grass_plot = grass_figure.add_subplot(111)
        grass_plot.set_title("Amount of grass per iteration step")
        grass_plot.set_xlabel('Step no')
        grass_plot.set_ylabel('Amount of grass')
        grass_plot.set_xlim([0, 100])
        grass_plot.set_ylim([0, len(table.widgets[0]) * len(table.widgets)])

        grass_canvas = FigureCanvasTkAgg(grass_figure, master)
        grass_canvas.show()
        grass_canvas.get_tk_widget().pack(in_=bottom, side=tk.LEFT, expand=True)

        wolf_figure = Figure(figsize=(5, 5), dpi=100)
        wolf_plot = wolf_figure.add_subplot(111)
        wolf_plot.set_title("Number of wolfs per iteration step")
        wolf_plot.set_xlabel('Step no')
        wolf_plot.set_ylabel('Number of wolfs')
        wolf_plot.set_xlim([0, 100])
        wolf_plot.set_ylim([0, len(table.widgets[0]) * len(table.widgets)])

        wolf_canvas = FigureCanvasTkAgg(wolf_figure, master)
        wolf_canvas.show()
        wolf_canvas.get_tk_widget().pack(in_=bottom, side=tk.LEFT, expand=True)

    def initialize(self, run_button, table):
        run_button['state'] = 'active'
        table.reset(w.empty)

        if w.rabbitInitEntryMean.get() <> '':
            rabbit_mean = int(w.rabbitInitEntryMean.get())
        else:
            rabbit_mean = 5

        if w.rabbitInitEntryVariance.get() <> '':
            rabbit_variance = int(w.rabbitInitEntryVariance.get())
        else:
            rabbit_variance = 0

        rabbit_no = round(random_number_generator(rabbit_mean, rabbit_variance))
        rabbit_no = 0 if rabbit_no < 0 else rabbit_no

        if w.wolfInitEntryMean.get() <> '':
            wolf_mean = int(w.wolfInitEntryMean.get())
        else:
            wolf_mean = 5

        if w.wolfInitEntryVariance.get() <> '':
            wolf_variance = int(w.wolfInitEntryVariance.get())
        else:
            wolf_variance = 0

        wolf_no = round(random_number_generator(wolf_mean, wolf_variance))
        wolf_no = 0 if wolf_no < 0 else wolf_no

        if w.grassInitEntryMean.get() <> '':
            grass_mean = int(w.grassInitEntryMean.get())
        else:
            grass_mean = 5

        if w.grassInitEntryVariance.get() <> '':
            grass_variance = int(w.grassInitEntryVariance.get())
        else:
            grass_variance = 0

        grass_no = round(random_number_generator(grass_mean, grass_variance))
        grass_no = 0 if grass_no < 0 else grass_no

        table.randomPlacement(w.rabbit, rabbit_no)
        table.randomPlacement(w.wolf, wolf_no)
        table.randomPlacement(w.grass, grass_no)

    @property
    def master(self):
        return self._master

    def run(self, run_button, stop_button, pause_button, init_button, table, rabbit_plot, rabbit_canvas, grass_plot,
            grass_canvas, wolf_plot, wolf_canvas):
        """Runs a given simulation."""
        run_button['state'] = 'disabled'
        init_button['state'] = 'disabled'
        stop_button['state'] = 'active'
        pause_button['state'] = 'active'
        step_no = [0]
        rabbit_no = [self.countAgents(table, w.rabbit)]
        grass_no = [self.countAgents(table, w.grass, w.wolf_in_grass)]
        wolf_no = [self.countAgents(table, w.wolf, w.wolf_in_grass)]

        if w.simulation_resume == True:
            step_no = w.step_no
            rabbit_no = w.rabbit_no
            grass_no = w.grass_no
            wolf_no = w.wolf_no
            start = w.simulation_step
        else:
            start = 0
            step_no = [start]
            rabbit_no = [self.countAgents(table, w.rabbit)]
            grass_no = [self.countAgents(table, w.grass, w.wolf_in_grass)]
            wolf_no = [self.countAgents(table, w.wolf, w.wolf_in_grass)]
        
        for k in range(start, int(w.stepsEntry.get()) if w.stepsEntry.get() <> '' else 200):
            if w.simulation_pause == True:
                w.simulation_pause = False
                w.step_no = step_no
                w.rabbit_no = rabbit_no
                w.grass_no = grass_no
                w.wolf_no = wolf_no
                w.simulation_step = k
                return
            if w.simulation_stop == True:
                w.simulation_stop = False
                return
            movedMatrix = [[0 for m in range(0, len(table.widgets[n]))]
                           for n in range(0, len(table.widgets))]
            for i in range(0, len(table.widgets)):
                for j in range(0, len(table.widgets[i])):
                    if hasattr(table.widgets[i][j], 'image'):
                        neighbours = [None] * 4
                        if not i == 0:
                            neighbours[w.UP] = table.widgets[i-1][j].image
                        if not i == len(table.widgets) - 1:
                            neighbours[w.DOWN] = table.widgets[i+1][j].image
                        if not j == 0:
                            neighbours[w.LEFT] = table.widgets[i][j-1].image
                        if not j == len(table.widgets[i]) - 1:
                            neighbours[w.RIGHT] = table.widgets[i][j+1].image
                        if (table.widgets[i][j].image == w.rabbit or
                            table.widgets[i][j].image == w.wolf or
                            table.widgets[i][j].image == w.wolf_in_grass):
                            if movedMatrix[i][j] == 0:
                                table.widgets[i][j].agent.move(i, j, neighbours,
                                                               len(table.widgets) - 1,
                                                               len(table.widgets[i]) - 1,
                                                               table, movedMatrix)

            step_no.append(k + 1)
            rabbit_no.append(self.countAgents(table, w.rabbit))
            grass_no.append(self.countAgents(table, w.grass, w.wolf_in_grass))
            wolf_no.append(self.countAgents(table, w.wolf, w.wolf_in_grass))

            rabbit_plot.clear()
            grass_plot.clear()
            wolf_plot.clear()
            rabbit_plot.plot(step_no, rabbit_no)
            rabbit_plot.set_title("Number of rabbits per iteration step")
            rabbit_plot.set_xlabel('Step no')
            rabbit_plot.set_ylabel('Number of rabbits')
            grass_plot.plot(step_no, grass_no)
            grass_plot.set_title("Amount of grass per iteration step")
            grass_plot.set_xlabel('Step no')
            grass_plot.set_ylabel('Amount of grass')
            wolf_plot.plot(step_no, wolf_no)
            wolf_plot.set_title("Number of wolfs per iteration step")
            wolf_plot.set_xlabel('Step no')
            wolf_plot.set_ylabel('Number of wolfs')
            if k <= 100:
                rabbit_plot.set_xlim([0, 100])
                grass_plot.set_xlim([0, 100])
                wolf_plot.set_xlim([0, 100])
            else:
                rabbit_plot.set_xlim([k - 100, k])
                grass_plot.set_xlim([k - 100, k])
                wolf_plot.set_xlim([k - 100, k])
            rabbit_plot.set_ylim([0, len(table.widgets[i]) * len(table.widgets)])
            grass_plot.set_ylim([0, len(table.widgets[i]) * len(table.widgets)])
            wolf_plot.set_ylim([0, len(table.widgets[i]) * len(table.widgets)])
            rabbit_canvas.draw()
            grass_canvas.draw()
            wolf_canvas.draw()
            time.sleep(w.sleep_time)

            if w.grassInitEntryMean.get() <> '':
                grass_mean = int(w.grassInitEntryMean.get())
            else:
                grass_mean = 5

            if w.grassInitEntryVariance.get() <> '':
                grass_variance = int(w.grassInitEntryVariance.get())
            else:
                grass_variance = 0

            grass_add_no = round(random_number_generator(grass_mean, grass_variance))
            grass_add_no = 0 if grass_add_no < 0 else grass_add_no

            table.randomPlacement(w.grass, grass_add_no)
            self.master.update()

    def countAgents(self, t, *args):
        """Count the number of given agent type, that are currently in the simulation."""
        counter = 0
        for i in range(0, len(t.widgets)):
            for j in range(0, len(t.widgets[i])):
                if hasattr(t.widgets[i][j], 'image'):
                    for count, thing in enumerate(args):
                        if t.widgets[i][j].image == thing:
                            counter += 1
                            break
        return counter


class SimpleTable(tk.Frame):
    def __init__(self, parent, empty, rows=10, columns=10):
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
                label.configure(image=self.empty)
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
        """Creates 'counter' number of agents for a given 'image'"""
        empty = self.getFreePlaces()
        while counter > 0 and len(empty) > 0:
            randPlace = randint(0, len(empty) - 1)
            x_coord = empty[randPlace][0]
            y_coord = empty[randPlace][1]
            self._widgets[x_coord][y_coord].configure(image=image)
            self._widgets[x_coord][y_coord].image = image
            if image == w.rabbit:
                self._widgets[x_coord][y_coord].agent = RabbitAgent(w.app, image, RabbitRule())
            elif image == w.grass:
                self._widgets[x_coord][y_coord].agent = GrassAgent(w.app, image, None)
            elif image == w.wolf:
                self._widgets[x_coord][y_coord].agent = WolfAgent(w.app, image, WolfRule())
            empty.remove(empty[randPlace])
            counter -= 1

    def reset(self, empty):
        for i in range(0, self._rows):
            for j in range(0, self.columns):
                self._widgets[i][j].configure(image=empty)
                self._widgets[i][j].image = empty
                self._widgets[i][j].agent = None

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()