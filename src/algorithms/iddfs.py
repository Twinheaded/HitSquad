from .search_method import SearchMethod

class IDDFS(SearchMethod):
    name = "IDDFS"

    def search(self):
        goal_test, get_actions = self.problem.goal_test, self.problem.get_actions # Methods


        ## TODO: Convert to OOP


        ################
        self.print_state(node, get_actions(node)) # <-- For debugging only
        ################
        return None
