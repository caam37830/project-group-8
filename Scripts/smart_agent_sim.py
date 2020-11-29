# fmt: off
import sys
import os
import numpy as np
sys.path.append("../")  # lets us access sibling directory `sir`
from sir.smart_agent import *
import matplotlib.pyplot as plt
# fmt: on


def sim_agent(
    p,
    q,
    k,
    size,
    t,
    knowledge_threshold=0,
    fear_threshold=0,
    knowledge_distance=0,
    fear_distance=0,
    prob_infect=None,
    initial_infect=None,
):
    """
    returns `days` by `4` numpy array, with columns ...
        - day number
        - number susceptible
        - number infected
        - number recovered
    """
    sim = SmartAgentModel2D(
        p=p,
        q=q,
        k=k,
        size=size,
        knowledge_threshold=knowledge_threshold,
        fear_threshold=fear_threshold,
        knowledge_distance=knowledge_distance,
        fear_distance=fear_distance,
        prob_infect=prob_infect,
        initial_infect=initial_infect,
    )
    vals = sim.step_t_days(t)
    return vals


X = sim_agent(
    p=0.1,
    q=0.1,
    k=0.1,
    size=500,
    t=50,
    knowledge_threshold=1,
    fear_threshold=1,
    knowledge_distance=0,
    fear_distance=0.25,
    prob_infect=1,
    initial_infect=2,
)

print(X[3][0])

for t in range(10):
    fig, ax = plt.subplots()
    for ii in range(len(X[3][t])):
        if X[3][t][ii] == 0:
            color = "blue"
        elif X[3][t][ii] == 1:
            color = "red"
        else:

            color = "green"
        x, y = X[1][t][ii], X[2][t][ii]
        ax.scatter(x, y, c=color, alpha=0.3, edgecolors="none")

    ax.grid(True)
    plt.show()
