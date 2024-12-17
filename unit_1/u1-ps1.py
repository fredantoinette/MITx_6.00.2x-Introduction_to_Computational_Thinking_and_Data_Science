"""
Space Cows Introduction

A colony of Aucks (super-intelligent alien bioengineers) has landed on Earth 
and has created new species of farm animals! The Aucks are performing their 
experiments on Earth, and plan on transporting the mutant animals back to 
their home planet of Aurock. In this problem set, you will implement 
algorithms to figure out how the aliens should shuttle their experimental 
animals back across space.


Transporting Cows Across Space!

The aliens have succeeded in breeding cows that jump over the moon! Now they 
want to take home their mutant cows. The aliens want to take all chosen cows 
back, but their spaceship has a weight limit and they want to minimize the 
number of trips they have to take across the universe. Somehow, the aliens 
have developed breeding technology to make cows with only integer weights.

The data for the cows to be transported is stored in ps1_cow_data.txt. All of 
your code for Part A should go into ps1.py.

First we need to load the cow data from the data file ps1_cow_data.txt, this 
has already been done for you and should let you begin working on the rest of 
this problem. If you are having issues getting the ps1_cow_data.txt to load, 
be sure that you have it in the same folder as the ps1.py that you are running.

You can expect the data to be formatted in pairs of x,y on each line, where x 
is the name of the cow and y is a number indicating how much the cow weighs in 
tons, and that all of the cows have unique names. Here are the first few lines 
of ps1_cow_data.txt:

Maggie,3
Herman,7
Betsy,9
...
"""


###########################
# 6.00.2x Problem Set 1: Space Cows 

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """

    cow_dict = dict()

    f = open(filename, 'r')
    
    for line in f:
        line_data = line.split(',')
        cow_dict[line_data[0]] = int(line_data[1])
    return cow_dict


from collections import OrderedDict

# Problem 1
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    # pass
    # cows_copy = dict(sorted(cows.items(), key = lambda item: item[1], reverse = True))
    cows_copy = OrderedDict(sorted(cows.items(), key = lambda item: item[1], reverse = True))
    all_trips = []
    one_trip = []
    total_weight = 0
    overweight_cows_names = []
    chosen_cows_names = []
    for name, weight in cows_copy.items():
        if weight > limit:
            overweight_cows_names.append(name)
    for name in overweight_cows_names:
        del cows_copy[name]
    while len(cows_copy) > 0:
        for name, weight in cows_copy.items():
            if total_weight + weight <= limit:
                one_trip.append(name)
                total_weight += weight
                chosen_cows_names.append(name)
        for name in chosen_cows_names:
            del cows_copy[name]
        all_trips.append(one_trip)
        one_trip = []
        chosen_cows_names = []
        total_weight = 0
    return all_trips
        

# Problem 2
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    # pass
    best_trips = None
    min_num_trips = 0
    for partition in get_partitions(cows):
        is_overweight = False
        for trip in partition:
            partition_weight = 0
            for name in trip:
                partition_weight += cows[name]
            if partition_weight > limit:
                is_overweight = True
                break
        if is_overweight == False and (min_num_trips == 0 or len(partition) < min_num_trips):
            best_trips = partition
            min_num_trips = len(partition)
    return best_trips
               
        
# Problem 3
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # TODO: Your code here
    # pass
    print("Greedy")
    start = time.time()
    g = greedy_cow_transport(cows)
    end = time.time()
    print("Trips:", g)
    print("Number of trips:", len(g))
    print("Run-time (second):", end - start)
    print("-----")
    print("Brute Force")
    start = time.time()
    bf = brute_force_cow_transport(cows)
    end = time.time()
    print("Trips:", bf)
    print("Number of trips:", len(bf))
    print("Run-time (second):", end - start)
     
    
"""
Here is some test data for you to see the results of your algorithms with. 
Do not submit this along with any of your answers. Uncomment the last two
lines to print the result of your problem.
"""

cows = load_cows("ps1_cow_data.txt")
limit=100
print(cows)
print("-----")

print(greedy_cow_transport(cows, limit))
print(brute_force_cow_transport(cows, limit))
print("-----")

# Test Greedy
print(greedy_cow_transport({'Polaris': 20, 'Milkshake': 75, 'Louis': 45, 'Horns': 50, 'MooMoo': 85, 'Miss Bella': 15, 'Muscles': 65, 'Lotus': 10, 'Patches': 60, 'Clover': 5}, 100))
print(greedy_cow_transport({'Daisy': 50, 'Coco': 10, 'Lilly': 24, 'Dottie': 85, 'Willow': 35, 'Abby': 38, 'Rose': 50, 'Patches': 12, 'Betsy': 65, 'Buttercup': 72}, 100))
print(greedy_cow_transport({'Coco': 59, 'Rose': 42, 'Willow': 59, 'Abby': 28, 'Starlight': 54, 'Luna': 41, 'Betsy': 39, 'Buttercup': 11}, 120))
print("-----")

# Test Brute Force
print(brute_force_cow_transport({'Horns': 25, 'Miss Bella': 25, 'MooMoo': 50, 'Lotus': 40, 'Milkshake': 40, 'Boo': 20}, 100))
print(brute_force_cow_transport({'Betsy': 65, 'Buttercup': 72, 'Daisy': 50}, 75))
print(brute_force_cow_transport({'Betsy': 39, 'Starlight': 54, 'Luna': 41, 'Buttercup': 11}, 145))
print("-----")

compare_cow_transport_algorithms()