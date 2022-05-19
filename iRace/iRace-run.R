library(irace)

# C:\\Users\\dinos\\OneDrive\\Faks\\3. Godina\\6. Semestar\\Zavrsni\\iRace\\

# Create the R objects scenario and parameters
parameters <- readParameters("iRace/parameters.txt")
scenario <- readScenario(filename = "iRace/scenario.txt", scenario = defaultScenario())
irace(scenario = scenario, parameters = parameters)