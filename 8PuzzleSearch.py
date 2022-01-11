
import random
import time
from queue import PriorityQueue

#GLOBAL VARIABLES

goal = "12345678-"              # The goal state
randomize_iterations = 1000     # How many iterations the randomize function should perform on the goal state
test_iterations = 100           # How many iterations the rank function should perform when comparing search strategies

class Node: # The only class in this program. Holds information on a node, or instance, of an 8-puzzle state.
    def __init__(self, instance, parent, h, g):
        self.instance = instance
        self.parent = parent
        self.h = h
        self.g = g

    def __gt__(self, other):
        if (self.h + self.g) == (other.h + other.g):
            return self.g > other.g # If they tie, prioritize the g score, rather than assuming they are equal
        return (self.h + self.g) > (other.h + other.g)

    def __lt__(self, other):
        if (self.h + self.g) == (other.h + other.g):
            return self.g < other.g # If they tie, prioritize the g score, rather than assuming they are equal
        return (self.h + self.g) < (other.h + other.g)

    def __eq__(self, other):
        return (self.h == other.h) and (self.g == other.g) # They are only equal if both Gs are equal and both Hs

    def __repr__(self):
        return repr("Instance: " + str(self.instance) + ", G: " + str(self.g) + ", H: " + str(self.h))

    def find_neighbors(self): # Finds the neighbors of an instance. This function could be cleaned up to use the find_row() and find_column helper functions. Currently a little messy.
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

    def print_path(self, pretty: bool = False): # Prints the path from a node back to it's initial parent. If you use this on the output of one of the search strategies, it will print the solution path.
        current = self
        path = []
        while (current):
            path.insert(0,current)
            current = current.parent
        for node in path:
            if pretty:
                node.print_pretty()
                print()
            else:
                print(repr(node))

    def path_length(self): # Prints the number of steps back to the original parent node. If you use this on the output of one of the search strategies, it will print the solution length.
        current = self
        length = 0
        while (current):
            length += 1
            current = current.parent
        return length

    def print_pretty(self):
        index = 0
        for char in self.instance:
            print(char, end=" ")
            index += 1
            if (index%3) == 0:
                print()


#HELPER FUNCTIONS

def find_row(instance, tile): # returns the row number of a tile within a specific instance. Doesn't currently take a node object, but rather a node.instance
    position = instance.index(tile)
    if position < 3:
        return 0
    elif position < 6:
        return 1
    else:
        return 2

def find_column(instance, tile): # returns the column number of a tile within a specific instance. Doesn't currently take a node object, but rather a node.instance
    position = instance.index(tile)
    return (position%3)

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

def num_displaced(instance):      # returns the number of tiles that are not in the correct goal-state location
    displaced_tiles = 0
    for tile in range (1,9):
        if (instance.index(str(tile)) != goal.index(str(tile))):
            displaced_tiles += 1
    return displaced_tiles

#SEARCH FUNCTIONS

def breadth_first_search(initial_instance):
    visited = set()
    queue = []
    visited.add(initial_instance.instance)
    queue.append(initial_instance)
    while queue:
        node = queue.pop(0)
        if node.instance == goal:
            return (node, len(visited))
        for neighbor in node.find_neighbors():
            if neighbor not in visited:
                new_node = Node(neighbor, node, manhattan_distance(neighbor), node.g + 1) #while this does input heuristic values, breadth first search does not utilize them
                visited.add(neighbor)
                queue.append(new_node)
    return -1


def best_first_search(initial_instance, heuristic):
    visited = set()
    queue = PriorityQueue()
    initial_instance.h = heuristic(initial_instance.instance)
    visited.add(initial_instance.instance)
    queue.put(initial_instance)
    while queue:
        node = queue.get()
        if node.instance == goal:
            return (node, len(visited))
        for neighbor in node.find_neighbors():
            if neighbor not in visited:
                new_node = Node(neighbor, node, heuristic(neighbor), 0)
                visited.add(neighbor)
                queue.put(new_node)
    return -1


def a_star_search(initial_instance, heuristic):
    visited = set()
    queue = PriorityQueue()
    initial_instance.h = heuristic(initial_instance.instance)
    visited.add(initial_instance.instance)
    queue.put(initial_instance)
    while queue:
        node = queue.get()
        if node.instance == goal:
            return (node, len(visited))
        for neighbor in node.find_neighbors():
            if neighbor not in visited:
                new_node = Node(neighbor, node, heuristic(neighbor), node.g + 1)
                visited.add(neighbor)
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
        print("Running test " + str(tests_completed + 1) + " of " + str(test_iterations) + ". Random puzzle state: " + str(test_board))

        print("Starting Breadth First Search")
        start = time.time()
        results = breadth_first_search(test_board)
        end = time.time()

        breadth_first_results[0] += results[1]
        breadth_first_results[1] += results[0].path_length()
        breadth_first_results[2] += (end - start)

        print("Starting Greedy Best First Search with \'Number of Tiles Out of Place\' heuristic")
        start = time.time()
        results = best_first_search(test_board, num_displaced)
        end = time.time()

        greedy_best_first_num_displaced_results[0] += results[1]
        greedy_best_first_num_displaced_results[1] += results[0].path_length()
        greedy_best_first_num_displaced_results[2] += (end - start)

        print("Starting Greedy Best First Search with \'Manhattan Distance\' heuristic")
        start = time.time()
        results = best_first_search(test_board, manhattan_distance)
        end = time.time()

        greedy_best_first_manhattan_distance_results[0] += results[1]
        greedy_best_first_manhattan_distance_results[1] += results[0].path_length()
        greedy_best_first_manhattan_distance_results[2] += (end - start)

        print("Starting A-Star Search with \'Number of Tiles Out of Place\' heuristic")
        start = time.time()
        results = a_star_search(test_board, num_displaced)
        end = time.time()

        a_star_num_displaced_results[0] += results[1]
        a_star_num_displaced_results[1] += results[0].path_length()
        a_star_num_displaced_results[2] += (end - start)

        print("Starting A-Star Search with \'Manhattan Distance\' heuristic")
        start = time.time()
        results = a_star_search(test_board, manhattan_distance)
        end = time.time()

        a_star_manhattan_distance_results[0] += results[1]
        a_star_manhattan_distance_results[1] += results[0].path_length()
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

def compare():
    instance = randomize()
    print("________________________________________________________________")
    print(instance)
    print()

    astar = a_star_search(instance, manhattan_distance)
    print("         Num Visited   Solution Length     ")
    print("A*         " + str(astar[1])   + " " * (18 - len(str(astar[1]))) + str(astar[0].path_length()))

    astar = a_star_search(instance, num_displaced)
    print()
    print("a* ndh     " + str(astar[1])   + " " * (18 - len(str(astar[1]))) + str(astar[0].path_length()))

    gbfs  = best_first_search(instance, manhattan_distance)
    print()
    print("gbfs       " + str(gbfs[1])    + " " * (18 - len(str(gbfs[1]))) + str(gbfs[0].path_length()))

    gbfs  = best_first_search(instance, manhattan_distance)
    print()
    print("gbfs ndh   " + str(gbfs[1])    + " " * (18 - len(str(gbfs[1]))) + str(gbfs[0].path_length()))

    breadth = breadth_first_search(instance)
    print()
    print("Breadth    " + str(breadth[1]) + " " * (18 - len(str(breadth[1])))   + str(breadth[0].path_length()))



# Compare the strategies with these functions
#rank()
#compare()


test = randomize()
a_star_search(test, manhattan_distance)[0].print_path(True)
#compare()



# OTHER TESTS
# Searchs for a sitation where A* produces a result with a longer path length than breadth first search. This shouldn't happen, but I used this to find situations where it was an fix them.
# keep_going = True
# alength = 0
# blength = 0
# lowest = ("12345678-", 25)
# while keep_going:
#     instance = randomize()
#     breadth = breadth_first_search(instance)
#     astar = a_star_search(instance, manhattan_distance)
#     if (breadth[0].path_length() != astar[0].path_length()):
#         print(instance)
#         if (astar[0].path_length() < lowest[1]):
#             lowest = (instance, astar[0].path_length())
#             print(lowest)
