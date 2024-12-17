"""
Write a generator that returns every arrangement of items such that each is in 
one or none of two different bags. Each combination should be given as a tuple 
of two lists, the first being the items in bag1, and the second being the 
items in bag2.
"""


import random

def yieldAllCombos(items):
    """
        Generates all combinations of N items into two bags, whereby each 
        item is in one or zero bags.

        Yields a tuple, (bag1, bag2), where each bag is represented as a list 
        of which item(s) are in each bag.
    """
    # Your code here
    N = len(items)
    # enumerate the 3**N possible combinations
    for i in range(3**N):
        bag1 = []
        bag2 = []
        for j in range(N):
            if (i // (3**j)) % 3 == 1:
                bag1.append(items[j])
            elif (i // (3**j)) % 3 == 2:
                bag2.append(items[j])
        yield (bag1, bag2)
        

# Test        
        
class Item(object):
    def __init__(self, n, v, w):
        self.name = n
        self.value = float(v)
        self.weight = float(w)
    def getName(self):
        return self.name
    def getValue(self):
        return self.value
    def getWeight(self):
        return self.weight
    def __str__(self):
        return '<' + self.name + ', ' + str(self.value) + ', '\
                     + str(self.weight) + '>'
                     
def buildItems():
    return [Item(n,v,w) for n,v,w in (('clock', 175, 10),
                                      ('painting', 90, 9),
                                      ('radio', 20, 4),
                                      ('vase', 50, 2),
                                      ('book', 10, 1),
                                      ('computer', 200, 20))]

def buildRandomItems(n):
    return [Item(str(i),10*random.randint(1,10),random.randint(1,10))
            for i in range(n)]


# See output

items = buildItems()
combos = yieldAllCombos(items)
for c in combos:
    bag1 = [str(item) for item in c[0]]
    bag2 = [str(item) for item in c[1]]
    print(f"({bag1}, {bag2})")
    
print("-----")

items = buildRandomItems(1)
combos = yieldAllCombos(items)
for c in combos:
    bag1 = [str(item) for item in c[0]]
    bag2 = [str(item) for item in c[1]]
    print(f"({bag1}, {bag2})")
