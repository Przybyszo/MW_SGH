"""This module specifies agents, that are used in the simulation."""

import itertools
from random import randint
import world as w
from utils import random_number_generator

class Identificator(object):
    """Identificator class."""
    newid = itertools.count().next
    def __init__(self):
        self._id = Identificator.newid()

    @property
    def id(self):
        """Returns id"""
        return self._id


class Agent(object):
    """Agent class."""
    def __init__(self, image, rule):
        self._image = image
        self._move_rule = rule
        self._energy = 0
        self._id = Identificator().id

    @property
    def id(self):
        """Returns id"""
        return self._id

    @property
    def image(self):
        """Returns image"""
        return self._image

    @property
    def rule(self):
        """Returns rule"""
        return self._move_rule

    @property
    def energy(self):
        """Returns energy"""
        return self._energy

    def move(self, x_pos, y_pos, neighbourhood, max_x, max_y, plane, moved_matrix):
        """Performs a move of an agent."""
        pass

    def die(self):
        """Check if agent is supposed to die."""
        if self.energy < 0:
            return True
        return False


class RabbitAgent(Agent):
    """Rabbit agent class."""
    def __init__(self, app, image, rule):
        super(RabbitAgent, self).__init__(image, rule)

        if w.RABBIT_ENERGY_ENTRY_MEAN.get() <> '':
            rabbit_mean = float(w.RABBIT_ENERGY_ENTRY_MEAN.get())
        else:
            rabbit_mean = 5

        if w.RABBIT_ENERGY_ENTRY_VARIANCE.get() <> '':
            rabbit_variance = float(w.RABBIT_ENERGY_ENTRY_VARIANCE.get())
        else:
            rabbit_variance = 0

        rabbit_energy = random_number_generator(rabbit_mean, rabbit_variance)
        rabbit_energy = 0 if rabbit_energy < 0 else rabbit_energy

        self._energy = rabbit_energy
        self._app = app

        if w.BIRTHDAY_RABBIT_ENTRY_MEAN.get() <> '':
            rabbit_mean = float(w.BIRTHDAY_RABBIT_ENTRY_MEAN.get())
        else:
            rabbit_mean = 10

        if w.BIRTHDAY_RABBIT_ENTRY_VARIANCE.get() <> '':
            rabbit_variance = float(w.BIRTHDAY_RABBIT_ENTRY_VARIANCE.get())
        else:
            rabbit_variance = 0

        rabbit_threshold = random_number_generator(rabbit_mean, rabbit_variance)
        rabbit_threshold = 0 if rabbit_threshold < 0 else rabbit_threshold

        self._condition = rabbit_threshold

    @property
    def condition(self):
        """Returns birthday threshold"""
        return self._condition

    @property
    def app(self):
        """Returns application"""
        return self._app

    def add_energy(self, energy):
        """Adds energy to agent's energy."""
        self._energy += energy

    def reproduce(self, plane, row, column, max_row, max_column, moved_matrix):
        """Agent reproduces (if it is possible due to energy constraints)"""
        reproduce_set = []
        if row <> 0:
            if (not plane.widgets[row - 1][column].image == w.WOLF and
                    not plane.widgets[row - 1][column].image == w.RABBIT and
                    not plane.widgets[row - 1][column].image == w.WOLF_IN_GRASS):
                reproduce_set.append((row - 1, column))
        if row <> max_row:
            if (not plane.widgets[row + 1][column].image == w.WOLF and
                    not plane.widgets[row + 1][column].image == w.RABBIT and
                    not plane.widgets[row + 1][column].image == w.WOLF_IN_GRASS):
                reproduce_set.append((row + 1, column))
        if column <> 0:
            if (not plane.widgets[row][column - 1].image == w.WOLF and
                    not plane.widgets[row][column - 1].image == w.RABBIT and
                    not plane.widgets[row][column - 1].image == w.WOLF_IN_GRASS):
                reproduce_set.append((row, column - 1))
        if column <> max_column:
            if (not plane.widgets[row][column + 1].image == w.WOLF and
                    not plane.widgets[row][column + 1].image == w.RABBIT and
                    not plane.widgets[row][column + 1].image == w.WOLF_IN_GRASS):
                reproduce_set.append((row, column + 1))

        if len(reproduce_set) == 0:
            return

        rand = randint(0, len(reproduce_set) - 1)

        if self.energy >= self.condition:
            move_tuple = reproduce_set[rand]
            self.add_energy(-0.5 * self.condition)
            plane.widgets[move_tuple[0]][move_tuple[1]].agent = RabbitAgent(self.app, self.image,
                                                                            self.rule)
            plane.widgets[move_tuple[0]][move_tuple[1]].image = w.RABBIT
            plane.widgets[move_tuple[0]][move_tuple[1]].configure(image=w.RABBIT)
            moved_matrix[move_tuple[0]][move_tuple[1]] = 1

    def move(self, x_pos, y_pos, neighbourhood, max_x, max_y, plane, moved_matrix):
        """Performs a move of an agent."""
        if w.RABBIT_MOVE_COST_ENTRY_MEAN.get() <> '':
            move_energy_mean = float(w.RABBIT_MOVE_COST_ENTRY_MEAN.get())
        else:
            move_energy_mean = 0.5

        if w.RABBIT_MOVE_COST_ENTRY_VARIANCE.get() <> '':
            move_energy_variance = float(w.RABBIT_MOVE_COST_ENTRY_VARIANCE.get())
        else:
            move_energy_variance = 0

        move_energy = random_number_generator(move_energy_mean, move_energy_variance)
        move_energy = 0 if move_energy < 0 else move_energy

        self._energy -= move_energy
        moves = self.rule.move_set(x_pos, y_pos, neighbourhood, max_x, max_y)
        if self.die():
            self.rule.remove_agent(plane, x_pos, y_pos)
            return

        moves_counter = 0
        for i in range(0, len(moves)):
            if not moves[i] == w.NOT_POSSIBLE:
                moves_counter += 1

        move = None
        if moves_counter == 0:
            return
        else:
            while True:
                rand = randint(0, len(moves) - 1)
                if not moves[rand] == w.NOT_POSSIBLE:
                    move = rand
                    break

        if move == w.UP:
            self.rule.perform_move(self.app, plane, x_pos, y_pos, x_pos - 1, y_pos)
            x_pos = x_pos - 1
        if move == w.DOWN:
            self.rule.perform_move(self.app, plane, x_pos, y_pos, x_pos + 1, y_pos)
            x_pos = x_pos + 1
        if move == w.LEFT:
            self.rule.perform_move(self.app, plane, x_pos, y_pos, x_pos, y_pos - 1)
            y_pos = y_pos - 1
        if move == w.RIGHT:
            self.rule.perform_move(self.app, plane, x_pos, y_pos, x_pos, y_pos + 1)
            y_pos = y_pos + 1

        moved_matrix[x_pos][y_pos] = 1
        self.reproduce(plane, x_pos, y_pos, max_x, max_y, moved_matrix)


class WolfAgent(Agent):
    """Wolf agent class."""
    def __init__(self, app, image, rule):
        super(WolfAgent, self).__init__(image, rule)
        self._app = app

        if w.WOLF_ENERGY_ENTRY_MEAN.get() <> '':
            wolf_mean = float(w.WOLF_ENERGY_ENTRY_MEAN.get())
        else:
            wolf_mean = 10

        if w.WOLF_ENERGY_ENTRY_VARIANCE.get() <> '':
            wolf_variance = float(w.WOLF_ENERGY_ENTRY_VARIANCE.get())
        else:
            wolf_variance = 0

        wolf_energy = random_number_generator(wolf_mean, wolf_variance)
        wolf_energy = 0 if wolf_energy < 0 else wolf_energy

        self._energy = wolf_energy

        if w.BIRTHDAY_WOLF_ENTRY_MEAN.get() <> '':
            wolf_mean = float(w.BIRTHDAY_WOLF_ENTRY_MEAN.get())
        else:
            wolf_mean = 20

        if w.BIRTHDAY_WOLF_ENTRY_VARIANCE.get() <> '':
            wolf_variance = float(w.BIRTHDAY_WOLF_ENTRY_VARIANCE.get())
        else:
            wolf_variance = 0

        wolf_threshold = random_number_generator(wolf_mean, wolf_variance)
        wolf_threshold = 0 if wolf_threshold < 0 else wolf_threshold

        self._condition = wolf_threshold

    @property
    def condition(self):
        """Returns birthday threshold."""
        return self._condition

    @property
    def app(self):
        """Returns application"""
        return self._app

    def move(self, x_pos, y_pos, neighbourhood, max_x, max_y, plane, moved_matrix):
        """Performs a move of an agent."""
        if w.WOLF_MOVE_COST_ENTRY_MEAN.get() <> '':
            move_energy_mean = float(w.WOLF_MOVE_COST_ENTRY_MEAN.get())
        else:
            move_energy_mean = 0.5

        if w.WOLF_MOVE_COST_ENTRY_VARIANCE.get() <> '':
            move_energy_variance = float(w.WOLF_MOVE_COST_ENTRY_VARIANCE.get())
        else:
            move_energy_variance = 0

        move_energy = random_number_generator(move_energy_mean, move_energy_variance)
        move_energy = 0 if move_energy < 0 else move_energy

        self._energy -= move_energy
        moves = self.rule.move_set(x_pos, y_pos, neighbourhood, max_x, max_y)
        if self.die():
            self.rule.remove_agent(plane, x_pos, y_pos)
            return

        moves_counter = 0
        for i in range(0, len(moves)):
            if not moves[i] == w.NOT_POSSIBLE:
                moves_counter += 1

        move = None
        if moves_counter == 0:
            return
        else:
            while True:
                rand = randint(0, len(moves) - 1)
                if not moves[rand] == w.NOT_POSSIBLE:
                    move = rand
                    break

        if move == w.UP:
            self.rule.perform_move(self.app, plane, x_pos, y_pos, x_pos - 1, y_pos)
            moved_matrix[x_pos - 1][y_pos] = 1
        if move == w.DOWN:
            self.rule.perform_move(self.app, plane, x_pos, y_pos, x_pos + 1, y_pos)
            moved_matrix[x_pos + 1][y_pos] = 1
        if move == w.LEFT:
            self.rule.perform_move(self.app, plane, x_pos, y_pos, x_pos, y_pos - 1)
            moved_matrix[x_pos][y_pos - 1] = 1
        if move == w.RIGHT:
            self.rule.perform_move(self.app, plane, x_pos, y_pos, x_pos, y_pos + 1)
            moved_matrix[x_pos][y_pos + 1] = 1

    def add_energy(self, energy):
        """Adds energy to agent's energy."""
        self._energy += energy

    def reproduce(self, plane, row, column, max_row, max_column, moved_matrix):
        """Agent reproduces (if it is possible due to energy constraints)"""
        reproduce_set = []
        if row <> 0:
            if (not plane.widgets[row - 1][column].image == w.WOLF and
                    not plane.widgets[row - 1][column].image == w.RABBIT):
                reproduce_set.append((row - 1, column))
        if row <> max_row:
            if (not plane.widgets[row + 1][column].image == w.WOLF and
                    not plane.widgets[row + 1][column].image == w.RABBIT):
                reproduce_set.append((row + 1, column))
        if column <> 0:
            if (not plane.widgets[row][column - 1].image == w.WOLF and
                    not plane.widgets[row][column - 1].image == w.RABBIT):
                reproduce_set.append((row, column - 1))
        if column <> max_column:
            if (not plane.widgets[row][column + 1].image == w.WOLF and
                    not plane.widgets[row][column + 1].image == w.RABBIT):
                reproduce_set.append((row, column + 1))

        if len(reproduce_set) == 0:
            return

        rand = randint(0, len(reproduce_set) - 1)

        if self.energy >= self.condition:
            move_tuple = reproduce_set[rand]
            self.add_energy(-0.5 * self.condition)
            plane.widgets[move_tuple[0]][move_tuple[1]].agent = WolfAgent(self.app, self.image,
                                                                          self.rule)
            plane.widgets[move_tuple[0]][move_tuple[1]].image = w.WOLF
            plane.widgets[move_tuple[0]][move_tuple[1]].configure(image=w.WOLF)
            moved_matrix[move_tuple[0]][move_tuple[1]] = 1


class GrassAgent(Agent):
    """Grass agent class."""
    def __init__(self, app, image, rule):
        super(GrassAgent, self).__init__(image, None)
        self._app = app

        if w.GRASS_ENERGY_ENTRY_MEAN.get() <> '':
            grass_mean = float(w.GRASS_ENERGY_ENTRY_MEAN.get())
        else:
            grass_mean = 1

        if w.GRASS_ENERGY_ENTRY_VARIANCE.get() <> '':
            grass_variance = float(w.GRASS_ENERGY_ENTRY_VARIANCE.get())
        else:
            grass_variance = 0

        grass_energy = random_number_generator(grass_mean, grass_variance)
        grass_energy = 0 if grass_energy < 0 else grass_energy

        self._energy = grass_energy

    @property
    def app(self):
        """Returns application."""
        return self._app

    @property
    def energy(self):
        """Returns energy"""
        return self._energy

    def move(self, x_pos, y_pos, neighbourhood, max_x, max_y, plane, moved_matrix):
        """Performs move."""
        return None
