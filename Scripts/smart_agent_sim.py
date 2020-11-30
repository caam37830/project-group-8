# fmt: off
import sys
import os
import numpy as np
sys.path.append("../")  # lets us access sibling directory `sir`
from sir.smartagent import *
import matplotlib.pyplot as plt
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
T = 200
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
print(X[0])
plt.savefig("../doc/final/plots/nolearn.png")


P = 0.01
Q = 0.01
K = 0.05
Size = 10000
T = 200
KT = 100
FT = 100
KD = 0.15
FD = 0.15
PI = 1
II = 5

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
print(X[0])
plt.savefig("../doc/final/plots/yeslearn.png")
