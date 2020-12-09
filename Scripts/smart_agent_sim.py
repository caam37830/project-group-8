# fmt: off
import sys
import os
import numpy as np
sys.path.append("../")  # lets us access sibling directory `sir`
from sir.smartagent import *
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
# fmt: on


def sim_agent(
    p,
    q,
    k,
    size,
    t,
    knowledge_threshold=1,
    fear_threshold=1,
    knowledge_distance=0,
    fear_distance=0,
    prob_infect=None,
    initial_infect=None,
):
    """
    returns simulation information with infected agents placed randomly around the population
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


# parameters for simulation with no learning
P = 0.01
Q = 0.01
K = 0.05
Size = 10000
T = 200
KT = 1
FT = 1
KD = 0
FD = 0
PI = 1
II = 5

# simulation with no learning
X = sim_agent(
    p=P,
    q=Q,
    k=K,
    size=Size,
    t=T,
    knowledge_threshold=KT,
    fear_threshold=FT,
    knowledge_distance=KD,
    fear_distance=FD,
    prob_infect=PI,
    initial_infect=II,
)

figfull = plt.figure(figsize=(10, 10))
count = 1
for t in [0, 66, 133, 199]:
    plt.subplot(2, 2, count)
    for ii in range(len(X[3][t])):
        if X[3][t][ii] == 0:
            color = "blue"
        elif X[3][t][ii] == 1:
            color = "red"
        else:
            color = "green"
        x, y = X[1][t][ii], X[2][t][ii]
        plt.scatter(x, y, c=color, alpha=0.5, edgecolors="none")
        plt.title("state at t = {}".format(t + 1))
    count = count + 1
blue_patch = mpatches.Patch(color="blue", label="susceptible")
red_patch = mpatches.Patch(color="red", label="infected")
green_patch = mpatches.Patch(color="green", label="recovered")
figfull.legend(handles=[blue_patch, red_patch, green_patch])
figfull.suptitle("p = 0.01, q = 0.01, k = 0.05, size = 10000, I0 = 5, no learning")
plt.savefig("../doc/final/plots/nolearn.png")
print(X[0])

# parameters for simulation with learning
P = 0.01
Q = 0.01
K = 0.05
Size = 10000
T = 200
KT = 1000
FT = 1000
KD = 0.1
FD = 0.1
PI = 1
II = 5

# simulation with no learning
X = sim_agent(
    p=P,
    q=Q,
    k=K,
    size=Size,
    t=T,
    knowledge_threshold=KT,
    fear_threshold=FT,
    knowledge_distance=KD,
    fear_distance=FD,
    prob_infect=PI,
    initial_infect=II,
)

figfull = plt.figure(figsize=(10, 10))
count = 1
for t in [0, 66, 133, 199]:
    plt.subplot(2, 2, count)
    for ii in range(len(X[3][t])):
        if X[3][t][ii] == 0:
            color = "blue"
        elif X[3][t][ii] == 1:
            color = "red"
        else:
            color = "green"
        x, y = X[1][t][ii], X[2][t][ii]
        plt.scatter(x, y, c=color, alpha=0.5, edgecolors="none")
        plt.title("state at t = {}".format(t + 1))
    count = count + 1
blue_patch = mpatches.Patch(color="blue", label="susceptible")
red_patch = mpatches.Patch(color="red", label="infected")
green_patch = mpatches.Patch(color="green", label="recoverd")
figfull.legend(handles=[blue_patch, red_patch, green_patch])
figfull.suptitle(
    "p = 0.01, q = 0.01, k = 0.05, size = 10000, I0 = 5, kt = ft = 1000, kd = fd = 0.1"
)
plt.savefig("../doc/final/plots/yeslearn.png")
print(X[0])
