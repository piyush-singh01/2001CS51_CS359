from datetime import datetime
from time import sleep
from queue import Queue
from threading import Thread
import logging

start_time = datetime.now()
logging.getLogger().setLevel(logging.INFO)



node_list = list()          # Contains node
edge_list = list(list())    # The edge list
router = dict()             # Contains class instance for each router
INF = 20000000

# A function to parse inputs from the 'topology.txt' file
def parseInputs():
    with open('topology.txt', 'r') as file:
        lines = file.readlines()

        nodes = lines[0]    # Get the first line of input, containing the list of all nodes
        lines.pop(0)        # Pop the first line of input, which contains the list of nodes.

        # Create an edge list from the rest of the lines in the format [first_node, second_node, edge_weight]
        nodes = nodes.strip()
        nodes = nodes.split(' ')
        for node in nodes:
            node_list.append(node)
        
        for line in lines:
            line = line.strip()
            # Break from the loop if end-of-file encountered
            if line == 'EOF':
                file.close()
                break

            line = line.strip()
            line = line.split(' ')

            edge = list()
            for i in range(0,3):
                edge.append(line[i])
            edge_list.append(edge)
        
        file.close()

# A class for each router
class Router:
    def __init__(self, _node):
        self.q = Queue()            
        self.neighbors = list()     # Contains the neighbors of this router's node
        self.distance_vector = {}   # Contains the distance vector of this router's node
        self.changed_list = list()  # List of nodes whose value in the distance vector table of this routers has changed
        self.node = _node

        self.distance_vector[self.node] = 0

        # Append values in neighbors and distance vector lists
        for edge in edge_list:
            node1 = edge[0]
            node2 = edge[1]
            wt = int(edge[2])

            if node1 == self.node or node2 == self.node:
                if node1 == self.node and node2 != self.node:
                    self.neighbors.append(node2)
                    self.distance_vector[node2] = wt
                elif node2 == self.node and node1 != self.node:
                    self.neighbors.append(node1)
                    self.distance_vector[node1] = wt

        
        for node in node_list:
            if node not in self.distance_vector:
                self.distance_vector[node] = INF
        

    # 'Getter' functions for various class data
    def getNode(self):
        return self.node
    
    def getNeighbors(self):
        return self.neighbors
    
    def getDistanceVector(self):
        return self.distance_vector
    
    def getChangedList(self):
        return self.changed_list
    
    def clearChangedList(self):
        self.changed_list.clear()

    # Computes changes in the distance vectors using the distance vectors from neighbors using the bellman-ford equation
    def compute(self):
        dv_neighbor, _node = self.q.get()
        for node in node_list:
            if node != self.node:
                if int(self.distance_vector[node]) > int(self.distance_vector[_node]) + int(dv_neighbor[node]):
                    self.distance_vector[node] = int(self.distance_vector[_node]) + int(dv_neighbor[node])
                    self.changed_list.append(node)

        self.q.task_done()
    

# For printing the table with '*' added to the changed values
def print_table(node, changed_list):
    num_spaces = 27
    print(f'For the node {node}, the routing table is:')
    print('_'*num_spaces)
    print("{:<1} {:<10} {:<1} {:<10} {:<1}".format('|', 'To_Node','|', 'Distance','|'))
    print('-'*num_spaces)
    
    for key, value in router[node].getDistanceVector().items():
        if key in changed_list:
            key = '*' + str(key)
        if value == INF:
            value = 'INF'
        print("{:<1} {:<10} {:<1} {:<10} {:<1}".format('|', key, '|', value,'|'))
    print('_'*num_spaces, '\n\n')

# A utility function for printing all tables
def print_all_tables(changes):
    for node in node_list:
        if node not in changes:
            sleep(0.1)
            print_table(node, [])
        else:
            sleep(0.1)
            print_table(node, changes[node])


def Main():
    parseInputs()               # Parse inputs from the 'topology.txt' file
    compute_list = list()       # List of nodes whose routing table has changed in the current iteration
    for node in node_list:
        router[node] = Router(node)
        compute_list.append(node)   # Initially, we have all the nodes in the compute list

    # Print initial configuration
    iteration_number = 0
    print("The initial configuration is as follows")
    print_all_tables({})
    iteration_number+=1

    # While there are items in the compute list
    while len(compute_list) > 0:
        print("Sleeping for 2 seconds...")
        sleep(2)
        print("Iteration number:", iteration_number)

        threads = list()
        changed_list = {}
        for node in compute_list:
            for neighbors in router[node].getNeighbors():
                router[neighbors].q.put((router[node].getDistanceVector(), node))
                thread = Thread(target=router[neighbors].compute())
        
        # All threads for this iteration are started only when all the changes have been pushed into each routers queues
        # This ensures starts computation only when ALL distance vectors have been received by neighbors
        for thread in threads:
            thread.start()

        new_compute_list = list()
        for node in compute_list:
            router[node].q.join()       # Will proceed only when all tasks in the queue have been processed
            changed_list[node] = router[node].getChangedList()[:]
            if len(changed_list[node]) > 0:
                new_compute_list.append(node)
                router[node].clearChangedList()
        
       
        print_all_tables(changed_list)
        changed_list.clear()
        compute_list.clear()
        compute_list = new_compute_list[:]
        new_compute_list.clear()

        iteration_number+=1

    print(f'No Routing Table was changed in the last iteration.')

if __name__ == '__main__':
    Main()


#This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))