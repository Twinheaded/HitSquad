from src.file_parser import FileParser

from src.site import Site
from src.link import Link
from src.traffic_problem import TrafficProblem

from src.algorithms.search_method import SearchMethod
from src.algorithms.bfs import BFS
from src.algorithms.a_star import AS
from src.algorithms.bs import BS
from src.algorithms.dfs import DFS
from src.algorithms.gbfs import GBFS
from src.algorithms.iddfs import IDDFS

if __name__ == "__main__":
    fp = FileParser("Oct_2006_Boorondara_Traffic_Flow_Data.csv")
    fp.parse()

    # s1 = Site(1, (1,1), ["",""])
    # s2 = Site(2, (2,2), ["",""])
    # s3 = Site(3, (3,3), ["",""])
    # s4 = Site(4, (4,4), ["",""])
    # s5 = Site(5, (5,5), ["",""])
    # links = [
    #         Link(s1, s4, 12),
    #         Link(s2, s3, 23),
    #         Link(s4, s3, 23),
    #         Link(s4, s5, 23),
    #         Link(s5, s2, 23),
    #         Link(s2, s1, 23),
    #         ]

    # p1 = TrafficProblem([s1, s2, s3, s4], s4, s1, links)

    # searchObj = IDDFS(p1)
    # searchObj.search()
    # print(searchObj.result)
