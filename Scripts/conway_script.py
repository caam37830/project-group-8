"""
Visualization of `ConwayModel` class outputs
"""
import os
import sys
import random
import numpy as np
from matplotlib import pyplot as plt

# Make an adjustment to where python will look for classes. Since this script
# can be run from within `/script`, a sibling directory of `/sir`, or from the
# main project directory
if os.getcwd().split("/")[-2] == "project-group-8":
    sys.path.append("../sir")
    IMG_PREFIX = "../doc/final/conway_plots/"
else:
    sys.path.append("./sir")
    IMG_PREFIX = "./doc/final/conway_plots/"
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


def simulate_and_animate(days, m, n, k, p, prop_alive, prop_infect, file_prefix=None):
    """
    Simulate `days` and produce a GIF file
    Returns the day-by-day tallies in a numpy array
    """
    def generate_filename():
        """
        Generate a descriptive filename for each simulation
        """
        if file_prefix is None:
            return "conway_m_{}_n_{}_k_{}_p_{}_pia_{}_pii_{}.gif".format(
                m, n, k, p, pa, pi
            )
        return file_prefix + "conway_m_{}_n_{}_k_{}_p_{}_pia_{}_pii_{}.gif".format(
            m, n, k, p, pa, pi
        )

    agents = generate_agents(m * n, prop_alive, prop_infect)
    model = ConwayModel(m, n, k, p, agents)
    filename = generate_filename()
    results = model.plot_t_days(days, filename)
    return results


# Run some simulations with various parameters
ms = np.array([50, 100, 200, 500]).repeat(4)
ns = np.array([50, 100, 200, 500]).repeat(4)
ks = np.tile(np.array([0.1, 0.2, 0.3, 0.4]), 4)
ps = np.tile(np.array([0.1, 0.4, 0.7, 1.0]), 4)

# The following affect ONLY the initial state
prop_alive = np.tile(np.array([0.3, 0.4, 0.5, 0.6]), 4)
prop_infect = np.tile(np.array([0.3, 0.4, 0.5, 0.6]), 4)
for m, n, k, p, pa, pi in zip(ms, ns, ks, ps, prop_alive, prop_infect):
    # Simulate 100 days and save results to a gif file
    filename = IMG_PREFIX + "conway_m_{}_n_{}_k_{}_p_{}_pia_{}_pii_{}.gif".format(
	m, n, k, p, pa, pi
    )
    results = simulate_and_animate(200, m, n, k, p, pa, pi, filename)
    # Print filename and results to stdout, so we can look ath them later if we want
    print(
	"m = {}, n = {}, k = {}, p = {}, pia = {}, pii = {}".format(
	    m, n, k, p, pa, pi
	)
    )
    print("-" * 80)
    print(results)
