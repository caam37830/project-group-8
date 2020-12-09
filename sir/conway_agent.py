"""
Class definitions for `ConwayAgent` and `ConwayModel` classes
"""

import random
import math
import numpy as np
from scipy import sparse as sp
from matplotlib import colors
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from agent import Agent, DiscreteAgentModel


class ConwayModel:
    def __init__(self, m, n, k, p, agents):
        """
        Initalize a `ConwayModel` class.
        :param m: number of rows on the grid
        :param n: number of columns on the grid
        :param k: proportion of infected who recover each day
        :param p: probability of infection, if a susceptible agent and an infected agent interact
        :param agents: a list of m * n `ConwayAgent`s set to the desired initial state
        """
        self.m, self.n, self.k, self.p, self.agents = m, n, k, p, agents
        self.alive_agents = self.get_alive_agents()
        self.set_agent_grid()
        self.set_conway_grid()
        self.days_passed = 0

    def get_alive_agents(self):
        """
        Filter the agent list to only those which are 'alive' (according to Conway's definition of alive)
        """
        return [agent for agent in self.agents if agent.is_alive]

    def set_alive_agents(self, born_list):
        """
        Set all agents as being alive or dead, based on membership in a list of ids
        """
        for agent in self.agents:
            if agent.id in born_list:
                agent.born()
            else:
                agent.kill()

        self.alive_agents = self.get_alive_agents()

    def set_agent_grid(self, update=False):
        """
        Create an `m` x `n` grid of agent statuses. Can also update `self.alive_agents` if desired
        0 = dead agent
        1 = susceptible agent
        2 = infected agent
        3 = removed agent (but alive)
        """
        if update:
            self.alive_agents = self.get_alive_agents()

        data = []
        ids = []
        for agent in self.alive_agents:
            data.append(agent.status())
            ids.append(agent.id)

        rows, cols = np.unravel_index(ids, shape=(self.m, self.n))
        self.agent_grid = sp.csr_matrix(
            (data, (rows, cols)), shape=(self.m, self.n), dtype=np.int8
        ).toarray()

    def set_conway_grid(self, update=False):
        """
        Create an `m` x `n` grid indicating which agents are alive
        """
        if update:
            self.alive_agents = self.get_alive_agents()

        data = []
        ids = []
        for agent in self.alive_agents:
            data.append(1)
            ids.append(agent.id)

        rows, cols = np.unravel_index(ids, shape=(self.m, self.n))
        self.conway_grid = sp.csr_matrix(
            (data, (rows, cols)), shape=(self.m, self.n)
        ).toarray()

    def count_neighbors(self, grid):
        """
        Count the number of neighbors at every point on a certain grid of 0s and 1s
        """
        counts = np.zeros(grid.shape)
        counts[1:, :] += grid[:-1, :]
        counts[:, 1:] += grid[:, :-1]
        counts[:-1, :] += grid[1:, :]
        counts[:, :-1] += grid[:, 1:]
        counts[1:, 1:] += grid[:-1, :-1]
        counts[1:, :-1] += grid[:-1, 1:]
        counts[:-1, 1:] += grid[1:, :-1]
        counts[:-1, :-1] += grid[1:, 1:]
        return counts

    def step_conway(self):
        """
        The first part of every 'turn': Conway moves.
        Need to update the killed/born agents
        """
        self.set_conway_grid(True)
        prior = self.conway_grid.copy()
        counts = self.count_neighbors(prior)
        post = np.logical_or(np.logical_and(counts == 2, prior), counts == 3)

        born_rows, born_cols = np.where(post == 1)
        born_ids = np.ravel_multi_index((born_rows, born_cols), (self.m, self.n))

        self.set_alive_agents(born_ids)
        self.conway_grid = post

    def step_agents(self):
        """
        The second part of every 'turn': agent moves.
        Need to update the susceptible / infect / recovered
        """
        self.set_agent_grid(True)
        # Determine who is infected
        infected_ids = [agent.id for agent in self.agents if (agent.status() == 2)]

        # Find susceptible and infected agents
        s_grid = np.array(self.agent_grid == 1, dtype=np.int8)
        i_grid = np.array(self.agent_grid == 2, dtype=np.int8)

        # Find the number of nearby infected agents
        num_infected_nearby = self.count_neighbors(i_grid)

        # We incorporate randomness drawn from standard uniform
        uniform = np.random.random(i_grid.shape)

        # Incoroporate the probability of being infected, based on `self.p`,
        # randomness from the uniform distribution, and the number of nearby infected
        # agents. This can only apply to agents who are currently susceptible, so we
        # also compare against s_grid
        infect_ids = np.ravel_multi_index(
            np.where(
                np.logical_and(
                    np.array(
                        np.power(uniform, num_infected_nearby) <= self.p,
                        dtype=np.int8,
                    ),
                    s_grid,
                )
            ),
            (self.m, self.n),
        )

        # Infect those agents
        for i_id in infect_ids:
            self.agents[i_id].infect()

        # Recover `self.k` proportion of the infected agents
        recover_ids = np.array(
            random.sample(infected_ids, k=math.ceil(self.k * len(infected_ids)))
        )
        for r_id in recover_ids:
            self.agents[r_id].recover()

        # Set the new `self.agent_grid` and we are done
        self.set_agent_grid(True)

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
            self.step_conway()
            self.step_agents()
            self.days_passed += 1
            num_d[ii], num_s[ii], num_i[ii], num_r[ii] = self.summarize_model()

        return np.array([num_d, num_s, num_i, num_r]).T

    def summarize_model(self):
        """
        Return the number of infected, susceptible, and recovered "alive" agents,
        as well as the number of days passed, in a tuple
        """
        agent_status = np.array([agent.status() for agent in self.alive_agents])
        num_i = np.sum(agent_status == 1)
        num_s = np.sum(agent_status == 2)
        num_r = np.sum(agent_status == 3)
        return self.days_passed, num_i, num_s, num_r

    def plot_t_days(self, days, filename):
        """
        Simulate for `days`. Save the resulting animation to a GIF file. Return
        the `summarize_model()` output for each day in a `days` x 4 numpy array
        """
        fig = plt.figure(figsize=(8, 8))
        fig.set_tight_layout(True)
        plt.axis("off")

        num_d = np.zeros(days, dtype=np.int64)  # day indices
        num_s = np.zeros(days, dtype=np.int64)  # num susceptible
        num_i = np.zeros(days, dtype=np.int64)  # num infected
        num_r = np.zeros(days, dtype=np.int64)  # num recovered

        cmap = colors.ListedColormap(["white", "blue", "red", "green"])
        bounds = [0, 1, 2, 3, 4]
        norm = colors.BoundaryNorm(bounds, cmap.N)
        im = plt.imshow(
            self.agent_grid,
            interpolation="nearest",
            origin="lower",
            cmap=cmap,
            norm=norm,
        )

        def update_gol(frame, print_progress=False):
            """
            Helper function for `FuncAnimation`. Rules on how to update the frame.
            Also grab the summary statistics for each frame
            """
            nonlocal im
            if print_progress:
                print("{} : Creating frame {} out of {}".format(filename, frame, days))
            self.step_conway()
            self.step_agents()
            (
                num_d[frame],
                num_s[frame],
                num_i[frame],
                num_r[frame],
            ) = self.summarize_model()
            self.days_passed += 1

            im.set_array(self.agent_grid)
            return (im,)

        anim = FuncAnimation(
            fig, update_gol, frames=np.arange(days), interval=200, blit=True
        )
        anim.save(filename, dpi=150, writer="imagemagick", fps=10)
        return np.array([num_d, num_s, num_i, num_r]).T


class ConwayAgent(Agent):
    """
    `ConwayAgent` class for the Conway game-of-life model
    All that need be added is a status as to whether the agent is alive
    """

    def __init__(self, agent_id, is_alive):
        """
        Initialize a new `ConwayAgent`. This adds an additional parameter: `is_alive`,
        to enable the two "games" (Conway + SIR model) to be played on the same board
        """
        super().__init__(agent_id)
        self.initial_alive = is_alive
        self.is_alive = is_alive

    def reset(self):
        """
        Reset the agent to its initial state
        """
        super().reset()
        self.is_alive = self.initial_alive

    def infect(self):
        """
        If the agent is alive and susceptible, infect the agent
        """
        if self.is_alive and self.s:
            super().infect()

    def recover(self):
        """
        If the agent is alive and infected, recover the agent
        """
        if self.is_alive and self.i:
            super().recover()

    def born(self):
        """
        Birth / reincarnation: take your pick
        """
        if not self.is_alive:
            self.is_alive = True

    def kill(self):
        """
        Dodge this
        """
        if self.is_alive:
            self.is_alive = False

    def status(self):
        """
        Get the agent's status:
        0 = dead
        1 = susceptible
        2 = infected
        3 = recovered
        """
        if self.is_alive:
            if self.s:
                return 1
            elif self.i:
                return 2
            return 3
        return 0
