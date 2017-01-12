"""Package holding utility functions."""

import random
import world

def random_number_generator(mean, variance):
    """Returns a random number according to specified distribution."""
    if world.DISTRIBUTION == 'NORMAL':
        return random.gauss(mean, variance)
    return None
