"""This module specifies movement rules for a given agent."""

import world as w
from agent import GrassAgent

class Rule(object):
    """Container for the agent's movement boundaries"""
    @staticmethod
    def move_set(x_pos, y_pos, neighbourhood, max_x, max_y):
        """Returns possible moveset of an agent."""
        moveset = [w.POSSIBLE] * 4
        if x_pos == 0:
            moveset[w.UP] = w.NOT_POSSIBLE
        if x_pos == max_x:
            moveset[w.DOWN] = w.NOT_POSSIBLE
        if y_pos == 0:
            moveset[w.LEFT] = w.NOT_POSSIBLE
        if y_pos == max_y:
            moveset[w.RIGHT] = w.NOT_POSSIBLE
        return moveset

    @staticmethod
    def perform_move(app, plane, src_x, src_y, dest_x, dest_y):
        """Performs move of an agent on a table."""
        pass

    @staticmethod
    def remove_agent(plane, x_coord, y_coord):
        """Removes agent from given position in a table."""
        plane.widgets[x_coord][y_coord].configure(image=w.EMPTY)
        plane.widgets[x_coord][y_coord].agent = None
        plane.widgets[x_coord][y_coord].image = w.EMPTY

class WolfRule(Rule):
    """Container for the wolf's movement boundaries"""
    def move_set(self, x_pos, y_pos, neighbourhood, max_x, max_y):
        """Returns possible moveset of an agent."""
        moveset = super(WolfRule, self).move_set(x_pos, y_pos, neighbourhood, max_x, max_y)
        for i in range(w.LEFT, w.DOWN + 1):
            if neighbourhood[i] == w.WOLF:
                moveset[i] == w.NOT_POSSIBLE
        return moveset

    @staticmethod
    def perform_move(app, plane, src_x, src_y, dest_x, dest_y):
        """Performs move of an agent on a table."""
        if (plane.widgets[dest_x][dest_y].image == w.EMPTY or
                plane.widgets[dest_x][dest_y].image == w.RABBIT):
            if plane.widgets[dest_x][dest_y].image == w.RABBIT:
                energy_to_be_added = plane.widgets[dest_x][dest_y].agent.energy
                plane.widgets[src_x][src_y].agent.add_energy(energy_to_be_added)
            if plane.widgets[src_x][src_y].image == w.WOLF_IN_GRASS:
                plane.widgets[dest_x][dest_y].agent = plane.widgets[src_x][src_y].agent
                plane.widgets[dest_x][dest_y].image = w.WOLF
                plane.widgets[dest_x][dest_y].configure(image=w.WOLF)
                plane.widgets[src_x][src_y].configure(image=w.GRASS)
                plane.widgets[src_x][src_y].agent = GrassAgent(app, w.GRASS, None)
                plane.widgets[src_x][src_y].image = w.GRASS
            else:
                plane.widgets[dest_x][dest_y].agent = plane.widgets[src_x][src_y].agent
                plane.widgets[dest_x][dest_y].image = plane.widgets[src_x][src_y].image
                plane.widgets[dest_x][dest_y].configure(image=plane.widgets[src_x][src_y].image)
                plane.widgets[src_x][src_y].configure(image=w.EMPTY)
                plane.widgets[src_x][src_y].agent = None
                plane.widgets[src_x][src_y].image = w.EMPTY
        elif plane.widgets[dest_x][dest_y].image == w.GRASS:
            if plane.widgets[src_x][src_y].image == w.WOLF_IN_GRASS:
                plane.widgets[dest_x][dest_y].agent = plane.widgets[src_x][src_y].agent
                plane.widgets[dest_x][dest_y].image = w.WOLF_IN_GRASS
                plane.widgets[dest_x][dest_y].configure(image=w.WOLF_IN_GRASS)
                plane.widgets[src_x][src_y].configure(image=w.GRASS)
                plane.widgets[src_x][src_y].agent = GrassAgent(app, w.GRASS, None)
                plane.widgets[src_x][src_y].image = w.GRASS
            else:
                plane.widgets[dest_x][dest_y].agent = plane.widgets[src_x][src_y].agent
                plane.widgets[dest_x][dest_y].image = w.WOLF_IN_GRASS
                plane.widgets[dest_x][dest_y].configure(image=w.WOLF_IN_GRASS)
                plane.widgets[src_x][src_y].configure(image=w.EMPTY)
                plane.widgets[src_x][src_y].agent = None
                plane.widgets[src_x][src_y].image = w.EMPTY

class RabbitRule(Rule):
    """Container for the rabbit's movement boundaries"""
    def move_set(self, x_pos, y_pos, neighbourhood, max_x, max_y):
        """Returns possible moveset of an agent."""
        moveset = super(RabbitRule, self).move_set(x_pos, y_pos, neighbourhood, max_x, max_y)
        for i in range(w.LEFT, w.DOWN + 1):
            if neighbourhood[i] == w.RABBIT or neighbourhood[i] == w.WOLF:
                moveset[i] == w.NOT_POSSIBLE
        return moveset

    @staticmethod
    def perform_move(app, plane, src_x, src_y, dest_x, dest_y):
        """Performs move of an agent on a table."""
        if plane.widgets[dest_x][dest_y].image == w.EMPTY:
            plane.widgets[dest_x][dest_y].agent = plane.widgets[src_x][src_y].agent
            plane.widgets[dest_x][dest_y].image = plane.widgets[src_x][src_y].image
            plane.widgets[dest_x][dest_y].configure(image=plane.widgets[src_x][src_y].image)
            plane.widgets[src_x][src_y].configure(image=w.EMPTY)
            plane.widgets[src_x][src_y].agent = None
            plane.widgets[src_x][src_y].image = w.EMPTY
        if plane.widgets[dest_x][dest_y].image == w.GRASS:
            plane.widgets[src_x][src_y].agent.add_energy(plane.widgets[dest_x][dest_y].agent.energy)
            plane.widgets[dest_x][dest_y].agent = plane.widgets[src_x][src_y].agent
            plane.widgets[dest_x][dest_y].image = plane.widgets[src_x][src_y].image
            plane.widgets[dest_x][dest_y].configure(image=plane.widgets[src_x][src_y].image)
            plane.widgets[src_x][src_y].configure(image=w.EMPTY)
            plane.widgets[src_x][src_y].agent = None
            plane.widgets[src_x][src_y].image = w.EMPTY
