"""
A very useful docstring
"""
# fmt: off
import sys
import os
sys.path.append("../")  # lets us access sibling directory `sir`
from sir.ode import *
from sir.agent import *
import matplotlib.pyplot as plt
# fmt: on

# parameters
Population = 10000
initial_infected = 50
initial_proportion = initial_infected / Population
time_span = 60


def sim_ODE(i0, N, b, k, t):
    """
    returns array of arrays:
        - first sub array is T
        - second sub array is S
        - third sub array is I
        - fourthe sub array is R
    """
    sim = OdeSir(i0=i0, N=N, b=b, k=k)
    sim._infect(t=t)
    s, i, r = sim._give_values()
    t = sim._give_time()
    vals = np.array([t, s, i, r])
    return vals


a = sim_ODE(i0=initial_proportion, N=Population, b=1, k=0.05, t=time_span)
b = sim_ODE(i0=initial_proportion, N=Population, b=1, k=0.1, t=time_span)
c = sim_ODE(i0=initial_proportion, N=Population, b=1, k=0.15, t=time_span)
d = sim_ODE(i0=initial_proportion, N=Population, b=1, k=0.2, t=time_span)
e = sim_ODE(i0=initial_proportion, N=Population, b=1, k=0.25, t=time_span)
f = sim_ODE(i0=initial_proportion, N=Population, b=1, k=0.3, t=time_span)
g = sim_ODE(i0=initial_proportion, N=Population, b=1, k=0.35, t=time_span)
h = sim_ODE(i0=initial_proportion, N=Population, b=1, k=0.4, t=time_span)

# phase diagram for varied k using agent ODE model
plt.figure(figsize=(12, 8))
plt.plot(a[1], a[2], "blue")
plt.plot(b[1], b[2], "red")
plt.plot(c[1], c[2], "green")
plt.plot(d[1], d[2], "yellow")
plt.plot(e[1], e[2], "purple")
plt.plot(f[1], f[2], "gray")
plt.plot(g[1], g[2], "pink")
plt.plot(h[1], h[2], "orange")
plt.legend(
    [
        "k=0.05",
        "k=0.1",
        "k=0.15",
        "k=0.2",
        "k=0.25",
        "k=0.3",
        "k=0.35",
        "k=0.4",
    ],
    loc="upper right",
)
plt.xlabel("susceptible proportion")
plt.ylabel("infected proportion")
plt.title(
    "S vs I with varied k (b = 1, population size = {}, I0 = {}, t = {})".format(
        Population, initial_infected, time_span
    )
)
plt.savefig("../doc/checkpoint/plots/PhasekODE.png")

# S I R over time k = 0.05 using ODE model
plt.figure(figsize=(12, 8))
plt.plot(a[0], a[1], "blue")
plt.plot(a[0], a[2], "red")
plt.plot(a[0], a[3], "green")
plt.legend(["S", "I", "R"], loc="upper right")
plt.xlabel("time")
plt.ylabel("proportion of agents")
plt.title(
    "S I R over time (b = 1, k = 0.05, population size = {}, I0 = {}, t = {})".format(
        Population, initial_infected, time_span
    )
)
plt.savefig("../doc/checkpoint/plots/k05ODE.png")

# S I R over time k = 0.40 using ODE model
plt.figure(figsize=(12, 8))
plt.plot(h[0], h[1], "blue")
plt.plot(h[0], h[2], "red")
plt.plot(h[0], h[3], "green")
plt.legend(["S", "I", "R"], loc="upper right")
plt.xlabel("time")
plt.ylabel("proportion of agents")
plt.title(
    "S I R over time (b = 1, k = 0.40, population size = {}, I0 = {}, t = {})".format(
        Population, initial_infected, time_span
    )
)
plt.savefig("../doc/checkpoint/plots/k40ODE.png")


a = sim_ODE(i0=initial_proportion, N=Population, b=1, k=0.25, t=time_span)
b = sim_ODE(i0=initial_proportion, N=Population, b=2, k=0.25, t=time_span)
c = sim_ODE(i0=initial_proportion, N=Population, b=3, k=0.25, t=time_span)
d = sim_ODE(i0=initial_proportion, N=Population, b=4, k=0.25, t=time_span)
e = sim_ODE(i0=initial_proportion, N=Population, b=5, k=0.25, t=time_span)
f = sim_ODE(i0=initial_proportion, N=Population, b=10, k=0.25, t=time_span)
g = sim_ODE(i0=initial_proportion, N=Population, b=20, k=0.25, t=time_span)
h = sim_ODE(i0=initial_proportion, N=Population, b=50, k=0.25, t=time_span)


# phase diagram for varied b using agent ODE model
plt.figure(figsize=(12, 8))
plt.plot(a[1], a[2], "blue")
plt.plot(b[1], b[2], "red")
plt.plot(c[1], c[2], "green")
plt.plot(d[1], d[2], "yellow")
plt.plot(e[1], e[2], "purple")
plt.plot(f[1], f[2], "gray")
plt.plot(g[1], g[2], "pink")
plt.plot(h[1], h[2], "orange")
plt.legend(
    ["b=1", "b=2", "b=3", "b=4", "b=5", "b=10", "b=20", "b=50"], loc="upper right"
)
plt.xlabel("susceptible proportion")
plt.ylabel("infected proportion")
plt.title(
    "S vs I with varied b (k = 0.25, population size = {}, I0 = {}, t = {})".format(
        Population, initial_infected, time_span
    )
)
plt.savefig("../doc/checkpoint/plots/PhasebODE.png")

# S I R over time b = 1 using ODE model
plt.figure(figsize=(12, 8))
plt.plot(a[0], a[1], "blue")
plt.plot(a[0], a[2], "red")
plt.plot(a[0], a[3], "green")
plt.legend(["S", "I", "R"], loc="upper right")
plt.xlabel("time")
plt.ylabel("proportion of agents")
plt.title(
    "S I R over time (b = 1, k = 0.25, population size = {}, I0 = {}, t = {})".format(
        Population, initial_infected, time_span
    )
)
plt.savefig("../doc/checkpoint/plots/b1ODE.png")

# S I R over time b = 50 using ODE model
plt.figure(figsize=(12, 8))
plt.plot(h[0], h[1], "blue")
plt.plot(h[0], h[2], "red")
plt.plot(h[0], h[3], "green")
plt.legend(["S", "I", "R"], loc="upper right")
plt.xlabel("time")
plt.ylabel("proportion of agents")
plt.title(
    "S I R over time (b = 50, k = 0.25, population size = {}, I0 = {}, t = {})".format(
        Population, initial_infected, time_span
    )
)
plt.savefig("../doc/checkpoint/plots/b50ODE.png")


a = sim_ODE(i0=initial_proportion, N=Population, b=1, k=0.25, t=time_span)
b = sim_ODE(i0=initial_proportion * 2, N=Population, b=1, k=0.25, t=time_span)
c = sim_ODE(i0=initial_proportion * 3, N=Population, b=1, k=0.25, t=time_span)
d = sim_ODE(i0=initial_proportion * 4, N=Population, b=1, k=0.25, t=time_span)
e = sim_ODE(i0=initial_proportion * 5, N=Population, b=1, k=0.25, t=time_span)
f = sim_ODE(i0=initial_proportion * 10, N=Population, b=1, k=0.25, t=time_span)
g = sim_ODE(i0=initial_proportion * 20, N=Population, b=1, k=0.25, t=time_span)
h = sim_ODE(i0=initial_proportion * 25, N=Population, b=1, k=0.25, t=time_span)


# phase diagram for varied I0 using agent ODE model
plt.figure(figsize=(12, 8))
plt.plot(a[1], a[2], "blue")
plt.plot(b[1], b[2], "red")
plt.plot(c[1], c[2], "green")
plt.plot(d[1], d[2], "yellow")
plt.plot(e[1], e[2], "purple")
plt.plot(f[1], f[2], "gray")
plt.plot(g[1], g[2], "pink")
plt.plot(h[1], h[2], "orange")
plt.legend(
    [
        "I0={}".format(initial_infected),
        "I0={}".format(initial_infected * 2),
        "I0={}".format(initial_infected * 3),
        "I0={}".format(initial_infected * 4),
        "I0={}".format(initial_infected * 5),
        "I0={}".format(initial_infected * 10),
        "I0={}".format(initial_infected * 20),
        "I0={}".format(initial_infected * 25),
    ],
    loc="upper right",
)
plt.xlabel("susceptible proportion")
plt.ylabel("infected proportion")
plt.title(
    "S vs I with varied I0 (b = 1, k = 0.25, population size = {}, t = {})".format(
        Population, time_span
    )
)
plt.savefig("../doc/checkpoint/plots/PhaseI0ODE.png")

# S I R over time I0 = initial_infected using ODE model
plt.figure(figsize=(12, 8))
plt.plot(a[0], a[1], "blue")
plt.plot(a[0], a[2], "red")
plt.plot(a[0], a[3], "green")
plt.legend(["S", "I", "R"], loc="upper right")
plt.xlabel("time")
plt.ylabel("proportion of agents")
plt.title(
    "S I R over time (b = 1, k = 0.25, population size = {}, I0 = {}, t = {})".format(
        Population, initial_infected, time_span
    )
)
plt.savefig("../doc/checkpoint/plots/I01ODE.png")

# S I R over time  I0 = initial_infected*25 using ODE model
plt.figure(figsize=(12, 8))
plt.plot(h[0], h[1], "blue")
plt.plot(h[0], h[2], "red")
plt.plot(h[0], h[3], "green")
plt.legend(["S", "I", "R"], loc="upper right")
plt.xlabel("time")
plt.ylabel("proportion of agents")
plt.title(
    "S I R over time (b = 1, k = 0.25, population size = {}, I0 = {}, t = {})".format(
        Population, initial_infected * 25, time_span
    )
)
plt.savefig("../doc/checkpoint/plots/I0250ODE.png")


def sim_agent(b, k, size, prob_infect, initial_infect, t):
    """
    returns `days` by `4` numpy array, with columns ...
        - day number
        - number susceptible
        - number infected
        - number recovered
    """
    sim = SIRModel(
        b=b, k=k, size=size, prob_infect=prob_infect, initial_infect=initial_infect
    )
    vals = sim.step_t_days(t)
    return vals


a = sim_agent(
    b=1,
    k=0.05,
    size=Population,
    prob_infect=1,
    initial_infect=initial_infected,
    t=time_span,
)
b = sim_agent(
    b=1,
    k=0.1,
    size=Population,
    prob_infect=1,
    initial_infect=initial_infected,
    t=time_span,
)
c = sim_agent(
    b=1,
    k=0.15,
    size=Population,
    prob_infect=1,
    initial_infect=initial_infected,
    t=time_span,
)
d = sim_agent(
    b=1,
    k=0.2,
    size=Population,
    prob_infect=1,
    initial_infect=initial_infected,
    t=time_span,
)
e = sim_agent(
    b=1,
    k=0.25,
    size=Population,
    prob_infect=1,
    initial_infect=initial_infected,
    t=time_span,
)
f = sim_agent(
    b=1,
    k=0.3,
    size=Population,
    prob_infect=1,
    initial_infect=initial_infected,
    t=time_span,
)
g = sim_agent(
    b=1,
    k=0.35,
    size=Population,
    prob_infect=1,
    initial_infect=initial_infected,
    t=time_span,
)
h = sim_agent(
    b=1,
    k=0.40,
    size=Population,
    prob_infect=1,
    initial_infect=initial_infected,
    t=time_span,
)


# phase diagram for varied k using agent model
plt.figure(figsize=(12, 8))
plt.plot(a[:, 1], a[:, 2], "blue")
plt.plot(b[:, 1], b[:, 2], "red")
plt.plot(c[:, 1], c[:, 2], "green")
plt.plot(d[:, 1], d[:, 2], "yellow")
plt.plot(e[:, 1], e[:, 2], "purple")
plt.plot(f[:, 1], f[:, 2], "gray")
plt.plot(g[:, 1], g[:, 2], "pink")
plt.plot(h[:, 1], h[:, 2], "orange")
plt.legend(
    [
        "k=0.05",
        "k=0.1",
        "k=0.15",
        "k=0.2",
        "k=0.25",
        "k=0.3",
        "k=0.35",
        "k=0.4",
    ],
    loc="upper right",
)
plt.xlabel("susceptible")
plt.ylabel("infected")
plt.title(
    "S vs I with varied k (b = 1, population size = {}, I0 = {}, t = {}, probability of infection = 1)".format(
        Population, initial_infected, time_span
    )
)
plt.savefig("../doc/checkpoint/plots/PhasekAgent.png")

# S I R over time k = 0.05 using agent model
plt.figure(figsize=(12, 8))
plt.plot(a[:, 0], a[:, 1], "blue")
plt.plot(a[:, 0], a[:, 2], "red")
plt.plot(a[:, 0], a[:, 3], "green")
plt.legend(["S", "I", "R"], loc="upper right")
plt.xlabel("time")
plt.ylabel("number of agents")
plt.title(
    "S I R over time (b = 1, k = 0.05, population size = {}, I0 = {}, t = {}, probability of infection = 1)".format(
        Population, initial_infected, time_span
    )
)
plt.savefig("../doc/checkpoint/plots/k05Agent.png")

# S I R over time k = 0.40 using agent model
plt.figure(figsize=(12, 8))
plt.plot(h[:, 0], h[:, 1], "blue")
plt.plot(h[:, 0], h[:, 2], "red")
plt.plot(h[:, 0], h[:, 3], "green")
plt.legend(["S", "I", "R"], loc="upper right")
plt.xlabel("time")
plt.ylabel("number of agents")
plt.title(
    "S I R over time (b = 1, k = 0.40, population size = {}, I0 = {}, t = {}, probability of infection = 1".format(
        Population, initial_infected, time_span
    )
)
plt.savefig("../doc/checkpoint/plots/k40Agent.png")

# S I R over time k = 0.30 using agent model
plt.figure(figsize=(12, 8))
plt.plot(f[:, 0], f[:, 1], "blue")
plt.plot(f[:, 0], f[:, 2], "red")
plt.plot(f[:, 0], f[:, 3], "green")
plt.legend(["S", "I", "R"], loc="upper right")
plt.xlabel("time")
plt.ylabel("number of agents")
plt.title(
    "S I R over time (b = 1, k = 0.30, population size = {}, I0 = {}, t = {}, probability of infection = 1".format(
        Population, initial_infected, time_span
    )
)
plt.savefig("../doc/checkpoint/plots/k30Agent.png")

# S I R over time k = 0.35, using agent model
plt.figure(figsize=(12, 8))
plt.plot(g[:, 0], g[:, 1], "blue")
plt.plot(g[:, 0], g[:, 2], "red")
plt.plot(g[:, 0], g[:, 3], "green")
plt.legend(["S", "I", "R"], loc="upper right")
plt.xlabel("time")
plt.ylabel("number of agents")
plt.title(
    "S I R over time (b = 1, k = 0.35, population size = {}, I0 = {}, t = {}, probability of infection = 1".format(
        Population, initial_infected, time_span
    )
)
plt.savefig("../doc/checkpoint/plots/k35Agent.png")


a = sim_agent(
    b=1,
    k=0.25,
    size=Population,
    prob_infect=1,
    initial_infect=initial_infected,
    t=time_span,
)
b = sim_agent(
    b=2,
    k=0.25,
    size=Population,
    prob_infect=1,
    initial_infect=initial_infected,
    t=time_span,
)
c = sim_agent(
    b=3,
    k=0.25,
    size=Population,
    prob_infect=1,
    initial_infect=initial_infected,
    t=time_span,
)
d = sim_agent(
    b=4,
    k=0.25,
    size=Population,
    prob_infect=1,
    initial_infect=initial_infected,
    t=time_span,
)
e = sim_agent(
    b=5,
    k=0.25,
    size=Population,
    prob_infect=1,
    initial_infect=initial_infected,
    t=time_span,
)
f = sim_agent(
    b=10,
    k=0.25,
    size=Population,
    prob_infect=1,
    initial_infect=initial_infected,
    t=time_span,
)
g = sim_agent(
    b=20,
    k=0.25,
    size=Population,
    prob_infect=1,
    initial_infect=initial_infected,
    t=time_span,
)
h = sim_agent(
    b=50,
    k=0.25,
    size=Population,
    prob_infect=1,
    initial_infect=initial_infected,
    t=time_span,
)

# phase diagram for varied b using agent model
plt.figure(figsize=(12, 8))
plt.plot(a[:, 1], a[:, 2], "blue")
plt.plot(b[:, 1], b[:, 2], "red")
plt.plot(c[:, 1], c[:, 2], "green")
plt.plot(d[:, 1], d[:, 2], "yellow")
plt.plot(e[:, 1], e[:, 2], "purple")
plt.plot(f[:, 1], f[:, 2], "gray")
plt.plot(g[:, 1], g[:, 2], "pink")
plt.plot(h[:, 1], h[:, 2], "orange")
plt.legend(
    ["b=1", "b=2", "b=3", "b=4", "b=5", "b=10", "b=20", "b=50"], loc="upper right"
)
plt.xlabel("susceptible")
plt.ylabel("infected")
plt.title(
    "S vs I with varied b (k = 0.25, population size = {}, I0 = {}, t = {}, probability of infection = 1)".format(
        Population, initial_infected, time_span
    )
)
plt.savefig("../doc/checkpoint/plots/PhasebAgent.png")

# S I R over time b = 1 using agent model
plt.figure(figsize=(12, 8))
plt.plot(a[:, 0], a[:, 1], "blue")
plt.plot(a[:, 0], a[:, 2], "red")
plt.plot(a[:, 0], a[:, 3], "green")
plt.legend(
    ["S", "I", "R"],
    loc="upper right",
)
plt.xlabel("time")
plt.ylabel("number of agents")
plt.title(
    "S I R over time (b = 1, k = 0.25, population size = {}, I0 = {}, t = {}, probability of infection = 1)".format(
        Population, initial_infected, time_span
    )
)
plt.savefig("../doc/checkpoint/plots/b1Agent.png")

# S I R over time b = 50 using agent model
plt.figure(figsize=(12, 8))
plt.plot(h[:, 0], h[:, 1], "blue")
plt.plot(h[:, 0], h[:, 2], "red")
plt.plot(h[:, 0], h[:, 3], "green")
plt.legend(["S", "I", "R"], loc="upper right")
plt.xlabel("time")
plt.ylabel("number of agents")
plt.title(
    "S I R over time (b = 50, k = 0.25, population size = {}, I0 = {}, t = {}, probability of infection = 1)".format(
        Population, initial_infected, time_span
    )
)
plt.savefig("../doc/checkpoint/plots/b50Agent.png")


a = sim_agent(
    b=1,
    k=0.25,
    size=Population,
    prob_infect=1,
    initial_infect=initial_infected,
    t=time_span,
)
b = sim_agent(
    b=1,
    k=0.25,
    size=Population,
    prob_infect=1,
    initial_infect=initial_infected * 2,
    t=time_span,
)
c = sim_agent(
    b=1,
    k=0.25,
    size=Population,
    prob_infect=1,
    initial_infect=initial_infected * 3,
    t=time_span,
)
d = sim_agent(
    b=1,
    k=0.25,
    size=Population,
    prob_infect=1,
    initial_infect=initial_infected * 4,
    t=time_span,
)
e = sim_agent(
    b=1,
    k=0.25,
    size=Population,
    prob_infect=1,
    initial_infect=initial_infected * 5,
    t=time_span,
)
f = sim_agent(
    b=1,
    k=0.25,
    size=Population,
    prob_infect=1,
    initial_infect=initial_infected * 10,
    t=time_span,
)
g = sim_agent(
    b=1,
    k=0.25,
    size=Population,
    prob_infect=1,
    initial_infect=initial_infected * 20,
    t=time_span,
)
h = sim_agent(
    b=1,
    k=0.25,
    size=Population,
    prob_infect=1,
    initial_infect=initial_infected * 25,
    t=time_span,
)

# phase diagram for varied initial infected using agent model
plt.figure(figsize=(12, 8))
plt.plot(a[:, 1], a[:, 2], "blue")
plt.plot(b[:, 1], b[:, 2], "red")
plt.plot(c[:, 1], c[:, 2], "green")
plt.plot(d[:, 1], d[:, 2], "yellow")
plt.plot(e[:, 1], e[:, 2], "purple")
plt.plot(f[:, 1], f[:, 2], "gray")
plt.plot(g[:, 1], g[:, 2], "pink")
plt.plot(h[:, 1], h[:, 2], "orange")
plt.legend(
    [
        "I0=5",
        "I0=10",
        "I0=50",
        "I0=100",
        "I0=150",
        "I0=200",
        "I0=250",
        "I0=500",
    ],
    loc="upper right",
)
plt.xlabel("susceptible")
plt.ylabel("infected")
plt.title(
    "S vs I with varied I0 (b = 1, k = 0.25, population size = {}, t = {}, probability of infection = 1)".format(
        Population, time_span
    )
)
plt.savefig("../doc/checkpoint/plots/PhaseI0Agent.png")

# S I R over time I0 = initial_infected using agent model
plt.figure(figsize=(12, 8))
plt.plot(a[:, 0], a[:, 1], "blue")
plt.plot(a[:, 0], a[:, 2], "red")
plt.plot(a[:, 0], a[:, 3], "green")
plt.legend(
    ["S", "I", "R"],
    loc="upper right",
)
plt.xlabel("time")
plt.ylabel("number of agents")
plt.title(
    "S I R over time (b = 1, k = 0.25, population size = {}, I0 = {}, t = {}, probability of infection = 1)".format(
        Population, initial_infected, time_span
    )
)
plt.savefig("../doc/checkpoint/plots/I01Agent.png")

# S I R over time I0 = initial_infected*25 using agent model
plt.figure(figsize=(12, 8))
plt.plot(h[:, 0], h[:, 1], "blue")
plt.plot(h[:, 0], h[:, 2], "red")
plt.plot(h[:, 0], h[:, 3], "green")
plt.legend(["S", "I", "R"], loc="upper right")
plt.xlabel("time")
plt.ylabel("number of agents")
plt.title(
    "S I R over time (b = 1, k = 0.25, population size = {}, I0 = {}, t = {}, probability of infection = 1)".format(
        Population, initial_infected * 25, time_span
    )
)
plt.savefig("../doc/checkpoint/plots/I025Agent.png")
