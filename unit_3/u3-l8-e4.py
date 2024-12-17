"""
You have a bucket with 3 red balls and 3 green balls. Assume that once you 
draw a ball out of the bucket, you don't replace it. What is the probability 
of drawing 3 balls of the same color?

Write a Monte Carlo simulation to solve the above problem. Feel free to write 
a helper function if you wish.
"""


import random

def noReplacementSimulation(numTrials):
    '''
    Runs numTrials trials of a Monte Carlo simulation
    of drawing 3 balls out of a bucket containing
    3 red and 3 green balls. Balls are not replaced once
    drawn. Returns the a decimal - the fraction of times 3 
    balls of the same color were drawn.
    '''
    # Your code here
    num_successes = 0
    for trial in range(numTrials):
        choices = 3 * ["red", "green"]
        chosen = []
        for draw in range(3):
            ball = random.choice(choices)
            chosen.append(ball)
            choices.remove(ball)
        if chosen == 3 * ["red"] or chosen == 3 * ["green"]:
            num_successes += 1
    return num_successes / numTrials


# Test
print(noReplacementSimulation(100))
