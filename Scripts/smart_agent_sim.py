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


P = 0.01
Q = 0.01
K = 0.05
Size = 10000
T = 100
KT = 1
FT = 1
KD = 0
FD = 0
PI = 1
II = 5

X = sim_agent(
    p=P,
    q=Q,
    k=K,
    size=Size,
    t=100,
    knowledge_threshold=KT,
    fear_threshold=FT,
    knowledge_distance=KD,
    fear_distance=FD,
    prob_infect=PI,
    initial_infect=II,
)

figfull = plt.figure(figsize=(10, 10))
count = 1
for t in [0, 32, 66, 99]:
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
    print(X[0][ii])

plt.savefig("../doc/final/plots/nolearn3.png")


P = 0.01
Q = 0.01
K = 0.05
Size = 10000
T = 100
KT = 1000
FT = 1000
KD = 0.1
FD = 0.1
PI = 1
II = 5

X = sim_agent(
    p=P,
    q=Q,
    k=K,
    size=Size,
    t=100,
    knowledge_threshold=KT,
    fear_threshold=FT,
    knowledge_distance=KD,
    fear_distance=FD,
    prob_infect=PI,
    initial_infect=II,
)

figfull = plt.figure(figsize=(10, 10))
count = 1
for t in [0, 32, 66, 99]:
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
    print(X[0][ii])
plt.savefig("../doc/final/plots/yeslearn3.png")
