from datetime import datetime
from time import sleep
from queue import PriorityQueue
from threading import Thread, Semaphore
import logging

start_time = datetime.now()
logging.getLogger().setLevel(logging.INFO)


node_list = list()          # Contains node
adjacency_list = dict()     # An adjacency list
router = dict()             # Contains class instance for each router
semaphore = dict()          # Contains semaphores corresponding to each node
locked = 0                   # Number of semaphores that are locked
INF = 20000000
num_nodes=0

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
            global num_nodes
            num_nodes+=1
            node_list.append(node)
            adjacency_list[node] = list()
        

        for line in lines:
            line = line.strip()
            # Break from the loop if end-of-file encountered
            if line == 'EOF':
                file.close()
                break

            line = line.strip()
            line = line.split(' ')

            # edge = list()
            adjacency_list[line[0]].append((line[1], int(line[2])))
            adjacency_list[line[1]].append((line[0], int(line[2])))

        file.close()
    
    for node in node_list:
        semaphore[node] = Semaphore(1)


# A class for each router
# Here, each Router has access to edge list and node list
class Router:
    def __init__(self, _node):
        self.node = _node
        self.pq = PriorityQueue()
        self.routing_table = dict()
        self.changed_list = list()  # List of nodes whose value has changed in the last iteration
        for node in node_list:
            self.routing_table[node] = int(INF)

        self.routing_table[self.node] = int(0)


    def get_node(self):
        return self.node
    
    def getRoutingTable(self):
        return self.routing_table
    
    def compute(self):
        self.pq.put((0, self.node))
        # Djikstra
        while not self.pq.empty():
            # Acquire lock here.
            semaphore[self.node].acquire()
            set_table_node(self.node, self.changed_list)
            
            
            self.changed_list.clear()
            curr = self.pq.get()

            from_node = curr[1]
            dis_node = curr[0]
            for child in adjacency_list[from_node]:
                to = child[0]
                wt = int(child[1])
                if dis_node + wt < self.routing_table[to]:
                    self.routing_table[to] = dis_node + wt
                    self.pq.put((self.routing_table[to], to))
                    self.changed_list.append(to)
        


# For printing the table with '*' added to the changed values
def print_table(node, changed_list):
    num_spaces = 27
    print(f'For the node {node}, the routing table is:')
    print('_'*num_spaces)
    print("{:<1} {:<10} {:<1} {:<10} {:<1}".format('|', 'To_Node','|', 'Distance','|'))
    print('-'*num_spaces)
    
    for key, value in router[node].getRoutingTable().items():
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
            print_table(node, [])
        else:
            print_table(node, changes[node])


changes = dict()

iteration = 1
# A utility function for setting change list for all nodes
# Locks are released here
def set_table_node(node, change_list):
    changes[node] = change_list
    global locked
    locked+=1
    if locked == num_nodes:
        global iteration
        if iteration != 1:
            print("Sleeping for two seconds...\n")
            sleep(2)
        print(f"Iteration number {iteration}")
        iteration+=1
        print_all_tables(changes) 
        changes.clear()
        locked = 0
        for node in node_list:
            semaphore[node].release()

def Main():
    parseInputs()
    for node in node_list:
        router[node] = Router(node)
    
    threads = list()
    for node in node_list:
        thread = Thread(target=router[node].compute)
        threads.append(thread)
    
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    Main()

#This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))