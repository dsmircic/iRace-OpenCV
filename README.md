## iRace optimization
This program lets you optimize parameters for circle detection with known radiuses in OpenCV. The parameters and their uses are described in the FindCircle.py script.

### Requirements: 
	- install the latest version of R
	- from the R command line, install iRace with _packages.install("irace")_

### Usage:
	- run the _ImageCreator.py_ script to generate a blurred image of the circle you want to detect (this is so that _HoughDetection_ method can work with something)
	- run the _tester.py_ script to visualize detection results before optimization
	- (Optional) configure the number of iterations (maxExperiments) in the scenario.txt file, it is currently set to 1600, so it takes a few minutes
	- from the iRace directory, run the _iRace-run.R_ script to perform algorithm optimization
	- wait for the program to finish and return the optimal algorithm parameters
	- run the _tester.py_ script with the obtained parameters and see the results
	
### Implementation details
The _parameters.txt_ file in the iRace directory contains the parameters and their respective ranges which will be passed to the _FindCircle.py_ script through statistical filtering.

The _target_runner_ is an executable file which represents an interface between iRace and the _FindCircle.py_ script. This file passes arguments to the script.

The _scenario.txt_ file in the iRace directory gives a description of the optimization environment and it provides paths to the _parameters.txt_ file and the _forbidden.txt_ file.

The _forbidden.txt_ file contains configurations which are not allowed in the main program.

After each set of configurations was run on a given instance, the _FindCircle.py_ script is required to write down the score of the run which is used by iRace to determine how useful the configuration was. This is done by dividing the average radius of the circles which were found (note that with "bad" parameters, the _FindCircle.py_ script detects multiple circles while there is only one), with the actual circle radius. This is converted into a percentage and divided with the number of circles detected. iRace wants to maximise this score, this is why we need to divide the result with the number of circles detected, because we need to "discourage" the algorithm from finding circles which are not there. This means that only the best configurations will "survive" each run.
