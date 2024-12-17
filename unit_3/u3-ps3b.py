"""
Introduction

In this problem set, you will design and implement a stochastic simulation of 
patient and virus population dynamics, and reach conclusions about treatment 
regimens based on the simulation results.


Background: Viruses, Drug Treatments, and Computational Models

Viruses such as HIV and H1N1 represent a significant challenge to modern 
medicine. One of the reasons that they are so difficult to treat is their 
ability to evolve.

As you may know from introductory biology classes, the traits of an organism 
are determined by its genetic code. When organisms reproduce, their offspring 
will inherit genetic information from their parent. This genetic information 
will be modified, either because of mixing of the two parents' genetic 
information, or through mutations in the genome replication process, thus 
introducing diversity into a population.

Viruses are no exception. Two characteristics of viruses make them particularly 
difficult to treat. The first is that their replication mechanism often lacks 
the error checking mechanisms that are present in more complex organisms. This 
speeds up the rate of mutation. Secondly, viruses replicate extremely quickly 
(orders of magnitude faster than humans) -- thus, while we may be used to 
thinking of evolution as a process which occurs over long time scales, 
populations of viruses can undergo substantial evolutionary changes within a 
single patient over the course of treatment.

These two characteristics allow a virus population to acquire genetic 
resistance to therapy quickly. In this problem set, we will make use of 
simulations to explore the effect of introducing drugs on the virus population 
and determine how best to address these treatment challenges within a 
simplified model.

Computational modeling has played an important role in the study of viruses 
such as HIV (for example, see this paper, by MIT graduate David Ho). In this 
problem, we will implement a highly simplified stochastic model of virus 
population dynamics. Many details have been swept under the rug (host cells are 
not explicitly modeled and the size of the population is several orders of 
magnitude less than the size of actual virus populations). Nevertheless, our 
model exhibits biologically relevant characteristics and will give you a chance 
to analyze and interpret interesting simulation data.

Spread of a Virus in a Person

In reality, diseases are caused by viruses and have to be treated with 
medicine, so in the remainder of this problem set, we'll be looking at a 
detailed simulation of the spread of a virus within a person.
"""


# Problem Set 3: Simulating the Spread of Disease and Virus Population Dynamics 

import random
import pylab
import matplotlib.pyplot as plt

''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''


#
# PROBLEM 1
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """
        # TODO
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def getMaxBirthProb(self):
        """
        Returns the max birth probability.
        """
        # TODO
        return self.maxBirthProb

    def getClearProb(self):
        """
        Returns the clear probability.
        """
        # TODO
        return self.clearProb

    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.getClearProb and otherwise returns
        False.
        """
        # TODO
        if self.getClearProb() > random.random():
            return True
        else:
            return False

    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """
        # TODO
        if self.getMaxBirthProb() * (1 - popDensity) > random.random():
            return SimpleVirus(self.getMaxBirthProb(), self.getClearProb())
        else:
            raise NoChildException
            

class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the maximum virus population for this patient (an integer)
        """
        # TODO
        self.viruses = viruses
        self.maxPop = maxPop

    def getViruses(self):
        """
        Returns the viruses in this Patient.
        """
        # TODO
        return self.viruses

    def getMaxPop(self):
        """
        Returns the max population.
        """
        # TODO
        return self.maxPop

    def getTotalPop(self):
        """
        Gets the size of the current total virus population. 
        returns: The total virus population (an integer)
        """
        # TODO
        return len(self.getViruses())


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        
        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """
        # TODO
        temp_viruses = self.getViruses().copy()
        for virus in temp_viruses:
            if virus.doesClear():
                self.viruses.remove(virus)
            popDensity = len(self.viruses) / self.getMaxPop()
            if 0.0 < popDensity < 1.0:
                try:
                    offspring = virus.reproduce(popDensity)
                    self.viruses.append(offspring)
                except NoChildException:
                    pass
        return len(self.viruses)


#
# PROBLEM 2
#
def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).    
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """
    # TODO
    avg_pop = 300 * [0]
    for trial in range(numTrials):
        viruses = []
        for virus in range(numViruses):
            viruses.append(SimpleVirus(maxBirthProb, clearProb))
        p = Patient(viruses, maxPop)
        for time_step in range(300):
            p.update()
            avg_pop[time_step] += p.getTotalPop()
    avg_pop[:] = [e / numTrials for e in avg_pop]
    # pylab.plot(avg_pop, label = "SimpleVirus")
    # pylab.title("SimpleVirus simulation")
    # pylab.xlabel("Time Steps")
    # pylab.ylabel("Average Virus Population")
    # pylab.legend(loc = "best")
    # pylab.show()
    # print(avg_pop)
    plt.plot(avg_pop, label = "SimpleVirus")
    plt.title("SimpleVirus simulation")
    plt.xlabel("Time Steps")
    plt.ylabel("Average Virus Population")
    plt.legend(loc = "best")
    plt.show()

# from ps3b_precompiled_312 import *
# Test
simulationWithoutDrug(100, 1000, 0.1, 0.05, 100)
# simulationWithoutDrug(100, 1000, 0.3, 0.05, 100)
# simulationWithoutDrug(100, 1000, 0.5, 0.05, 100)
# simulationWithoutDrug(100, 1000, 0.7, 0.05, 100)
# simulationWithoutDrug(100, 1000, 0.99, 0.05, 100)
# simulationWithoutDrug(100, 1000, 0.1, 0.99, 100)
# simulationWithoutDrug(1, 10, 1.0, 0.0, 1)
# simulationWithoutDrug(100, 200, 0.2, 0.8, 1)
# simulationWithoutDrug(1, 90, 0.8, 0.1, 1)


#
# PROBLEM 3
#
class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """   

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)       

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """
        # TODO
        # super().__init__(maxBirthProb, clearProb)
        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.resistances = resistances
        self.mutProb = mutProb

    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        # TODO
        return self.resistances

    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        # TODO
        return self.mutProb

    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.       

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        # TODO
        if drug in self.getResistances():
            return self.getResistances()[drug]
        else:
            return False

    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A virus particle will only reproduce if it is resistant to ALL the drugs
        in the activeDrugs list. For example, if there are 2 drugs in the
        activeDrugs list, and the virus particle is resistant to 1 or no drugs,
        then it will NOT reproduce.

        Hence, if the virus is resistant to all drugs
        in activeDrugs, then the virus reproduces with probability:      

        self.maxBirthProb * (1 - popDensity).                       

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). The offspring virus
        will have the same maxBirthProb, clearProb, and mutProb as the parent.

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.       

        For example, if a virus particle is resistant to guttagonol but not
        srinol, and self.mutProb is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        srinol and a 90% chance that the offspring will not be resistant to
        srinol.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population       

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """
        # TODO
        count = 0
        for drug in activeDrugs:
            if self.isResistantTo(drug) == False:
                break
            else:
                count += 1
        if count == len(activeDrugs):
            if self.getMaxBirthProb() * (1 - popDensity) > random.random():
                offspring_resistances = self.getResistances().copy()
                for resistance in offspring_resistances:
                    if self.getMutProb() > random.random(): 
                        offspring_resistances[resistance] = not self.getResistances()[resistance]
                return ResistantVirus(self.getMaxBirthProb(), self.getClearProb(), offspring_resistances, self.getMutProb())
            else:
                raise NoChildException
        else:
            raise NoChildException

            
#
# PROBLEM 4
#
class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).              

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """
        # TODO
        # super().__init__(viruses, maxPop)
        Patient.__init__(self, viruses, maxPop)
        self.postcondition = []

    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """
        # TODO
        if newDrug not in self.postcondition:
            self.postcondition.append(newDrug)

    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """
        # TODO
        return self.postcondition

    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.       

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        # TODO
        resistpop = 0
        count = 0
        for virus in self.viruses:
            for drug in drugResist:
                if virus.isResistantTo(drug) == False:
                    break
                else:
                    count += 1
            if count == len(drugResist):
                resistpop += 1
            count = 0
        return resistpop

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """
        # TODO
        temp_viruses = self.getViruses().copy()
        for virus in temp_viruses:
            if virus.doesClear():
                self.viruses.remove(virus)
            popDensity = len(self.viruses) / self.getMaxPop()
            if 0.0 < popDensity < 1.0:
                try:
                    offspring = virus.reproduce(popDensity, self.getPrescriptions())
                    self.viruses.append(offspring)
                except NoChildException:
                    pass
        return len(self.viruses)


#
# PROBLEM 5
#
def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numTrials):
    """
    Runs simulations and plots graphs for problem 5.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1). 
    numTrials: number of simulation runs to execute (an integer)
    
    """
    # TODO
    avg_total_pop = 300 * [0]
    avg_resist_pop = 300 * [0]
    for trial in range(numTrials):
        viruses = []
        for virus in range(numViruses):
            viruses.append(ResistantVirus(maxBirthProb, clearProb, resistances, mutProb))
        p = TreatedPatient(viruses, maxPop)
        for time_step in range(150):
            p.update()
            avg_total_pop[time_step] += p.getTotalPop()
            avg_resist_pop[time_step] += p.getResistPop(["guttagonol"])
        p.addPrescription("guttagonol")
        for time_step in range(150, 300):
            p.update()
            avg_total_pop[time_step] += p.getTotalPop()
            avg_resist_pop[time_step] += p.getResistPop(["guttagonol"])
    avg_total_pop[:] = [e / numTrials for e in avg_total_pop]
    avg_resist_pop[:] = [e / numTrials for e in avg_resist_pop]
    # pylab.plot(avg_total_pop, label = "Total")
    # pylab.plot(avg_resist_pop, label = "ResistantVirus")
    # pylab.title("ResistantVirus simulation")
    # pylab.xlabel("time step")
    # pylab.ylabel("# viruses")
    # pylab.legend(loc = "best")
    # pylab.show()
    # # print(avg_total_pop)
    # print(avg_resist_pop)
    plt.plot(avg_total_pop, label = "Total")
    plt.plot(avg_resist_pop, label = "ResistantVirus")
    plt.title("ResistantVirus simulation")
    plt.xlabel("time step")
    plt.ylabel("# viruses")
    plt.legend(loc = "best")
    plt.show()

# from ps3b_precompiled_312 import *
# Test
simulationWithDrug(100, 1000, 0.1, 0.05, {'guttagonol': False}, 0.005, 100)
# simulationWithDrug(1, 10, 1.0, 0.0, {}, 1.0, 5)
# simulationWithDrug(1, 20, 1.0, 0.0, {"guttagonol": True}, 1.0, 5)
# simulationWithDrug(75, 100, .8, 0.1, {"guttagonol": True}, 0.8, 1)
# simulationWithDrug(100, 500, 1.0, 0.0, {}, 1.0, 5)