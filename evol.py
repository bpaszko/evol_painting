from PIL import Image
from random import randrange
from math import ceil
from copy import deepcopy
import numpy as np


COUNT = 2

image = None
width, height = 0, 0
speciments = []
top_speciments = []
best = []
generation = 134800



def load_image(path):
	global width, height, image
	im = Image.open(path).getdata()
	image = np.array(list(im))
	width, height = im.size
	


def mutate():
	global speciments, width, height, image, best
	for spec in speciments:
		x = randrange(width - 1)
		y = randrange(height - 1)
		w = min(randrange(1, width - x ), ceil(width // 60))
		h = min(randrange(1, height - y ), ceil(height // 60))
		start = y*width + x
		color_R = randrange(256)
		color_G = randrange(256)
		color_B = randrange(256)
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
	with open("pictures/Generation_{0}.jpg".format(generation), 'wb') as f:
		img = Image.new("RGB", (width, height))
		img.putdata(data)
		img.save(f)



def evolve():
	global generation, speciments, width, height
	im = Image.new("RGB", (width, height), "black").getdata()
	speciments = [np.array(list(im)) for i in range(COUNT*COUNT)]

	im = Image.open('pictures/Generation_134800.jpg').getdata()
	speciments.append(np.array(list(im)))

	while True:
		mutate()
		generation+=1
		if generation % 10 == 0:
			print("GENERATION: ", generation)
		
		score()

		show()
		#if generation >= 20: 
		#	break
		cross()



load_image("lena.jpg")
evolve()