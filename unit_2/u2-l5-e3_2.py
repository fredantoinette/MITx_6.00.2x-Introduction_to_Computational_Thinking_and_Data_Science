"""
Write a uniformly distributed stochastic program, stochasticNumber, that 
returns an even number between 9 and 21.
"""


import random
def stochasticNumber():
    '''
    Stochastically generates and returns a uniformly distributed even number between 9 and 21
    '''
    # Your code here
    return random.randrange(10, 21, 2)
