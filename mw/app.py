"""This module generates a rabbit-wolf-grass simulation
with a simple GUI."""

import Tkinter as tk
import time
from random import randint
from os import getcwd
from configparser import ConfigParser
from PIL import ImageTk, Image
import world as w
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from rule import RabbitRule, WolfRule
from agent import WolfAgent, RabbitAgent, GrassAgent
from utils import random_number_generator
matplotlib.use('TkAgg')

def stop_simulation(run_button, stop_button, pause_button, resume_button, init_button):
    """Stops the currently running simulation."""
    run_button['state'] = 'disabled'
    stop_button['state'] = 'disabled'
    pause_button['state'] = 'disabled'
    resume_button['state'] = 'disabled'
    init_button['state'] = 'active'
    w.SIMULATION_STOP = True
    w.SIMULATION_RESUME = False
    w.SIMULATION_PAUSE = False

def pause_simulation(pause_button, resume_button):
    """Pauses the currently running simulation."""
    pause_button['state'] = 'disabled'
    resume_button['state'] = 'active'
    w.SIMULATION_PAUSE = True
    w.SIMULATION_RESUME = False

def resume_simulation(pause_button, resume_button, table, app):
    """Resumes the currently running simulation."""
    pause_button['state'] = 'active'
    resume_button['state'] = 'disabled'
    w.SIMULATION_PAUSE = False
    w.SIMULATION_RESUME = True
    app.run(table)


class App(object):
    """Application that runs wolf-rabbit-grass simulation with GUI."""
    def __init__(self, master):
        self._master = master
        w.app = self
        config = ConfigParser()
        config_path = getcwd() + '/config/config.ini'
        config.read(config_path)

        w.CONFIG = config
        self.prepare_images()

        master.title("Multiagent systems - rabbitsWolfsGrass")
        master.minsize(width=800, height=800)

        frame = tk.Frame(master)

        table = SimpleTable(master, 10, 10)

        self.setup(frame, master, table)

    @staticmethod
    def prepare_images():
        """Prepares images for agents that are used in the simulation."""
        w.DISTRIBUTION = w.CONFIG.get('SIMULATION', 'DISTRIBUTION')
        rabbit_path = getcwd() + w.CONFIG.get('RABBIT', 'RELATIVE_PATH')
        wolf_path = getcwd() + w.CONFIG.get('WOLF', 'RELATIVE_PATH')
        grass_path = getcwd() + w.CONFIG.get('GRASS', 'RELATIVE_PATH')
        wolf_in_grass_path = getcwd() + w.CONFIG.get('WOLF_IN_GRASS', 'RELATIVE_PATH')
        empty_path = getcwd() + w.CONFIG.get('EMPTY', 'RELATIVE_PATH')

        rabbit = Image.open(rabbit_path)
        grass = Image.open(grass_path)
        wolf = Image.open(wolf_path)
        wolf_in_grass = Image.open(wolf_in_grass_path)
        empty = Image.open(empty_path)

        rabbit = rabbit.resize((40, 40), Image.ANTIALIAS)
        rabbit = ImageTk.PhotoImage(rabbit)
        w.RABBIT = rabbit

        grass = grass.resize((40, 40), Image.ANTIALIAS)
        grass = ImageTk.PhotoImage(grass)
        w.GRASS = grass

        wolf = wolf.resize((40, 40), Image.ANTIALIAS)
        wolf = ImageTk.PhotoImage(wolf)
        w.WOLF = wolf

        wolf_in_grass = wolf_in_grass.resize((40, 40), Image.ANTIALIAS)
        wolf_in_grass = ImageTk.PhotoImage(wolf_in_grass)
        w.WOLF_IN_GRASS = wolf_in_grass

        empty = empty.resize((40, 40), Image.ANTIALIAS)
        empty = ImageTk.PhotoImage(empty)
        w.EMPTY = empty

    @staticmethod
    def put_entry(master, left_side, text):
        """Adds a new entry box in a frame"""
        box = tk.Frame(master, bd=1, relief='sunken')
        box.pack(in_=left_side, fill='x')

        mean = tk.StringVar()
        mean.set("Mean:")

        variance = tk.StringVar()
        variance.set("Variance:")

        init_text = tk.StringVar()
        init_text.set(text)
        init_label = tk.Label(master, textvariable=init_text, height=2)
        init_label.grid(row=2, sticky='w')
        init_label.pack(in_=box, side="left")

        mean_label = tk.Label(master, textvariable=mean, height=2)
        mean_label.grid(row=2, sticky='w')
        mean_label.pack(in_=box, side="left", padx=10)

        mean_entry = tk.Entry(master, textvariable=tk.StringVar(None), width=10)
        mean_entry.grid(row=2, sticky='w')
        mean_entry.pack(in_=box, side="left")

        variance_label = tk.Label(master, textvariable=variance, height=2)
        variance_label.grid(row=2, sticky='w')
        variance_label.pack(in_=box, side="left", padx=10)

        variance_entry = tk.Entry(master, textvariable=tk.StringVar(None), width=10)
        variance_entry.grid(row=2, sticky='w')
        variance_entry.pack(in_=box, side="left")

        return mean_entry, variance_entry

    def setup(self, frame, master, table):
        """Sets up the application frame and environment."""
        frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        left_side = tk.Frame(master)
        left_side = tk.Frame(master)
        left_side.pack(in_=frame, side=tk.LEFT, fill=tk.BOTH, expand=True)

        center = tk.Frame(master)
        center.pack(in_=frame, side=tk.LEFT, fill=tk.BOTH, expand=True)

        right = tk.Frame(master)
        right.pack(in_=frame, side=tk.RIGHT, fill=tk.BOTH)

        button_init = tk.Button(master, height=4, width=20, text="Initialize",
                                command=lambda: self.initialize(table))
        button_init.pack(in_=right, fill='x', padx=100, pady=10)
        self.button_init = button_init

        button_start = tk.Button(master, height=4, width=20, state='disabled',
                                 text="Run simulation", command=lambda: self.run(table))
        button_start.pack(in_=right, fill='x', padx=100, pady=10)
        self.button_start = button_start

        button_end = tk.Button(master, height=4, width=20, text="Stop simulation",
                               command=lambda: stop_simulation(button_start, button_end,
                                                               button_pause, button_resume,
                                                               button_init), state='disabled')
        button_end.pack(in_=right, fill='x', padx=100, pady=10)
        self.button_end = button_end

        button_pause = tk.Button(master, height=4, width=20, text="Pause simulation",
                                 command=lambda: pause_simulation(button_pause, button_resume),
                                 state='disabled')
        button_pause.pack(in_=right, fill='x', padx=100, pady=10)
        self.button_pause = button_pause

        button_resume = tk.Button(master, height=4, width=20, text="Resume simulation",
                                  command=lambda: resume_simulation(button_pause, button_resume,
                                                                    table, self),
                                  state='disabled')
        button_resume.pack(in_=right, fill='x', padx=100, pady=10)
        self.button_resume = button_resume

        txt_label = "Enter initial number of rabbits"
        w.RABBIT_INIT_ENTRY_MEAN, w.RABBIT_INIT_ENTRY_VARIANCE = self.put_entry(master,
                                                                                left_side,
                                                                                txt_label)
        txt_label = "Enter initial number of wolfs"
        w.WOLF_INIT_ENTRY_MEAN, w.WOLF_INIT_ENTRY_VARIANCE = self.put_entry(master,
                                                                            left_side,
                                                                            txt_label)
        txt_label = "Enter grass growing rate per step"
        w.GRASS_INIT_ENTRY_MEAN, w.GRASS_INIT_ENTRY_VARIANCE = self.put_entry(master,
                                                                              left_side,
                                                                              txt_label)
        txt_label = "Enter the rabbit birthday energy threshold"
        w.BIRTHDAY_RABBIT_ENTRY_MEAN, w.BIRTHDAY_RABBIT_ENTRY_VARIANCE = self.put_entry(master,
                                                                                        left_side,
                                                                                        txt_label)
        txt_label = "Enter rabbit energy cost for movement"
        w.RABBIT_MOVE_COST_ENTRY_MEAN, w.RABBIT_MOVE_COST_ENTRY_VARIANCE = self.put_entry(master,
                                                                                          left_side,
                                                                                          txt_label)
        txt_label = "Enter the rabbit initial energy"
        w.RABBIT_ENERGY_ENTRY_MEAN, w.RABBIT_ENERGY_ENTRY_VARIANCE = self.put_entry(master,
                                                                                    left_side,
                                                                                    txt_label)
        txt_label = "Enter grass energy boost"
        w.GRASS_ENERGY_ENTRY_MEAN, w.GRASS_ENERGY_ENTRY_VARIANCE = self.put_entry(master,
                                                                                  left_side,
                                                                                  txt_label)
        txt_label = "Enter initial wolf energy"
        w.WOLF_ENERGY_ENTRY_MEAN, w.WOLF_ENERGY_ENTRY_VARIANCE = self.put_entry(master,
                                                                                left_side,
                                                                                txt_label)
        txt_label = "Enter the wolf birthday energy threshold"
        w.BIRTHDAY_WOLF_ENTRY_MEAN, w.BIRTHDAY_WOLF_ENTRY_VARIANCE = self.put_entry(master,
                                                                                    left_side,
                                                                                    txt_label)
        txt_label = "Enter wolf energy cost for movement"
        w.WOLF_MOVE_COST_ENTRY_MEAN, w.WOLF_MOVE_COST_ENTRY_VARIANCE = self.put_entry(master,
                                                                                      left_side,
                                                                                      txt_label)

        up_left_step_space = tk.Frame(master, bd=1, relief='sunken')
        up_left_step_space.pack(in_=left_side, fill='x')

        steps_text = tk.StringVar()
        steps_text.set("Enter number of steps")
        steps_label = tk.Label(master, textvariable=steps_text, height=2)
        steps_label.pack(in_=up_left_step_space, side="left")

        steps_entry = tk.Entry(master, textvariable=tk.StringVar(None), width=10)
        steps_entry.pack(in_=up_left_step_space, side="left")

        self._steps_entry = steps_entry
        w.STEPS_ENTRY = steps_entry

        table.pack(side="top", fill="x")
        table2 = SimpleTable(master, 10, 10)

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
        self.rabbit_plot = rabbit_plot

        rabbit_canvas = FigureCanvasTkAgg(rabbit_figure, master)
        rabbit_canvas.show()
        rabbit_canvas.get_tk_widget().pack(in_=bottom, side=tk.LEFT, expand=True)
        self.rabbit_canvas = rabbit_canvas

        grass_figure = Figure(figsize=(5, 5), dpi=100)
        grass_plot = grass_figure.add_subplot(111)
        grass_plot.set_title("Amount of grass per iteration step")
        grass_plot.set_xlabel('Step no')
        grass_plot.set_ylabel('Amount of grass')
        grass_plot.set_xlim([0, 100])
        grass_plot.set_ylim([0, len(table.widgets[0]) * len(table.widgets)])
        self.grass_plot = grass_plot

        grass_canvas = FigureCanvasTkAgg(grass_figure, master)
        grass_canvas.show()
        grass_canvas.get_tk_widget().pack(in_=bottom, side=tk.LEFT, expand=True)
        self.grass_canvas = grass_canvas

        wolf_figure = Figure(figsize=(5, 5), dpi=100)
        wolf_plot = wolf_figure.add_subplot(111)
        wolf_plot.set_title("Number of wolfs per iteration step")
        wolf_plot.set_xlabel('Step no')
        wolf_plot.set_ylabel('Number of wolfs')
        wolf_plot.set_xlim([0, 100])
        wolf_plot.set_ylim([0, len(table.widgets[0]) * len(table.widgets)])
        self.wolf_plot = wolf_plot

        wolf_canvas = FigureCanvasTkAgg(wolf_figure, master)
        wolf_canvas.show()
        wolf_canvas.get_tk_widget().pack(in_=bottom, side=tk.LEFT, expand=True)
        self.wolf_canvas = wolf_canvas

    def initialize(self, table):
        """Initializes the table with agents."""
        self.button_start['state'] = 'active'
        table.reset(w.EMPTY)
        w.SIMULATION_PAUSE = False
        w.SIMULATION_STOP = False
        w.SIMULATION_RESUME = False

        if w.RABBIT_INIT_ENTRY_MEAN.get() <> '':
            rabbit_mean = float(w.RABBIT_INIT_ENTRY_MEAN.get())
        else:
            rabbit_mean = float(w.CONFIG.get("RABBIT", "DEFAULT_INIT_MEAN"))

        if w.RABBIT_INIT_ENTRY_VARIANCE.get() <> '':
            rabbit_variance = float(w.RABBIT_INIT_ENTRY_VARIANCE.get())
        else:
            rabbit_variance = float(w.CONFIG.get("RABBIT", "DEFAULT_INIT_VARIANCE"))

        rabbit_no = round(random_number_generator(rabbit_mean, rabbit_variance))
        rabbit_no = 0.0 if rabbit_no < 0 else rabbit_no

        if w.WOLF_INIT_ENTRY_MEAN.get() <> '':
            wolf_mean = float(w.WOLF_INIT_ENTRY_MEAN.get())
        else:
            wolf_mean = float(w.CONFIG.get("WOLF", "DEFAULT_INIT_MEAN"))

        if w.WOLF_INIT_ENTRY_VARIANCE.get() <> '':
            wolf_variance = float(w.WOLF_INIT_ENTRY_VARIANCE.get())
        else:
            wolf_variance = float(w.CONFIG.get("WOLF", "DEFAULT_INIT_VARIANCE"))

        wolf_no = round(random_number_generator(wolf_mean, wolf_variance))
        wolf_no = 0.0 if wolf_no < 0 else wolf_no

        if w.GRASS_INIT_ENTRY_MEAN.get() <> '':
            grass_mean = float(w.GRASS_INIT_ENTRY_MEAN.get())
        else:
            grass_mean = float(w.CONFIG.get("GRASS", "DEFAULT_INIT_MEAN"))

        if w.GRASS_INIT_ENTRY_VARIANCE.get() <> '':
            grass_variance = float(w.GRASS_INIT_ENTRY_VARIANCE.get())
        else:
            grass_variance = float(w.CONFIG.get("GRASS", "DEFAULT_INIT_VARIANCE"))

        grass_no = round(random_number_generator(grass_mean, grass_variance))
        grass_no = 0.0 if grass_no < 0 else grass_no

        table.randomPlacement(w.RABBIT, rabbit_no)
        table.randomPlacement(w.WOLF, wolf_no)
        table.randomPlacement(w.GRASS, grass_no)

    @property
    def master(self):
        """Returns tkinter root"""
        return self._master

    def run(self, table):
        """Runs a given simulation."""
        self.button_start['state'] = 'disabled'
        self.button_init['state'] = 'disabled'
        self.button_end['state'] = 'active'
        self.button_pause['state'] = 'active'
        step_no = [0]
        rabbit_no = [self.count_agents(table, w.RABBIT)]
        grass_no = [self.count_agents(table, w.GRASS, w.WOLF_IN_GRASS)]
        wolf_no = [self.count_agents(table, w.WOLF, w.WOLF_IN_GRASS)]

        if w.SIMULATION_RESUME:
            step_no = w.STEP_NO
            rabbit_no = w.RABBIT_NO
            grass_no = w.GRASS_NO
            wolf_no = w.WOLF_NO
            start = w.SIMULATION_STEP
        else:
            start = 0
            step_no = [start]
            rabbit_no = [self.count_agents(table, w.RABBIT)]
            grass_no = [self.count_agents(table, w.GRASS, w.WOLF_IN_GRASS)]
            wolf_no = [self.count_agents(table, w.WOLF, w.WOLF_IN_GRASS)]
        if w.STEPS_ENTRY.get() <> '':
            iteration_limit = int(w.STEPS_ENTRY.get())
        else:
            iteration_limit = int(w.CONFIG.get("SIMULATION", "DEFAULT_STEPS"))
        for k in range(start,  iteration_limit):
            if w.SIMULATION_PAUSE:
                w.SIMULATION_PAUSE = False
                w.STEP_NO = step_no
                w.RABBIT_NO = rabbit_no
                w.GRASS_NO = grass_no
                w.WOLF_NO = wolf_no
                w.SIMULATION_STEP = k
                return
            if w.SIMULATION_STOP:
                w.SIMULATION_STOP = False
                return
            moved_matrix = [[0 for m in range(0, len(table.widgets[n]))]
                            for n in range(0, len(table.widgets))]
            for i in range(0, len(table.widgets)):
                for j in range(0, len(table.widgets[i])):
                    neighbours = [None] * 4
                    if not i == 0:
                        neighbours[w.UP] = table.widgets[i-1][j].image
                    if not i == len(table.widgets) - 1:
                        neighbours[w.DOWN] = table.widgets[i+1][j].image
                    if not j == 0:
                        neighbours[w.LEFT] = table.widgets[i][j-1].image
                    if not j == len(table.widgets[i]) - 1:
                        neighbours[w.RIGHT] = table.widgets[i][j+1].image
                    if (table.widgets[i][j].image == w.RABBIT or
                            table.widgets[i][j].image == w.WOLF or
                            table.widgets[i][j].image == w.WOLF_IN_GRASS):
                        if moved_matrix[i][j] == 0:
                            table.widgets[i][j].agent.move(i, j, neighbours,
                                                           len(table.widgets) - 1,
                                                           len(table.widgets[i]) - 1,
                                                           table, moved_matrix)

            step_no.append(k + 1)
            rabbit_no.append(self.count_agents(table, w.RABBIT))
            grass_no.append(self.count_agents(table, w.GRASS, w.WOLF_IN_GRASS))
            wolf_no.append(self.count_agents(table, w.WOLF, w.WOLF_IN_GRASS))

            self.redraw_plot(step_no, rabbit_no, self.rabbit_plot, self.rabbit_canvas, k,
                             "Number of rabbits per iteration step", table)
            self.redraw_plot(step_no, wolf_no, self.wolf_plot, self.wolf_canvas, k,
                             "Number of wolfs per iteration step", table)
            self.redraw_plot(step_no, grass_no, self.grass_plot, self.grass_canvas, k,
                             "Amount of grass per iteration step", table)

            time.sleep(w.SLEEP_TIME)

            if w.GRASS_INIT_ENTRY_MEAN.get() <> '':
                grass_mean = float(w.GRASS_INIT_ENTRY_MEAN.get())
            else:
                grass_mean = 5.0

            if w.GRASS_INIT_ENTRY_VARIANCE.get() <> '':
                grass_variance = float(w.GRASS_INIT_ENTRY_VARIANCE.get())
            else:
                grass_variance = 0.0

            grass_add_no = round(random_number_generator(grass_mean, grass_variance))
            grass_add_no = 0.0 if grass_add_no < 0 else grass_add_no

            table.randomPlacement(w.GRASS, grass_add_no)
            self.master.update()

        self.button_start['state'] = 'disabled'
        self.button_init['state'] = 'active'
        self.button_end['state'] = 'disabled'
        self.button_pause['state'] = 'disabled'

    @staticmethod
    def redraw_plot(x_line, y_line, plot, canvas, step_no, title, table):
        """Redraws given plot."""
        plot.clear()
        plot.plot(x_line, y_line)
        plot.set_title(title)
        plot.set_xlabel('Step no')
        plot.set_ylabel('Number of agents')
        if step_no <= 100:
            plot.set_xlim([0, 100])
        else:
            plot.set_xlim([step_no - 100, step_no])
        plot.set_ylim([0, len(table.widgets[1]) * len(table.widgets)])
        canvas.draw()

    @staticmethod
    def count_agents(table, *args):
        """Count the number of given agent type, that are currently in the simulation."""
        counter = 0
        for i in range(0, len(table.widgets)):
            for j in range(0, len(table.widgets[i])):
                for count, thing in enumerate(args):
                    if table.widgets[i][j].image == thing:
                        counter += 1
                        break
        return counter


class SimpleTable(tk.Frame):
    """Table that holds positions of agents in a given simulation."""
    def __init__(self, parent, rows=10, columns=10):
        tk.Frame.__init__(self, parent, background="black")
        self._widgets = []
        self._rows = rows
        self._columns = columns
        for row in range(rows):
            current_row = []
            for column in range(columns):
                label = tk.Label(self, width=40, height=40, relief="ridge")
                label.grid(row=row, column=column, sticky="wnes", padx=2, pady=2)
                label.configure(image=w.EMPTY)
                label.image = w.EMPTY
                label.agent = None
                current_row.append(label)
            self._widgets.append(current_row)

        for column in range(columns):
            self.grid_columnconfigure(column, weight=4)

    @property
    def columns(self):
        """Returns number of columns."""
        return self._columns

    @property
    def rows(self):
        """Returns number of rows."""
        return self._rows

    @property
    def widgets(self):
        """Returns table widgets."""
        return self._widgets

    def get_free_places(self):
        """Returns the number of squares, which are not occupied by any agent."""
        places = []
        for i in range(0, self.rows):
            for j in range(0, self.columns):
                if self._widgets[i][j].image == w.EMPTY:
                    places.append((i, j))
        return places

    def randomPlacement(self, image, counter):
        """Creates 'counter' number of agents for a given 'image'"""
        empty = self.get_free_places()
        while counter > 0 and len(empty) > 0:
            rand_place = randint(0, len(empty) - 1)
            x_coord = empty[rand_place][0]
            y_coord = empty[rand_place][1]
            self._widgets[x_coord][y_coord].configure(image=image)
            self._widgets[x_coord][y_coord].image = image
            if image == w.RABBIT:
                self._widgets[x_coord][y_coord].agent = RabbitAgent(w.app, image, RabbitRule())
            elif image == w.GRASS:
                self._widgets[x_coord][y_coord].agent = GrassAgent(w.app, image, None)
            elif image == w.WOLF:
                self._widgets[x_coord][y_coord].agent = WolfAgent(w.app, image, WolfRule())
            empty.remove(empty[rand_place])
            counter -= 1

    def reset(self, empty):
        """Fills the table with 'empty' images and resets agents."""
        for i in range(0, self._rows):
            for j in range(0, self.columns):
                self._widgets[i][j].configure(image=empty)
                self._widgets[i][j].image = empty
                self._widgets[i][j].agent = None

if __name__ == "__main__":
    ROOT = tk.Tk()
    APP = App(ROOT)
    ROOT.mainloop()
