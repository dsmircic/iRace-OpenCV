import cv2
import argparse
import numpy as np
import logging
import os

CIRCLE_RADIUS = 50
NOT_REALLY_USEFUL = 0
WORKING_DIRECTORY = os.getcwd()

def findCircle (dp: int, minDist: int, param1: int, param2: int, minRadius: int, maxRadius: int, datfile: str):
	# the image of the blurred circle we want to find, the blurring happens in the imageCreator.py script
	image = cv2.imread(f'{WORKING_DIRECTORY}/../Images/blurred_circle.png', cv2.IMREAD_GRAYSCALE)

	detectedCircles = cv2.HoughCircles(
		image=image, 
		method=cv2.HOUGH_GRADIENT, 
		dp=dp, 
		minDist=minDist, 
		param1=param1, 
		param2=param2, 
		minRadius=minRadius, 
		maxRadius=maxRadius
	)

	if detectedCircles is not None:
		detectedCircles = np.uint16(np.around(detectedCircles))

		# rSum = 0
		rList = list()
		cnt = 0

		for pt in detectedCircles[0, :]:
			# pt is an object which contains the x and y coordinates of the circle's focus,
			# the third parameter represents the radius
			r = pt[2]

			# rSum += r
			rList.append(r)
			cnt += 1

		# radiusAverage = rSum / cnt
		minFound = min(rList)
		error = abs(minFound - CIRCLE_RADIUS)
		result = ((CIRCLE_RADIUS - error) / CIRCLE_RADIUS) * (100 / cnt)

		if (result < 0):
			with open(datfile, 'w') as file:
				file.write(str(NOT_REALLY_USEFUL))

		else:
			with open(datfile, 'w') as file:
				# rSum / cnt represents the average circle radius from the search algorithm
				# CIRCLE_RADIUS is the radius of the circle we are trying to find
				# result represents the score of each run, ideally we want the error to be 0, then the result would be 100
					# 100 represents the perfect score
					# score gets diminished if the program generated multiple circles, ideally we want only one
				# the result of running an instance must be written into the file given with the parameter --datfile
					# so iRace can determine which results it needs to discard
					# ideally, we want our score to be as close to a 100 as possible
				file.write(str(result))
		
	else:
		with open(datfile, 'w') as file:
			file.write(str(NOT_REALLY_USEFUL))


if __name__ == "__main__":
	ap = argparse.ArgumentParser(description='OpenCV optimization using iRace')
	ap.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
	ap.add_argument('--dp', dest='dp', type=int, required=True, help='The ratio of the resolution of original image to the accumulator matrix.')
	ap.add_argument('--minDist', dest='minDist', type=int, required=True, help='This parameter controls the minimum distance between detected circles.')
	ap.add_argument('--param1', dest='param1', type=int, required=True, help='Canny edge detection requires two parameters — minVal and maxVal. Param1 is the higher threshold of the two. The second one is set as Param1/2.')
	ap.add_argument('--param2', dest='param2', type=int, required=True, help='This is the accumulator threshold for the candidate detected circles. By increasing this threshold value, we can ensure that only the best circles, corresponding to larger accumulator values, are returned.')
	ap.add_argument('--minRadius', dest='minRadius', type=int, required=True, help='Minimum circle radius.')
	ap.add_argument('--maxRadius', dest='maxRadius', type=int, required=True, help='Maximum circle radius.')
	ap.add_argument('--datfile', dest='datFile', type=str, required=True, help='File where the score will be written into.')

	args = ap.parse_args()

	if args.verbose:
		logging.basicConfig(level=logging.DEBUG)

	logging.debug(args)

	findCircle(
		args.dp,
		minDist=args.minDist,
		param1=args.param1,
		param2=args.param2,
		minRadius=args.minRadius,
		maxRadius=args.maxRadius,
		datfile=args.datFile
	)