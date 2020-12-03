import numpy as np
import random
from matplotlib import pyplot as plt
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
