import random
import math


class SIRModel:
    def __init__(self, b, k, size, prob_infect=1, b_infected=None):
        """
        Initialize an `SIRModel` class
        :param b: number of interactions per day, per agent, which could result in infection
        :param k: proportion of infected who recover/removed each day
        :param size: number of agents to generate
        :param prob_infect: (optional) probability that an interaction between a susceptible
        agent and an infected agent results in the susceptible agent's infection
        :param b_infected: (optional) number of interactions per day for individuals who are
        infected. Allows easy simulation of "social-distancing" scenarios
        """
        self.b = b
        self.k = k
        self.size = size
        self.agents = [Agent(ii) for ii in range(size)]
        self.susceptible = [agent.id for agent in self.agents]
        self.infected = []
        self.recovered = []
        self.days_passed = 0
        self.prob_infect = prob_infect
        self.b_infected = b if b_infected is None else b_infected

    def exogenous_infect(self, n=None, indices=None):
        """
        Infect `n` of the individuals in `self.population` exogenously (i.e., outside
        model parameters)
        :param n: Number of agents to infect
        :param indices: Alternative to `n`, specify the indices in `self.agents` to infect
        :return: None
        """
        if n is not None:
            if n <= len(self.susceptible):
                infected = sorted(random.sample(self.susceptible, k=n))
                for agent_id in infected:
                    self.susceptible.remove(agent_id)
                    self.infected.append(agent_id)
                    self.agents[agent_id].infect()
            else:
                print(
                    "SIRModel.exogenous_infect: `n` greater than the number of susceptible agents"
                )

        if indices is not None:
            if set(indices).issubset(set(self.susceptible)):
                for agent_id in indices:
                    self.susceptible.remove(agent_id)
                    self.infected.append(agent_id)
                    self.agents[agent_id].infect()
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
        Reset the model to its initial state
        :return: None
        """
        for agent in self.agents:
            agent.reset()

        self.susceptible = list(range(self.size))
        self.infected = []
        self.recovered = []


    def categorize_agents(self):
        """
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
        :return:
        """
        agent_ids = [agent.id for agent in self.agents]
        # Recover k proportion of the infected
        num_recover = math.floor(len(self.infected) * self.k)
        ids_recover = random.sample(self.infected, k=num_recover)
        for r_id in ids_recover:
            self.agents[r_id].recover()

        # Infect susceptible agents, if they meet an infected agent
        for i_id in self.infected:
            meet = random.sample(agent_ids, k=self.b_infected)
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


    def summarise_model(self):
        """

        :return:
        """
        num_susceptible = len(self.susceptible)
        num_infected = len(self.infected)
        num_recovered = len(self.recovered)
        return self.days_passed, num_susceptible, num_infected, num_recovered

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
