
# class State:
#     def __init__(self, node_id, path):
#         """This represents a coordinate"""
#         self.node_id = node_id
#         self.path = []

#     def __repr__(self):
#         return f"{self.state_id}"

#     def __eq__(self, other):
#         return isinstance(other, State) and self.state_id == other.state_id

#     # The object will be referred to by its hash value instead of the object itself
#     def __hash__(self):
#         return hash(self.node_id)
