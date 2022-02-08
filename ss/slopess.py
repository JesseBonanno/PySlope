#note: plan to use JSX Graph for interactive web application.
#user can click a node and move it or delete it. (deleting it just removes the id from all lists)
# user can click a line and delete it, or add a node on the line
# user can add material boundaries using coordinates
# user can use coordinates to move nodes relatively or absolutely and same with lines or they can just move the whole line.
# user can assign materials to a particular location (changes the polygon color) (might be hard)
# material boundary might need to be based on an invisible node.

# should stop creating my own methods and should try to use SymPy to simplify my own code.

from math import sqrt, acos, pi

class Node:
    def __init__(self,Id,x,y):
        self.Id = Id
        self.x = x
        self.y = y

    def __str__(self):
        return f'Node {self.Id}: ({self.x}, {self.y})'


def length(n1, n2):
    return sqrt((n1.x - n2.x)**2 + (n1.y - n2.y)**2)

def check_ccw(a,b,c):
    # take 3 nodes and determine if order is ccw
    return (b.x - a.x) * (c.y - a.y) - (c.x - a.x) * (b.y - a.y)    

def lines_intersect(a,b,c,d):
    # let a and b be the points for one line
    # let c and d be the points for another line

    # check opposite rotation for both lines to each node of other line
    # https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
    return (check_ccw(a,c,d) != check_ccw(b,c,d)) and (check_ccw(a,b,c) != check_ccw(a,b,d))

def intersection(a,b,c,d):
    # let a and b be the points for one line
    # let c and d be the points for another non-parellel line

    # find the coordinates of the point of intersection
    l1 = 
class Slope:
    def __init__(self):
        # list of all nodes associated with the model
        self.nodes = []
        self.last_node_id = 0

    def add_node(self, x,y):
        # method helps manage duplicate and assigning Ids

        # loop through existing nodes
        for node in self.nodes:
            Id1, x1, y1 = node.Id, node.x, node.y

            # if coordinates are the same as an existing
            # dont create a new node, return the id for existing
            if x1 == x and y1 == y:
                return node

        # if node doesnt yet exist then create node
        # Get an id for the new node
        Id = self.last_node_id + 1
        self.last_node_id += 1

        node = Node(Id, x, y)
        self.nodes.append(node)
        return node

    def remove_node_by_id(self, Id):
        # loop through existing nodes
        for node in self.nodes:

            # if node exists remove it
            if node.Id == Id:
                self.nodes.pop(node)

        print(f'Node {Id} does not exist. For reference the highest node assigned is Node {self.last_node_id}')

    def remove_node(self, n):
        # loop through existing nodes
        for node in self.nodes:

            # if node exists remove it
            if node == n:
                self.nodes.pop(node)
            

    def closest_node(self, x,y):
        # method to help with GUI in future

        # if no nodes raise an error
        if not self.nodes:
            raise ValueError('there are no nodes')

        # track the closest node
        n = None

        # loop through existing nodes
        for node in self.nodes:
            Id1, x1, y1 = node.Id, node.x, node.y

            # calculate eucledian distance
            distance = sqrt((x1-x)**2 + (y1-y)**2)

            # if id = 0 then this is the first node, use it to initialize
            if n == None:
                min_distance = distance
                n = node
            elif distance < min_distance:
                min_distance = distance
                n = node

        return n

    def get_node_by_id(self,node_Id):
        """ Returns node object with certain ID.

        Parameters
        ----------
        node_Id : int,
            Node ID.

        Returns
        -------
        Node
            Node object with ID specified.
        """
        for node in self.nodes:
            if node.Id == node_Id:
                return node
        return None

    def length(self, n1, n2):
        return sqrt((n1.x - n2.x)**2 + (n1.y - n2.y)**2)

    
    def create_external_boundary(self, *coordinates):
        # boundary can be a list of node Id's to help with editing
        external_boundary = []

        # this should be a step before all other steps
        # hence coordinates are used rather than actual nodes
        for x, y in coordinates:
            # add node, and get the Id of the created node
            n = self.add_node(x,y)
            if n not in external_boundary:
                external_boundary.append(n)
            elif n == external_boundary[0]:
                # technically if the last node isnt the one that closes there is a slight error
                # just assume that the first node to close is the final node.
                break

        # model should have at least 3 nodes
        if len(external_boundary) < 3:
            raise ValueError('should be at lesat 3 nodes for external boundary')
        
        # validate external boundary doesnt double back on itself to prevent other
        # modelling / calculation issues
        switch_count = 0
        n1 = external_boundary[-3]
        n2 = external_boundary[-2]
        for n3 in external_boundary:
            if n1.x <= n2.x and n2.x <= n3.x:
                continue
            elif n1.x >= n2.x and n2.x >= n3.x:
                continue
            else:
                switch_count+=1
            n1 = n2
            n2 = n3

        if switch_count > 2:
            # shouldt be more than two switches in x direction
            raise ValueError('the external boundary does not appear to be valid') 

        self.external_boundary = external_boundary







    









        
        
        