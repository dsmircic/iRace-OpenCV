## iRace optimization
This program lets you optimize parameters for circle detection with known radiuses in OpenCV. The parameters and their uses are described in the FindCircle.py script.

### Requirements: 
	- install the latest version of R
	- from the R command line, install iRace with _packages.install("irace")_

### Usage:
	- run the _runner_ bash script from the terminal
		- when asked for an image name, the best results can be obtained with the "multiple_circles.png" image 
		- firstly, it will display the circles which were found with bad parameters
		- secondly, it will run the iRace optimizer to find the parameters for the smallest circle (radius 50)
		- lastly, it will display the circle which was found with the parameters from the iRace optimizer
	- (Optional) configure the number of iterations (maxExperiments) in the scenario.txt file, it is currently set to 1600, so it takes a few minutes
	
### Implementation details
The _parameters.txt_ file in the iRace directory contains the parameters and their respective ranges which will be passed to the _FindCircle.py_ script through statistical filtering.

The _target_runner_ is an executable file which represents an interface between iRace and the _FindCircle.py_ script. This file passes arguments to the script.

The _scenario.txt_ file in the iRace directory gives a description of the optimization environment and it provides paths to the _parameters.txt_ file and the _forbidden.txt_ file.

The _forbidden.txt_ file contains configurations which are not allowed in the main program.

The _iRace-run.R_ script will run the optimization algorithm with the parameters which were specified from the _parameters.txt_. After the optimization, the results will be written into _Results/results.csv_ file.

The _tester.py_ script tests out the result of the optimization if there is a _Results/results.csv_ file, if there isn't one, it is run with the default settings (bad parameters).

After each set of configurations was run on a given instance, the _FindCircle.py_ script is required to write down the score of the run which is used by iRace to determine how useful the configuration was. This is done by dividing the average radius of the circles which were found (note that with "bad" parameters, the _FindCircle.py_ script detects multiple circles, but we want to find only one, that being the smallest one), with the actual circle radius. This is converted into a percentage and divided with the number of circles detected. If the result is negative, that means that the circles which were found are larger than the one we are trying to find, so we will mark that run with a score of 0. iRace wants to maximise this score, this is why we need to divide the result with the number of circles detected, because we need to "discourage" the algorithm from finding circles which are not there. This means that only the best configurations will "survive" each run.
