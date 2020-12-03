"""
Visualization of `ConwayModel` class outputs
"""
import os
import sys
import random
import numpy as np
from matplotlib import pyplot as plt

# Make an adjustment to where python will look for classes
# Since this script can be run from within `/test`, a sibling
# directory of `/sir`, or from the main project directory
if os.getcwd().split("/")[-2] == "project-group-8":
    sys.path.append("../sir")
else:
    sys.path.append("./sir")
from conway_agent import ConwayModel, ConwayAgent


def generate_agents(num_agents, prop_alive, prop_infect):
    """
    Generate `num_agents` randomly, with `prop_alive` of them initially in the
    alive state and `prop_infect` of the initially alive in the infected state
    """
    start_alive = np.array(np.random.random(num_agents) <= prop_alive, dtype=np.int8)
    start_infected = np.array(
        np.random.random(num_agents) <= prop_infect, dtype=np.int8
    )

    agents = []
    for ii in range(num_agents):
        agents.append(ConwayAgent(ii, False))
        if start_alive[ii]:
            agents[ii].born()
            if start_infected[ii]:
                agents[ii].infect()

    return agents


def simulate_and_animate(days, m, n, k, p, prop_alive, prop_infect):
    """
    Simulate `days` and produce a GIF file
    Returns the day-by-day tallies in a numpy array
    """
    agents = generate_agents(m * n, prop_alive, prop_infect)
    model = ConwayModel(m, n, k, p, agents)
    filename = "conway_k{}_p{}.gif".format(k, p)
    results = model.plot_t_days(days, filename)
    return results


# Run some simulations with various parameters
if __name__ == "__main__":
    simulate_and_animate(200, 50, 50, 0.1, 0.5, 0.4, 0.2)
