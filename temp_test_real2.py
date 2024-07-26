import time
import busio
import board
import adafruit_amg88xx
import numpy as np
from scipy.ndimage import zoom
i2c = busio.I2C(board.SCL, board.SDA)
amg = adafruit_amg88xx.AMG88XX(i2c)

#vars
max_storage_size = 400
sensitivity = 0.45
val_dp = 0
avg_dp = 4
sigmoid_constant = .75
sigmoid_depth = 6
	#0 = adaptive to environment; 1 = set calibration
mode = 1
sleepTime = .01
counter = 0


#
def sigmoid1(x):
	return 1/(1+np.exp(-sigmoid_depth * (x-sigmoid_constant)))

storage = ['{0:.1f}'.format(amg.pixels[0][0])]
cal_storage = ['{0:.1f}'.format(amg.pixels[0][0])]
while True:
	counter += 1
	matrix = []
	for row in amg.pixels:
		matrixRow = []
		sum = 0.0
		count = 0.0
		for temp in row:
			numTemp = '{0:.1f}'.format(temp)
			matrixRow.append(float(numTemp))
			sum += float(numTemp)
			count += 1.0
		matrix.append(matrixRow)

	# Average Calcs
	avg = sum/count
	if len(storage) > max_storage_size and mode == 0:
		storage.pop(0)
		storage.append(avg)
	elif mode == 0:
		storage.append(avg)
	elif len(cal_storage) < max_storage_size and mode == 1:
		cal_storage.append(avg)
	#Upscale Grid
	matrix = np.array(matrix)
	upscaled_grid = zoom(matrix, 4, order=3)

	#Convert to String and round
	ret = ""
	for rows in upscaled_grid:
		for vals in rows:
			new_val = int(round(vals, val_dp))
			ret += str(new_val) + " "
		ret += "\n"
	print(ret)
	print("Average Temperature: " + str(round(avg,avg_dp)))

	#Check if Heat Detected
	storage_avg = 0.0
	storage_sum = 0.0
	step = 0.0
	if mode == 0:
		for vals in storage:
			step += 1.0
			storage_sum += float(vals)
	if mode == 1:
		for vals in cal_storage:
			step += 1.0
			storage_sum += float(vals)
	#storage_avg = storage_sum/step
	storage_avg = 23.4875
	confidence = sigmoid1(abs(storage_avg-avg))*100
	print("Confidence: " + str(confidence))

	print(len(cal_storage))
	if len(storage) < max_storage_size and mode == 0:
		print("Storage Average: " + str(round(storage_avg, avg_dp)))
	elif mode == 0:
		print("Storage Average: " + str(round(storage_avg, avg_dp)) + '*')
	if len(cal_storage) < max_storage_size and mode == 1:
		print("Storage Average: " + str(round(storage_avg, avg_dp)))
	elif mode == 1:
		print("Storage Average: " + str(round(storage_avg, avg_dp)) + "*")
	#TEST print(upscaled_grid.shape)
	if counter <= 400:
		time.sleep(sleepTime)
	else:
		time.sleep(2)
