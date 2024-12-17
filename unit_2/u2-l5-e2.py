"""
How would you randomly generate an even number x, 0 <= x < 100? Fill out the 
definition for the function genEven(). Please generate a uniform distribution 
over the even numbers between 0 and 100 (not including 100).
"""


import random
def genEven():
    '''
    Returns a random even number x, where 0 <= x < 100
    '''
    # Your code here
    return random.randrange(0, 100, 2)
