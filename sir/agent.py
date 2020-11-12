import random
import math
import numpy as np


class SIRModel:
    def __init__(self, b, k, size, prob_infect=1, initial_infect=None):
        """
        Initialize an `SIRModel` class
        :param b: number of interactions per day, per agent, which could result in infection
        :param k: proportion of infected who recover/removed each day
        :param size: number of agents to generate
        :param prob_infect: (optional) probability that an interaction between a susceptible
        agent and an infected agent results in the susceptible agent's infection
        :param initial_infect: (optional) if supplied, start with `initial_infect` agents already infected
        """
        self.b, self.k, self.size = b, k, size
        self.agents = [Agent(ii) for ii in range(size)]
        self.susceptible = [agent.id for agent in self.agents]
        self.infected = []
        self.recovered = []
        self.days_passed = 0
        self.prob_infect = prob_infect
        self.initial_infect = initial_infect
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
                    "SIRModel.exogenous_infect: `n` greater than the number of susceptible agents"
                )

        if indices is not None:
            if set(indices).issubset(set(self.susceptible)):
                for agent_id in indices:
                    self.agents[agent_id].infect()
                    self.categorize_agents()
            else:
                print(
                    "SIRModel.exogenous_infect: `indices` contains non-susceptible agents"
                )

        if n is None and indices is None:
            print(
                "SIRModel.exogenous_infect: supply either `n` or `indices`. No action was taken"
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

    def categorize_agents(self):
        """
        Iterate through the agents, and append their `id` to the appropriate list
        based off their current status
        :return:
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

        # Recover k proportion of the infected
        num_recover = math.ceil(len(self.infected) * self.k)
        ids_recover = random.sample(self.infected, k=num_recover)
        for r_id in ids_recover:
            self.agents[r_id].recover()
            self.categorize_agents()

        # Infect susceptible agents, if they meet an infected agent
        for i_id in self.infected:
            meet = random.sample(agent_ids, k=self.b)
            # If there is intersection between `meet` and `self.infected`, the agent
            # has met someone who is infected -- so they will be infected
            for id in meet:
                if id in self.susceptible:
                    # This allows us to change the probability of infection occuring
                    infect = random.random()
                    if infect < self.prob_infect:
                        self.agents[id].infect()

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

        # Initialize the 0th index to the initial state of the model
        num_d[0], num_s[0], num_i[0], num_r[0] = self.summarize_model()

        for ii in np.arange(1, days):
            self.step()
            num_d[ii], num_s[ii], num_i[ii], num_r[ii] = self.summarize_model()

        return np.array([num_d, num_s, num_i, num_r]).T

    def summarize_model(self):
        """
        Summarize the current state of the `SIRModel` object
        :return: A tuple summarizing the state of the model
        """
        return (
            self.days_passed,
            len(self.susceptible),
            len(self.infected),
            len(self.recovered),
        )


class Agent:
    def __init__(self, agent_id):
        """
        Initialize the `Agent` as susceptible
        """
        self.s = True
        self.i = False
        self.r = False
        self.id = agent_id

    def reset(self):
        """
        Reset the `Agent` to its initial state; i.e., make them susceptible again
        Opens possibility of reinfection in simulations
        :return: None
        """
        self.s = True
        self.i = False
        self.r = False

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

    def status(self):
        """
        Return a tuple of the `Agent`'s current state: `s`, `i`, `r`
        :return: Tuple
        """
        return self.s, self.i, self.r
