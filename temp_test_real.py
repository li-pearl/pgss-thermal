import time
import busio
import board
import adafruit_amg88xx
import matplotlib.pyplot as plt
#from colorama import Fore
import numpy as np
from scipy.ndimage import zoom
i2c = busio.I2C(board.SCL, board.SDA)
amg = adafruit_amg88xx.AMG88XX(i2c)
while True:
	matrix = []
	for row in amg.pixels:
		matrixRow = []
		for temp in row:
			numTemp = '{0:.1f}'.format(temp)
			matrixRow.append(float(numTemp))
		matrix.append(matrixRow)
	time.sleep(1) #time.sleep(0.001)
	matrix = np.array(matrix)
	upscaled_grid = zoom(matrix, 4, order=3)
	ret = ""
	for rows in upscaled_grid:
		for vals in rows:
			ret += str(vals) + " "
		ret += "\n"
	plt.figure(figsize=(8,8))
	plt.imshow(upscaled_grid, cmap='plasma', interpolation='bicubic', vmin=20, vmax=34) #plt.imshow(upscaled_grid, cmap='plasma', interpolation='bicubic', vmin=15, vmax=38)
	plt.colorbar(label='Temperature (Celsius)')
	plt.title('Thermal Sensor Readings')
	plt.show()
