# fmt: off
import sys
import os
import numpy as np
sys.path.append("../")  # lets us access sibling directory `sir`
from sir.smartagent import *
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
# fmt: on


def sim_agent_center(
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
    number_infect=0,
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
    )
    infect_inds = [i + 1 for i in range(number_infect)]
    sim.exogenous_infect(indices=infect_inds)
    for ii in infect_inds:
        sim.agents[ii].pos[0] = 0.5 + (1 / 100) * np.random.randn(1)
        sim.agents[ii].pos[1] = 0.5 + (1 / 100) * np.random.randn(1)
    vals = sim.step_t_days(t)
    return vals


def sim_agent_corner(
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
    number_infect=0,
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
    )
    infect_inds = [i + 1 for i in range(number_infect)]
    sim.exogenous_infect(indices=infect_inds)
    for ii in infect_inds:
        sim.agents[ii].pos[0] = 0 + (1 / 100) * np.random.rand(1)
        sim.agents[ii].pos[1] = 0 + (1 / 100) * np.random.randn(1)
    vals = sim.step_t_days(t)
    return vals


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


P = [0.0025, 0.005, 0.01, 0.025]
Q = 0.01
K = 0.05
Size = 10000
T = 200
KT = 1
FT = 1
KD = 0
FD = 0
PI = 1
NI = 5


figfull = plt.figure(figsize=(10, 10))
count = 1
for p in P:
    X = sim_agent_center(
        p=p,
        q=Q,
        k=K,
        size=Size,
        t=T,
        knowledge_threshold=KT,
        fear_threshold=FT,
        knowledge_distance=KD,
        fear_distance=FD,
        prob_infect=PI,
        number_infect=NI,
    )
    plt.subplot(2, 2, count)
    plt.plot(X[0][:, 0], X[0][:, 1], "blue")
    plt.plot(X[0][:, 0], X[0][:, 2], "red")
    plt.plot(X[0][:, 0], X[0][:, 3], "green")
    plt.title("SIR plot with p = {}".format(p))
    count = count + 1
blue_patch = mpatches.Patch(color="blue", label="susceptible")
red_patch = mpatches.Patch(color="red", label="infected")
green_patch = mpatches.Patch(color="green", label="recovered")
figfull.legend(handles=[blue_patch, red_patch, green_patch])
figfull.suptitle("q = 0.01, k = 0.05, size = 10000, I0 = 5, start in center")
plt.savefig("../doc/final/plots/startmid.png")

P = 0.0075
Q = 0.01
K = 0.05
Size = 10000
T = 200
KT = 1
FT = 1
KD = 0
FD = 0
PI = 1
NI = 5

figfull = plt.figure(figsize=(10, 5))
X = sim_agent_center(
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
    number_infect=NI,
)
plt.subplot(1, 3, 1)
plt.plot(X[0][:, 0], X[0][:, 1], "blue")
plt.plot(X[0][:, 0], X[0][:, 2], "red")
plt.plot(X[0][:, 0], X[0][:, 3], "green")
plt.title("SIR plot starting in center")

X = sim_agent_corner(
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
    number_infect=NI,
)
plt.subplot(1, 3, 2)
plt.plot(X[0][:, 0], X[0][:, 1], "blue")
plt.plot(X[0][:, 0], X[0][:, 2], "red")
plt.plot(X[0][:, 0], X[0][:, 3], "green")
plt.title("SIR plot starting in corner")

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
    initial_infect=5,
)
plt.subplot(1, 3, 3)
plt.plot(X[0][:, 0], X[0][:, 1], "blue")
plt.plot(X[0][:, 0], X[0][:, 2], "red")
plt.plot(X[0][:, 0], X[0][:, 3], "green")
plt.title("SIR plot starting random")

blue_patch = mpatches.Patch(color="blue", label="susceptible")
red_patch = mpatches.Patch(color="red", label="infected")
green_patch = mpatches.Patch(color="green", label="recovered")
figfull.legend(handles=[blue_patch, red_patch, green_patch])
figfull.suptitle("p = 0.0075, q = 0.01, k = 0.05, size = 10000, I0 = 5")
plt.savefig("../doc/final/plots/startdiff.png")