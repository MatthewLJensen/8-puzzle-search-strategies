
import random
import time
from queue import PriorityQueue

#GLOBAL VARIABLES

goal = "12345678-"
randomize_iterations = 100
test_iterations = 10

class Node:
    def __init__(self, instance, parent, h, g):
        self.instance = instance
        self.parent = parent
        self.h = h
        self.g = g

    def __gt__(self, other):
        return (self.h + self.g) > (other.h + other.g)
    def __lt__(self, other):
        return (self.h + self.g) < (other.h + other.g)
    def __eq__(self, other):
        return (self.h + self.g) == (other.h + other.g)
    def __repr__(self):
        return repr("Instance: " + str(self.instance) + ", G: " + str(self.g) + ", H: " + str(self.h))

    def find_neighbors(self):
        neighbors = []
        position = self.instance.index('-')

        if position <= 5: #Checks if the dash can move down
            #print("moving down")
            neighbors.append(self.instance[:position] + self.instance[position + 3] + self.instance[position + 1:position + 3] + "-" + self.instance[position + 4:])

        if position >= 3: #Checks if the dash can move up
            #print("moving up")
            neighbors.append(self.instance[:position-3] + "-" + self.instance[position - 2:position] + self.instance[position-3] + self.instance[position + 1:])

        if (position%3 < 2): #Checks if the dash can move right
            #print("moving right")
            neighbors.append(self.instance[:position] + self.instance[position + 1] + "-" + self.instance[position+2:])
        
        if (position%3 > 0): #Checks if the dash can move left
            #print("moving left")
            neighbors.append(self.instance[:position - 1] + "-" + self.instance[position - 1] + self.instance[position + 1:])

        return neighbors

    def print_path(self):
        current = self
        path = []
        while (current):
            path.insert(0,current.parent)
            current = current.parent
        for node in path:
            print(repr(node))

    def path_length(self):
        current = self
        length = 0
        while (current):
            length += 1
            current = current.parent
        return length

#HELPER FUNCTIONS



def find_row(instance, tile): # returns the row number of a tile
    position = instance.index(tile)
    if position < 3:
        return 0
    elif position < 6:
        return 1
    else:
        return 2

def find_column(instance, tile): # returns the column number of a tile
    position = instance.index(tile)
    return (position%3)

def sort_val(e):
    return e[-1][0]

def randomize(): # creates a random 8-puzzle configuration by moving tiles randomly 100 times.
    iterations = randomize_iterations
    instance = Node(goal, None, 0, 0)
    while iterations:
        instance.instance = random.choice(instance.find_neighbors())
        iterations = iterations - 1
    return instance

# HEURISTIC FUNCTIONS

def manhattan_distance(instance): # returns the combined distance that each tile must move to reach the goal-state. Does this by comparing the row and column of a tile and the row and column of the goal state for that tile.
    distance = 0
    for tile in instance:
        if tile != "-":
            distance += (abs(find_column(instance, tile) - find_column(goal, tile)) + abs(find_row(instance, tile) - find_row(goal, tile)))
    return distance




def num_displaced(instance): # returns the number of tiles that are not in the correct goal-state location
    displaced_tiles = 0
    for tile in range (1,9):
        if (instance.index(str(tile)) != goal.index(str(tile))):
            displaced_tiles += 1
    return displaced_tiles



#SEARCH FUNCTIONS

def breadth_first_search(initial_instance):
    visited = []
    queue = []
    visited.append(initial_instance.instance)
    queue.append(initial_instance)

    while queue:
        node = queue.pop(0)
        if node.instance == goal:
            return (node, len(visited))
        for neighbor in node.find_neighbors():
            if neighbor not in visited:
                new_node = Node(neighbor, node, 0, 0)
                visited.append(neighbor)
                queue.append(new_node)
    return -1



def best_first_search(initial_instance, heuristic):
    visited = []
    queue = PriorityQueue()
    initial_instance.h = heuristic(initial_instance.instance)
    visited.append(initial_instance.instance)
    queue.put(initial_instance)
    while queue:
        node = queue.get()
        if node.instance == goal:
            return (node, len(visited))
        for neighbor in node.find_neighbors():
            if neighbor not in visited:
                new_node = Node(neighbor, node, heuristic(neighbor), 0)
                visited.append(neighbor)
                queue.put(new_node)
    return -1


def a_star_search(initial_instance, heuristic):
    visited = []
    queue = PriorityQueue()
    initial_instance.h = heuristic(initial_instance.instance)
    visited.append(initial_instance.instance)
    queue.put(initial_instance)
    while queue:
        node = queue.get()
        if node.instance == goal:
            return (node, len(visited))
        for neighbor in node.find_neighbors():
            if neighbor not in visited:
                new_node = Node(neighbor, node, heuristic(neighbor), node.g + 1)
                visited.append(neighbor)
                queue.put(new_node)
    return -1



# RANK FUNCTIONS
def rank():
    tests_completed = 0

    # (avg visited nodes, avg num steps in solution, avg time)
    breadth_first_results = [0, 0, 0]
    greedy_best_first_num_displaced_results = [0, 0, 0]
    greedy_best_first_manhattan_distance_results = [0, 0, 0]
    a_star_num_displaced_results = [0, 0, 0]
    a_star_manhattan_distance_results = [0, 0, 0]
    print("Comparing search algorithms. Beginning: \n")
    while tests_completed < test_iterations:
        test_board = randomize()
        print("Running test " + str(tests_completed + 1) + " of " + str(test_iterations) + ". Random puzzle state: " + test_board)

        print("Starting Breadth First Search")
        start = time.time()
        results = breadth_first_search(test_board)
        end = time.time()

        breadth_first_results[0] += results[1]
        breadth_first_results[1] += len(results[0])
        breadth_first_results[2] += (end - start)

        print("Starting Greedy Best First Search with \'Number of Tiles Out of Place\' heuristic")
        start = time.time()
        results = best_first_search(test_board, num_displaced)
        end = time.time()

        greedy_best_first_num_displaced_results[0] += results[1]
        greedy_best_first_num_displaced_results[1] += len(results[0])
        greedy_best_first_num_displaced_results[2] += (end - start)

        print("Starting Greedy Best First Search with \'Manhattan Distance\' heuristic")
        start = time.time()
        results = best_first_search(test_board, manhattan_distance)
        end = time.time()

        greedy_best_first_manhattan_distance_results[0] += results[1]
        greedy_best_first_manhattan_distance_results[1] += len(results[0])
        greedy_best_first_manhattan_distance_results[2] += (end - start)

        print("Starting A-Star Search with \'Number of Tiles Out of Place\' heuristic")
        start = time.time()
        results = a_star_search(test_board, num_displaced)
        end = time.time()

        a_star_num_displaced_results[0] += results[1]
        a_star_num_displaced_results[1] += len(results[0])
        a_star_num_displaced_results[2] += (end - start)

        print("Starting A-Star Search with \'Manhattan Distance\' heuristic")
        start = time.time()
        results = a_star_search(test_board, manhattan_distance)
        end = time.time()

        a_star_manhattan_distance_results[0] += results[1]
        a_star_manhattan_distance_results[1] += len(results[0])
        a_star_manhattan_distance_results[2] += (end - start)


        tests_completed+=1
    
    #loop through and divide by total test count
    for i in range(len(breadth_first_results)):
        breadth_first_results[i] = (breadth_first_results[i]/test_iterations)
        greedy_best_first_num_displaced_results[i] = (greedy_best_first_num_displaced_results[i]/test_iterations)
        greedy_best_first_manhattan_distance_results[i] = (greedy_best_first_manhattan_distance_results[i]/test_iterations)
        a_star_num_displaced_results[i] = (a_star_num_displaced_results[i]/test_iterations)
        a_star_manhattan_distance_results[i] = (a_star_manhattan_distance_results[i]/test_iterations)

    print("---------------RESULTS---------------\n\n")

    print("(Average number of visited nodes, average number of steps in solution, average time)\n")
    print("\nBreadth first search")
    print(breadth_first_results)
    print("\nGreedy Best with \'Number of Tiles Displaced\' heuristic")
    print(greedy_best_first_num_displaced_results)
    print("\nGreedy Best with \'Manhattan Distance\' heuristic")
    print(greedy_best_first_manhattan_distance_results)
    print("\nA Star with \'Number of Tiles Displaced\' heuristic")
    print(a_star_num_displaced_results)
    print("\nA Star with \'Manhattan Distance\' heuristic")
    print(a_star_manhattan_distance_results)


# RANK SEARCH ALGOS
#rank()


# TEST HEURISTICS
# print(manhattan_distance("12345678-"))
# print(manhattan_distance("1234567-8"))
# print(manhattan_distance("21345678-"))
# print(num_displaced("7145-6832"))

# GENERATE RANDOM BOARD
#print(randomize())


#instance = Node("1638-7245", None, 0, 0)
instance = randomize()

astar = a_star_search(instance, manhattan_distance)
print("        Num Visited   Solution Length     ")
print("A*        " + str(astar[1])   + "               " + str(astar[0].path_length()))

gbfs  = best_first_search(instance, manhattan_distance)
print()
print("GBFS      " + str(gbfs[1])    + "               " + str(gbfs[0].path_length()))

breadth = breadth_first_search(instance)
print()
print("Breadth   " + str(breadth[1]) + "             "   + str(breadth[0].path_length()))
