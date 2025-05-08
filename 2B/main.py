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

    problem = fp.create_problem()

    print("\nSITES\n================")
    print(problem.sites)

    print("\nINTERSECTIONS\n================")
    for s in problem.sites:
        print("\n", s.scats_num)
        for i in s.intersections:
            print(i.location)

    print("LINKS (filtered to just site 4043)\n================")
    sites = []
    for l in problem.links:
        if l.origin in problem.get_site_at_intersection(l):
            sites.append(problem.get_site_at_intersection(l))
    print(sites)

    # s1 = next(filter(lambda x: x.scats_num == '0970', fp.sites))

    # print(s1.scats_num, s1.roads)
    # print(s1.flow_records)



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
