"""
Definitions for `DiscreteAgent` class, and the `Agent` class
"""

import random
import math
import numpy as np
import networkx as nx
from sklearn.neighbors import BallTree
from scipy.optimize import Bounds, minimize, NonlinearConstraint


# TODO: This class will be renamed to `DiscreteAgentModel` shortly after the
# midterm checkpoint. I just don't want to interfere with code that has already
# been submitted to run on the Midway RCC
class SmartAgentModel2D:
    def __init__(
        self,
        p,
        q,
        k,
        size,
        knowledge_threshold=0,
        fear_threshold=0,
        knowledge_distance=0,
        fear_distance=0,
        prob_infect=None,
        initial_infect=None,
    ):
        """
        Initialize an `DiscreteAgentModel` class
        :param b: number of interactions per day, per agent, which could result in infection
        :param k: proportion of infected who recover/removed each day
        :param size: number of agents to generate
        :param prob_infect: (optional) probability that an interaction between a susceptible
        agent and an infected agent results in the susceptible agent's infection
        :param initial_infect: (optional) if supplied, start with `initial_infect` agents already infected
        :return: None
        """
        (
            self.p,
            self.q,
            self.k,
            self.size,
            self.knowledge_threshold,
            self.fear_threshold,
            self.knowledge_distance,
            self.fear_distance,
        ) = (
            p,
            q,
            k,
            size,
            knowledge_threshold,
            fear_threshold,
            knowledge_distance,
            fear_distance,
        )
        self.agents = [SmartAgent(ii) for ii in range(size)]
        self.susceptible = [agent.id for agent in self.agents]
        self.locations = [agent.pos for agent in self.agents]
        self.infected = []
        self.recovered = []
        self.days_passed = 0
        self.initial_infect = initial_infect
        self.prob_infect = 1 if prob_infect is None else prob_infect
        if self.initial_infect is not None:
            self.exogenous_infect(n=initial_infect)

    def exogenous_infect(self, n=None, indices=None):
        """
        Infect `n` of the individuals in `self.population` exogenously (i.e., outside model parameters)
        :param n: Number of agents to infect
        :param indices: Alternative to `n`, specify the indices in `self.agents` to infect
        :return: None
        """
        if n is not None:
            if n <= len(self.susceptible):
                infected = sorted(random.sample(self.susceptible, k=n))
                for agent_id in infected:
                    self.agents[agent_id].infect()
                    self.categorize_agents()
            else:
                print(
                    "DiscreteAgentModel.exogenous_infect: `n` greater than the number of susceptible agents"
                )

        if indices is not None:
            if set(indices).issubset(set(self.susceptible)):
                for agent_id in indices:
                    self.agents[agent_id].infect()
                    self.categorize_agents()
            else:
                print(
                    "DiscreteAgentModel.exogenous_infect: `indices` contains non-susceptible agents"
                )

        if n is None and indices is None:
            print(
                "DiscreteAgentModel.exogenous_infect: supply either `n` or `indices`. No action was taken"
            )

    def reset(self):
        """
        Reset the model to a "clean slate"
        :return: None
        """
        for agent in self.agents:
            agent.reset()

        self.susceptible = list(range(self.size))
        self.infected = []
        self.recovered = []
        self.days_passed = 0

    def categorize_agents(self):
        """
        Iterate through the agents, and append their `id` to the appropriate list
        based off their current status
        :return: None
        """
        self.susceptible = []
        self.infected = []
        self.recovered = []
        for agent in self.agents:
            s, i, r = agent.status()
            if s:
                self.susceptible.append(agent.id)
            elif i:
                self.infected.append(agent.id)
            else:
                self.recovered.append(agent.id)

    def step(self):
        """
        Simulate one day according to SIR model parameters
        :return: None
        """
        agent_ids = [agent.id for agent in self.agents]
        # agents learn and become more fearful, then move and we store new locations of all agents
        tree = BallTree(np.array(self.locations))
        for ii in agent_ids:
            if self.fear_distance != 0:
                ind_fear = tree.query_radius(
                    self.locations[ii : ii + 1], r=self.fear_distance
                )
                self.agents[ii].react(
                    len(set(ind_fear[0]).intersection(set(self.infected)))
                )
            if self.knowledge_distance != 0:
                ind_knowledge = tree.query_radius(
                    self.locations[ii : ii + 1], r=self.knowledge_distance
                )
                self.agents[ii].learn(
                    len(set(ind_knowledge[0]).intersection(set(self.infected)))
                    + len(set(ind_knowledge[0]).intersection(set(self.recovered)))
                )
            if (
                self.fear_distance != 0
                and len(set(ind_fear[0]).intersection(set(self.infected))) > 0
                and self.agents[ii].s == True
                and self.agents[ii].fear > self.fear_threshold
            ):
                self.agents[ii].move(
                    self.p,
                    self.fear_threshold,
                    [
                        self.locations[jj]
                        for jj in set(ind_fear[0]).intersection(set(self.infected))
                    ],
                )
            elif (
                self.fear_distance != 0
                and len(set(ind_fear[0]).intersection(set(self.susceptible))) > 0
                and self.agents[ii].i == True
                and self.agents[ii].knowledge > self.knowledge_threshold
            ):
                self.agents[ii].move(
                    self.p,
                    self.fear_threshold,
                    [
                        self.locations[jj]
                        for jj in set(ind_fear[0]).intersection(set(self.susceptible))
                    ],
                )
            else:
                self.agents[ii].move(self.p, self.fear_threshold)
            self.locations[ii] = self.agents[ii].pos

        # Recover k proportion of the infected
        num_recover = np.random.choice(
            [
                math.ceil(len(self.infected) * self.k),
                math.floor(len(self.infected) * self.k),
            ]
        )
        if num_recover > 0:
            ids_recover = random.sample(self.infected, k=num_recover)
            for r_id in ids_recover:
                self.agents[r_id].recover()
                self.categorize_agents()

        # infected agents infect individuals within range q
        tree = BallTree(np.array(self.locations))
        for ii in self.infected:
            ind = tree.query_radius(self.locations[ii : ii + 1], r=self.q)
            num_infect = math.ceil(len(ind[0][1:]) * self.prob_infect)
            new_infect = random.sample(set(ind[0][1:]), num_infect)
            for jj in new_infect:
                self.agents[jj].infect()

        self.categorize_agents()
        self.days_passed += 1

    def step_t_days(self, days):
        """
        Simulate infections for `days` according to the procedure defined in `step`
        :param days: Number of days to step
        :return: `days` by `4` numpy array, with columns ...
          - day number
          - number susceptible
          - number infected
          - number recovered
        """
        num_d = np.zeros(days, dtype=np.int64)  # day indices
        num_s = np.zeros(days, dtype=np.int64)  # num susceptible
        num_i = np.zeros(days, dtype=np.int64)  # num infected
        num_r = np.zeros(days, dtype=np.int64)  # num recovered
        locsX = np.zeros((days, self.size))
        locsY = np.zeros((days, self.size))
        infected = np.zeros((days, self.size), dtype=np.int64)
        for jj in range(self.size):
            locsX[0, jj] = np.round(self.locations[jj][0], 5)
            locsY[0, jj] = np.round(self.locations[jj][1], 5)
            if self.agents[jj].i == True:
                infected[0, jj] = int(1)
            elif self.agents[jj].r == True:
                infected[0, jj] = int(2)
            else:
                infected[0, jj] = int(0)
        # Initialize the 0th index to the initial state of the model
        num_d[0], num_s[0], num_i[0], num_r[0] = self.summarize_model()

        for ii in np.arange(1, days):
            self.step()
            num_d[ii], num_s[ii], num_i[ii], num_r[ii] = self.summarize_model()
            for jj in range(self.size):
                locsX[ii, jj] = np.round(self.locations[jj][0], 5)
                locsY[ii, jj] = np.round(self.locations[jj][1], 5)
                if self.agents[jj].i == True:
                    infected[ii, jj] = int(1)
                elif self.agents[jj].r == True:
                    infected[ii, jj] = int(2)
                else:
                    infected[ii, jj] = int(0)

        return np.array([num_d, num_s, num_i, num_r]).T, locsX, locsY, infected

    def summarize_model(self):
        """
        Summarize the current state of the `DiscreteAgentModel` object
        :return: A tuple summarizing the state of the model
        """
        return (
            self.days_passed,
            len(self.susceptible),
            len(self.infected),
            len(self.recovered),
        )


class SmartAgent:
    def __init__(self, agent_id, pos=None):
        """
        Initialize the `Agent` as susceptible
        """
        self.s = True
        self.i = False
        self.r = False
        self.id = agent_id
        if pos == None:
            self.pos = np.random.rand(2)
        else:
            self.pos = pos
        self.knowledge = 0
        self.fear = 0

    def reset(self):
        """
        Reset the `Agent` to its initial state; i.e., make them susceptible again
        Opens possibility of reinfection in simulations
        :return: None
        """
        self.s = True
        self.i = False
        self.r = False
        self.pos = np.random.rand(2)
        self.knowledge = 0
        self.fear = 0

    def infect(self):
        """
        Infect the `Agent`.
        Checks that initial state was "susceptible", otherwise no action is taken
        :return: None
        """
        if self.s:
            self.s = False
            self.i = True
            self.r = False

    def recover(self):
        """
        Recover the `Agent` from the infected state
        Checks that the initial state was "infected", otherwise no action is taken
        :return: None
        """
        if self.i:
            self.s = False
            self.i = False
            self.r = True

    def move(self, p, fear_threshold, loc_nearby=None):
        """
        Moves the `Agent` in a smart direction based off of the agents fear of the virus
        Checks that the initial state was "infected", otherwise no action is taken
        :return: None
        """
        if loc_nearby == None or self.r == True:
            new_loc = [-1, -1]
            while new_loc[0] < 0 or new_loc[0] > 1 or new_loc[1] < 0 or new_loc[1] > 1:
                delta = (
                    p
                    * np.random.choice([1, -1], size=2, replace=True)
                    * np.random.rand(2)
                )
                new_loc = self.pos + delta
            self.pos = new_loc
        else:

            def f(x):
                return -np.linalg.norm(x - loc_nearby)

            def cons_f(x):
                return [(x[0] - self.pos[0]) ** 2 + (x[1] - self.pos[1]) ** 2]

            bounds = Bounds(
                [0, 0],
                [1, 1],
            )
            cons = NonlinearConstraint(cons_f, -np.inf, p)
            res = minimize(f, x0=self.pos, constraints=cons, bounds=bounds)
            new_loc = res.x
            self.pos = new_loc

    def learn(self, num_infect_or_recovered_nearby):
        """
        Moves the `Agent` in a smart direction based off of the agents fear of the virus
        Checks that the initial state was "infected", otherwise no action is taken
        :return: None
        """
        self.knowledge = self.knowledge + num_infect_or_recovered_nearby

    def react(self, num_nearby):
        """
        Moves the `Agent` in a smart direction based off of the agents fear of the virus
        Checks that the initial state was "infected", otherwise no action is taken
        :return: None
        """
        self.fear = self.fear + num_nearby

    def status(self):
        """
        Return a tuple of the `Agent`'s current state: `s`, `i`, `r`
        :return: Tuple
        """
        return self.s, self.i, self.r
