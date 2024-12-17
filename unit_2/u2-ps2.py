"""
Simulation Overview

iRobot is a company (started by MIT alumni and faculty) that sells the Roomba 
vacuuming robot. Roomba robots move around the floor, cleaning the area they 
pass over.

In this problem set, you will code a simulation to compare how much time a 
group of Roomba-like robots will take to clean the floor of a room using two 
different strategies.

The robot starts out at some random position in the room, and with a random 
direction of motion.


Simulation Details

Here are additional details about the simulation model. Read these carefully.

Multiple robots
In general, there are N > 0 robots in the room, where N is given. For 
simplicity, assume that robots are points and can pass through each other or 
occupy the same point without interfering.

The room
The room is rectangular with some integer width w and height h, which are 
given. Initially the entire floor is dirty. A robot cannot pass through 
the walls of the room. A robot may not move to a point outside the room.

Tiles
You will need to keep track of which parts of the floor have been cleaned by 
the robot(s). We will divide the area of the room into 1x1 tiles (there will 
be w * h such tiles). When a robot's location is anywhere in a tile, we will 
consider the entire tile to be cleaned. By convention, we will refer to the 
tiles using ordered pairs of integers: (0, 0), (0, 1), ..., (0, h-1), (1, 0), 
(1, 1), ..., (w-1, h-1).

Robot motion rules
- Each robot has a position inside the room. We'll represent the position 
using coordinates (x, y) which are floats satisfying 0 ≤ x < w and 0 ≤ y < h. 
In our program we'll use instances of the Position class to store these 
coordinates.
- A robot has a direction of motion. We'll represent the direction using an 
integer d satisfying 0 ≤ d < 360, which gives an angle in degrees.
- All robots move at the same speed s, a float, which is given and is constant 
throughout the simulation. Every time-step, a robot moves in its direction of 
motion by s units.
- If a robot detects that it will hit the wall within the time-step, that time 
step is instead spent picking a new direction at random. The robot will 
attempt to move in that direction on the next time step, until it reaches 
another wall.

Termination
The simulation ends when a specified fraction of the tiles in the room have 
been cleaned.
"""


# 6.00.2x Problem Set 2: Simulating robots

import math
import random

import ps2_visualize
# import pylab
import matplotlib.pyplot as plt

##################
## Comment/uncomment the relevant lines, depending on which version of Python you have
##################

# For Python 3.5:
#from ps2_verify_movement35 import testRobotMovement
# If you get a "Bad magic number" ImportError, you are not using Python 3.5 

# For Python 3.6:
#from ps2_verify_movement36 import testRobotMovement
# If you get a "Bad magic number" ImportError, you are not using Python 3.6

# For Python 3.12:
from ps2_verify_movement312 import testRobotMovement
# If you get a "Bad magic number" ImportError, you are not using Python 3.12


# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: number representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        angle = float(angle)
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    def __str__(self):  
        return "(%0.2f, %0.2f)" % (self.x, self.y)


# === Problem 1
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        # raise NotImplementedError
        self.width = width
        self.height = height
        self.clean_tiles = []
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        # raise NotImplementedError
        x = math.floor(Position.getX(pos))
        y = math.floor(Position.getY(pos))
        if (x, y) not in self.clean_tiles:
            self.clean_tiles.append((x, y))

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        # raise NotImplementedError
        if (m, n) in self.clean_tiles:
            return True
        else:
            return False
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        # raise NotImplementedError
        return self.width * self.height

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        # raise NotImplementedError
        return len(self.clean_tiles)

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        # raise NotImplementedError
        x = random.random() * self.width
        y = random.random() * self.height
        return Position(x, y)

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        # raise NotImplementedError
        x = Position.getX(pos)
        y = Position.getY(pos)
        if x < self.width and x >= 0 and y < self.height and y >= 0:
            return True
        else:
            return False


# === Problem 2
class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        # raise NotImplementedError
        self.room = room
        self.speed = speed
        self.position = room.getRandomPosition()
        self.direction = random.randrange(0, 360)
        self.room.cleanTileAtPosition(self.position)

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        # raise NotImplementedError
        return self.position
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        # raise NotImplementedError
        return self.direction

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        # raise NotImplementedError
        self.position = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        # raise NotImplementedError
        self.direction = direction

    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError # don't change this!


# === Problem 3
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead* chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        # raise NotImplementedError
        new_position = self.position.getNewPosition(self.direction, self.speed)
        if self.room.isPositionInRoom(new_position):
            self.setRobotPosition(new_position)
            self.room.cleanTileAtPosition(new_position)
        if not self.room.isPositionInRoom(new_position):
            self.setRobotDirection(random.randrange(0, 360))
            
# Uncomment this line to see your implementation of StandardRobot in action!
# testRobotMovement(StandardRobot, RectangularRoom)


# === Problem 4
def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                RandomWalkRobot)
    """
    # raise NotImplementedError
    total_time_steps = []
    for trial in range(num_trials):
        # anim = ps2_visualize.RobotVisualization(num_robots, width, height)
        # anim = ps2_visualize.RobotVisualization(num_robots, width, height, delay = 0.2)
        robots = []
        time_steps = 0
        room = RectangularRoom(width, height)
        for robot in range(num_robots):
            robots.append(robot_type(room, speed))
        while room.getNumCleanedTiles() / room.getNumTiles() < min_coverage: 
            for robot in robots:
                robot.updatePositionAndClean()
            time_steps += 1
            # anim.update(room, robots)
        total_time_steps.append(time_steps)
    # anim.done()
    avg_time_steps = sum(total_time_steps) / len(total_time_steps)
    return avg_time_steps

# Uncomment this line to see how much your simulation takes on average
# print(runSimulation(1, 1.0, 10, 10, 0.75, 30, StandardRobot))
# print(runSimulation(1, 0.5, 10, 10, 0.75, 30, StandardRobot))
# print(runSimulation(1, 2.0, 10, 10, 0.75, 30, StandardRobot))
# print(runSimulation(1, 3.5, 10, 10, 0.75, 30, StandardRobot))
# print(runSimulation(1, 1.0, 5, 5, 1, 30, StandardRobot))
# print(runSimulation(1, 1.0, 10, 10, 0.9, 30, StandardRobot))
# print(runSimulation(1, 1.0, 20, 20, 1, 30, StandardRobot))
# print(runSimulation(3, 1.0, 20, 20, 1, 30, StandardRobot))


# === Problem 5
class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random at the end of each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        # raise NotImplementedError
        new_position = self.position.getNewPosition(self.direction, self.speed)
        if self.room.isPositionInRoom(new_position):
            self.setRobotPosition(new_position)
            self.room.cleanTileAtPosition(new_position)
        self.setRobotDirection(random.randrange(0, 360))
            
# Uncomment this line to see your implementation of RandomWalkRobot in action!
# testRobotMovement(RandomWalkRobot, RectangularRoom)
            
# Uncomment this line to see how much your simulation takes on average
# print(runSimulation(1, 1.0, 10, 10, 0.75, 30, RandomWalkRobot))
# print(runSimulation(1, 0.5, 10, 10, 0.75, 30, RandomWalkRobot))
# print(runSimulation(1, 2.0, 10, 10, 0.75, 30, RandomWalkRobot))
# print(runSimulation(1, 3.5, 10, 10, 0.75, 30, RandomWalkRobot))
# print(runSimulation(1, 1.0, 5, 5, 1, 30, RandomWalkRobot))
# print(runSimulation(1, 1.0, 10, 10, 0.9, 30, RandomWalkRobot))
# print(runSimulation(1, 1.0, 20, 20, 1, 30, RandomWalkRobot))
# print(runSimulation(3, 1.0, 20, 20, 1, 30, RandomWalkRobot))


def showPlot1(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        print("Plotting", num_robots, "robots...")
        times1.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, StandardRobot))
        times2.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, RandomWalkRobot))
    # pylab.plot(num_robot_range, times1)
    # pylab.plot(num_robot_range, times2)
    # pylab.title(title)
    # pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    # pylab.xlabel(x_label)
    # pylab.ylabel(y_label)
    # pylab.show()
    plt.plot(num_robot_range, times1)
    plt.plot(num_robot_range, times2)
    plt.title(title)
    plt.legend(('StandardRobot', 'RandomWalkRobot'))
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()

    
def showPlot2(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = 300//width
        print("Plotting cleaning time for a room of width:", width, "by height:", height)
        aspect_ratios.append(float(width) / height)
        times1.append(runSimulation(2, 1.0, width, height, 0.8, 200, StandardRobot))
        times2.append(runSimulation(2, 1.0, width, height, 0.8, 200, RandomWalkRobot))
    # pylab.plot(aspect_ratios, times1)
    # pylab.plot(aspect_ratios, times2)
    # pylab.title(title)
    # pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    # pylab.xlabel(x_label)
    # pylab.ylabel(y_label)
    # pylab.show()
    plt.plot(aspect_ratios, times1)
    plt.plot(aspect_ratios, times2)
    plt.title(title)
    plt.legend(('StandardRobot', 'RandomWalkRobot'))
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()
    

# === Problem 6
# NOTE: If you are running the simulation, you will have to close it 
# before the plot will show up.

#
# 1) Write a function call to showPlot1 that generates an appropriately-labeled
#     plot.
#
#       (... your call here ...)
#
showPlot1("Time It Takes 1 - 10 Robots To Clean 80% Of A Room", "Number of Robots", "Time-steps")

#
# 2) Write a function call to showPlot2 that generates an appropriately-labeled
#     plot.
#
#       (... your call here ...)
#
showPlot2("Time It Takes Two Robots To Clean 80% Of Variously Shaped Rooms", "Aspect Ratio", "Time-steps")