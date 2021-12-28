from math import sqrt

class Node:
    def __init__(self,Id,x,y):
        self.Id = Id
        self.x = x
        self.y = y

    def __str__(self):
        return f'Node {self.Id}: ({self.x}, {self.y})'

class Slope:
    def __init__(self):
        # list of all nodes associated with the model
        self.nodes = []
        self.last_node_id = 0

    def add_node(x,y):
        # method helps manage duplicate and assigning Ids

        # loop through existing nodes
        for node in self.nodes:
            Id1, x1, y1 = node.Id, node.x, node.y

            # if coordinates are the same as an existing
            # dont create a new node, return the id for existing
            if x1 == x and y1 == y:
                return Id1

        # if node doesnt yet exist then create node
        # Get an id for the new node
        Id = self.last_node_id + 1
        self.last_node_id += 1

        node = Node(Id, x, y)
        self.nodes.append(node)
        return Id

    def remove_node(Id):
        # loop through existing nodes
        for node in self.nodes:

            # if node exists remove it
            if node.Id == Id:
                self.nodes.pop(node)

        print(f'Node {Id} does not exist. For reference the highest node assigned is Node {self.last_node_id}')

    def closest_node(x,y):
        # method to help with GUI in future

        # if no nodes raise an error
        if not self.nodes:
            raise ValueError('there are no nodes')

        # track the Id of the closest node
        Id = None

        # loop through existing nodes
        for node in self.nodes:
            Id1, x1, y1 = node.Id, node.x, node.y

            # calculate eucledian distance
            distance = sqrt((x1-x)**2 + (y1-y)**2)

            # if id = 0 then this is the first node, use it to initialize
            if Id == None:
                min_distance = distance
                Id = Id1
            elif distance < min_distance:
                min_distance = distance
                Id = Id1

        return Id

    
    def create_external_boundary(*coordinates):
        # boundary can be a list of node Id's to help with editing
        self.external_boundary = []

        # this should be a step before all other steps
        # hence coordinates are used rather than actual nodes
        for x, y in coordinates:
            # add node, and get the Id of the created node
            Id = self.add_node(x,y)
            self.external_boundary.append(Id)

        # dont allow same node twice (maybe the GUI can handle this)
        # dont allow doubling back in geometry, external boundary
        # should be circular in nature




    









        
        
        