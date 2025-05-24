from src import FileParser, TrafficProblem, ALGORITHMS
from src.gui import MapGUI

if __name__ == "__main__":
    origin = '2000'
    destination = '4043'

    fp = FileParser("Oct_2006_Boorondara_Traffic_Flow_Data.csv")
    fp.parse()
    problem = fp.create_problem(origin, destination) # Arguments: origin, destination

    searchObj = ALGORITHMS['DFS'](problem)
    searchObj.search()

    mp = MapGUI(problem.sites, origin, destination, searchObj.final_path)
    mp.generate()
    mp.open()
