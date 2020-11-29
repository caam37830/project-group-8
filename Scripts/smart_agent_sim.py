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
    knowledge_factor=0,
    fear_factor=0,
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
        knowledge_factor=knowledge_factor,
        fear_factor=fear_factor,
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
    size=100,
    t=50,
    knowledge_factor=0.1,
    fear_factor=0.1,
    knowledge_distance=0.1,
    fear_distance=0.1,
    prob_infect=1,
    initial_infect=2,
)

print(X[0])

plt.figure()
plt.scatter(X[1][0], X[2][0])
plt.show()

plt.figure()
plt.scatter(X[1][1], X[2][1])
plt.show()

plt.figure()
plt.scatter(X[1][2], X[2][2])
plt.show()

plt.figure()
plt.scatter(X[1][3], X[2][3])
plt.show()

plt.figure()
plt.scatter(X[1][4], X[2][4])
plt.show()

plt.figure()
plt.scatter(X[1][5], X[2][5])
plt.show()