from PIL import Image
from random import randint
from math import ceil
from copy import deepcopy
import numpy as np


COUNT = 2

image = None
width, height = 0, 0
speciments = []
top_speciments = []
best = []
generation = 1

DIV_FACTOR = 10


def load_image(path):
	global width, height, image
	im = Image.open(path).getdata()
	image = np.array(list(im))
	width, height = im.size
	


def mutate():
	global speciments, width, height, image, best, DIV_FACTOR
	for spec in speciments:
		x = randint(0, width - 2)
		y = randint(0, height - 2)
		w = min(randint(1, width - x - 1), ceil(width / DIV_FACTOR))
		h = min(randint(1, height - y - 1), ceil(height / DIV_FACTOR))
		start = y*width + x
		color_R = randint(0, 255)
		color_G = randint(0, 255)
		color_B = randint(0, 255)
		for j in range(h):
			for i in range(w):
				current = start + width*j+i
				new_R = (spec[current][0] + color_R) // 2
				new_G = (spec[current][1] + color_G) // 2
				new_B = (spec[current][2] + color_B) // 2
				spec[current] = np.array([new_R, new_G, new_B])



def cross():
	global speciments
	temps = []
	for i, first in enumerate(speciments):
		for j, second in enumerate(speciments, i):
			tmp = first + second
			tmp = tmp // 2
			temps.append(tmp)
	speciments = temps




def score():
	global speciments, best, top_speciments
	spec_scores = deepcopy(top_speciments)
	for spec in speciments:
		result = 0.0
		tmp = np.subtract(spec, image)
		tmp = np.power(tmp, 2)
		tmp = np.true_divide(tmp, 2)
		result = np.sum(tmp)
		spec_scores.append((result, spec))

	spec_scores = sorted(spec_scores, key=lambda x: x[0])
	top_speciments = spec_scores[:COUNT]
	speciments = [deepcopy(y) for x, y in top_speciments]
	best = speciments[0]



def show():
	global best, generation
	if generation % 100 != 0:
		return
	data = [(x[0], x[1], x[2]) for x in best]
	with open("pictures4/Generation_{0}.jpg".format(generation), 'wb') as f:
		img = Image.new("RGB", (width, height))
		img.putdata(data)
		img.save(f)



def evolve():
	global generation, speciments, width, height, DIV_FACTOR
	im = Image.new("RGB", (width, height), "black").getdata()
	speciments = [np.array(list(im)) for i in range(COUNT*COUNT)]

	while True:
		mutate()

		generation+=1
		if generation % 10 == 0:
			print("GENERATION: ", generation)
		if generation % (20000 * DIV_FACTOR // 5) == 0:
			DIV_FACTOR *= 2

		score()

		show()
		
		cross()



load_image("mona.jpg")
evolve()