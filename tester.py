from dataclasses import dataclass
import cv2
import numpy as np
import os
import csv
import sys

from FindCircle import WORKING_DIRECTORY

# source: https://www.geeksforgeeks.org/circle-detection-using-opencv-python/

WORKING_DIRECTORY = os.getcwd()

@dataclass
class Result:
	dp: int
	minDist: int
	param1: int
	param2: int
	minR: int
	maxR: int

def readResults () -> Result:
	csvFile = open("Results/results.csv")
	csvReader = csv.reader(csvFile)
	header = next(csvReader)

	configuration = next(csvReader)
	dp = int(configuration[header.index("dp")])
	minDist = int(configuration[header.index("minDist")])
	param1 = int(configuration[header.index("param1")])
	param2 = int(configuration[header.index("param2")])
	maxR = int(configuration[header.index("maxRadius")])
	minR = int(configuration[header.index("minRadius")])
	csvFile.close()

	result = Result(
		dp = dp,
		minDist = minDist,
		param1 = param1,
		param2 = param2,
		minR = minR,
		maxR = maxR
	)

	return result

def detectCircles (result: Result):
	# Read image.
	img = cv2.imread(f'{WORKING_DIRECTORY}/Images/{sys.argv[1]}', cv2.IMREAD_COLOR)

	# Convert to grayscale.
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	# Blur using 3 * 3 kernel.
	gray_blurred = cv2.blur(gray, (3, 3))
	

	# Apply Hough transform on the blurred image.
	detected_circles = cv2.HoughCircles(
		gray_blurred,
		cv2.HOUGH_GRADIENT, 
		dp = result.dp, 
		minDist = result.minDist, 
		param1 = result.param1,
		param2 = result.param2,
		minRadius = result.minR, 
		maxRadius = result.maxR
	)

	# Draw circles that are detected.
	if detected_circles is not None:

		# Convert the circle parameters a, b and r to integers.
		detected_circles = np.uint16(np.around(detected_circles))

		for pt in detected_circles[0, :]:
			a, b, r = pt[0], pt[1], pt[2]

			# Draw the circumference of the circle.
			cv2.circle(img, (a, b), r, (0, 255, 0), 2)

			# Draw a small circle (of radius 1) to show the center.
			cv2.circle(img, (a, b), 1, (0, 0, 255), 3)
			cv2.imshow("Detected Circle", img)

if __name__ == "__main__":

	if (os.path.exists("Results/results.csv")):
		result = readResults()
		detectCircles(result)
	else:
		badResults = Result(1, 5, 50, 11, 10, 200)
		detectCircles(badResults)

	cv2.waitKey(0)
	