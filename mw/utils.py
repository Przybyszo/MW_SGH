import world
import random

def random_number_generator(mean, variance):
	if world.distribution == 'NORMAL':
		return random.gauss(mean, variance)
	return None
