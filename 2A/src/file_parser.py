import regex as re

from .node import Node
from .problem import Problem

class FileParser:
    TEST_DIR_PATH = "src/tests/"
    def __init__(self):
        self.init = None        # <Node> - the first node of the search
        self.goal = []          # [<Node>, <Node>, ...] - a list of goal states
        self.nodes_by_id = {}
        self.edges = {}         # {<Node>:{<action>:<cost>, <action>:<cost>, ...}, ...}

    def create_problem(self):
        return Problem([n for n in self.nodes_by_id.values()], self.init, self.goal, self.edges)
        
    def parse(self, filename):
        format_error = "\nInput file is not written in the correct format.\n"
        self.nodes_by_id = {}
        f = open(self.TEST_DIR_PATH + filename, "r")
        assert f.readline().strip() == 'Nodes:', wrong_format_error
        node_str = f.readline().strip()        # Line under the 'Nodes:' heading
        while node_str != "Edges:":
            assert re.match(r'^\d+: \(\d+,\d+\)$', node_str), wrong_format_error # RegEx for '#: (#,#)'
            node_id, x, y = [int(x) for x in re.split(r'\D+', node_str[:-1])]
            self.nodes_by_id[node_id] = Node(node_id,(x,y))
            node_str = f.readline().strip()
        edge_str = f.readline().strip()        # Line under the 'Edges:' heading
        while edge_str:                        # Continue until an empty line
            # state      - the 'from' address (Int)
            # transition - the 'to' address (Node)
            # cost       - the expense of traversing (Int)
            assert re.match(r'^\(\d+,\d+\): \d+$', edge_str)  # RegEx for the text format, '(#,#): #'
            s, t, c = [int(x) for x in re.split(r'\D+', edge_str[1:])]
            s = self.nodes_by_id[s]
            t = self.nodes_by_id[t]
            # Connect s -> t by an edge with a cost of c
            if s in self.edges:
                self.edges[s].update({t:c})
            else:
                self.edges[s] = {t:c}
            edge_str = f.readline().strip()
        assert f.readline().strip() == 'Origin:', wrong_format_error
        self.init = self.nodes_by_id[int(f.readline())]    # initial - the first node of the problem (Node)
        assert f.readline().strip() == 'Destinations:', wrong_format_error
        dest_str = f.readline().strip()         # Line under the 'Destinations:' heading
        assert re.match(r'^\d+(; \d+)*$', dest_str), wrong_format_error # RegEx for '#' or '#; #; ... #'
        self.goal = [self.nodes_by_id[int(i)] for i in dest_str.split(";")] # [<Node>,<Node>,...]
