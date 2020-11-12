import importlib

mod = importlib.import_module("project-group-8")
from mod.sir.agent.agent import *
from mod.sir.ode.sirODE import *
import matplotlib.pyplot as plt


def sim_ODE(i0, N, b, k, t):
    """
    returns array of arrays:
        - first sub array is S
        - second sub array is I
        - third sub array is R
    """
    sim = OdeSir(i0=i0, N=N, b=b, k=k)
    sim._infect(t=t)
    s, i, r = sim._give_values()
    vals = np.array([s, i, r])
    return vals


a = sim_ODE(i0=0.005, N=1000, b=1, k=0.05, t=50)
b = sim_ODE(i0=0.005, N=1000, b=1, k=0.1, t=50)
c = sim_ODE(i0=0.005, N=1000, b=1, k=0.15, t=50)
d = sim_ODE(i0=0.005, N=1000, b=1, k=0.2, t=50)
e = sim_ODE(i0=0.005, N=1000, b=1, k=0.25, t=50)
f = sim_ODE(i0=0.005, N=1000, b=1, k=0.3, t=50)
g = sim_ODE(i0=0.005, N=1000, b=1, k=0.35, t=50)
h = sim_ODE(i0=0.005, N=1000, b=1, k=0.4, t=50)


# phase diagram for varied k using agent ODE model
plt.figure(figsize=(12, 8))
plt.plot(a[0], a[1], "blue")
plt.plot(b[0], b[1], "red")
plt.plot(c[0], c[1], "green")
plt.plot(d[0], d[1], "yellow")
plt.plot(e[0], e[1], "purple")
plt.plot(f[0], f[1], "gray")
plt.plot(g[0], g[1], "pink")
plt.plot(h[0], h[1], "orange")
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
plt.title("S vs I with varied k (b = 1, population size = 1000, I0 = 5, t = 50)")
plt.savefig("PhaseKODE.png")

# S I R over time (b = 1, k = 0.05, population size = 1000, I0 = 5, t = 50) using ODE model
plt.figure(figsize=(12, 8))
plt.plot(range(len(a[0])), a[0], "blue")
plt.plot(range(len(a[0])), a[1], "red")
plt.plot(range(len(a[0])), a[2], "green")
plt.legend(["S", "I", "R"], loc="upper right")
plt.xlabel("time")
plt.ylabel("proportion of agents")
plt.title("S I R over time (b = 1, k = 0.05, population size = 1000, I0 = 5, t = 50)")
plt.savefig("K05ODE.png")

# S I R over time (b = 1, k = 0.40, population size = 1000, I0 = 5, t = 50) using ODE model
plt.figure(figsize=(12, 8))
plt.plot(range(len(h[0])), h[0], "blue")
plt.plot(range(len(h[0])), h[1], "red")
plt.plot(range(len(h[0])), h[2], "green")
plt.legend(["S", "I", "R"], loc="upper right")
plt.xlabel("time")
plt.ylabel("proportion of agents")
plt.title("S I R over time (b = 1, k = 0.40, population size = 1000, I0 = 5, t = 50)")
plt.savefig("K40ODE.png")


a = sim_ODE(i0=0.005, N=1000, b=1, k=0.15, t=50)
b = sim_ODE(i0=0.005, N=1000, b=2, k=0.15, t=50)
c = sim_ODE(i0=0.005, N=1000, b=3, k=0.15, t=50)
d = sim_ODE(i0=0.005, N=1000, b=4, k=0.15, t=50)
e = sim_ODE(i0=0.005, N=1000, b=5, k=0.15, t=50)
f = sim_ODE(i0=0.005, N=1000, b=10, k=0.15, t=50)
g = sim_ODE(i0=0.005, N=1000, b=20, k=0.15, t=50)
h = sim_ODE(i0=0.005, N=1000, b=50, k=0.15, t=50)


# phase diagram for varied b using agent ODE model
plt.figure(figsize=(12, 8))
plt.plot(a[0], a[1], "blue")
plt.plot(b[0], b[1], "red")
plt.plot(c[0], c[1], "green")
plt.plot(d[0], d[1], "yellow")
plt.plot(e[0], e[1], "purple")
plt.plot(f[0], f[1], "gray")
plt.plot(g[0], g[1], "pink")
plt.plot(h[0], h[1], "orange")
plt.legend(
    ["b=1", "b=2", "b=3", "b=4", "b=5", "b=10", "b=20", "b=50"], loc="upper right"
)
plt.xlabel("susceptible proportion")
plt.ylabel("infected proportion")
plt.title("S vs I with varied b (k = 0.15, population size = 1000, I0 = 5, t = 50)")
plt.savefig("PhaseKODE.png")

# S I R over time (b = 1, k = 0.15, population size = 1000, I0 = 5, t = 50) using ODE model
plt.figure(figsize=(12, 8))
plt.plot(range(len(a[0])), a[0], "blue")
plt.plot(range(len(a[0])), a[1], "red")
plt.plot(range(len(a[0])), a[2], "green")
plt.legend(["S", "I", "R"], loc="upper right")
plt.xlabel("time")
plt.ylabel("proportion of agents")
plt.title("S I R over time (b = 1, k = 0.15, population size = 1000, I0 = 5, t = 50)")
plt.savefig("K05ODE.png")

# S I R over time (b = 50, k = 0.15, population size = 1000, I0 = 5, t = 50) using ODE model
plt.figure(figsize=(12, 8))
plt.plot(range(len(h[0])), h[0], "blue")
plt.plot(range(len(h[0])), h[1], "red")
plt.plot(range(len(h[0])), h[2], "green")
plt.legend(["S", "I", "R"], loc="upper right")
plt.xlabel("time")
plt.ylabel("number of agents")
plt.title("S I R over time (b = 50, k = 0.10, population size = 1000, I0 = 5, t = 50)")
plt.savefig("K40ODE.png")


a = sim_ODE(i0=0.005, N=1000, b=1, k=0.25, t=50)
b = sim_ODE(i0=0.01, N=1000, b=1, k=0.25, t=50)
c = sim_ODE(i0=0.05, N=1000, b=1, k=0.25, t=50)
d = sim_ODE(i0=0.1, N=1000, b=1, k=0.25, t=50)
e = sim_ODE(i0=0.15, N=1000, b=1, k=0.25, t=50)
f = sim_ODE(i0=0.2, N=1000, b=1, k=0.25, t=50)
g = sim_ODE(i0=0.25, N=1000, b=1, k=0.25, t=50)
h = sim_ODE(i0=0.5, N=1000, b=1, k=0.25, t=50)


# phase diagram for varied I0 using agent ODE model
plt.figure(figsize=(12, 8))
plt.plot(a[0], a[1], "blue")
plt.plot(b[0], b[1], "red")
plt.plot(c[0], c[1], "green")
plt.plot(d[0], d[1], "yellow")
plt.plot(e[0], e[1], "purple")
plt.plot(f[0], f[1], "gray")
plt.plot(g[0], g[1], "pink")
plt.plot(h[0], h[1], "orange")
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
plt.xlabel("susceptible proportion")
plt.ylabel("infected proportion")
plt.title("S vs I with varied I0 (b = 1, k = 0.15, population size = 1000, t = 50)")
plt.savefig("PhaseI0ODE.png")

# S I R over time (b = 1, k = 0.15, population size = 1000, I0 = 5, t = 50) using ODE model
plt.figure(figsize=(12, 8))
plt.plot(range(len(a[0])), a[0], "blue")
plt.plot(range(len(a[0])), a[1], "red")
plt.plot(range(len(a[0])), a[2], "green")
plt.legend(["S", "I", "R"], loc="upper right")
plt.xlabel("time")
plt.ylabel("number of agents")
plt.title("S I R over time (b = 1, k = 0.25, population size = 1000, I0 = 5, t = 50)")
plt.savefig("I05ODE.png")

# S I R over time (b = 50, k = 0.15, population size = 1000, I0 = 5, t = 50) using ODE model
plt.figure(figsize=(12, 8))
plt.plot(range(len(h[0])), h[0], "blue")
plt.plot(range(len(h[0])), h[1], "red")
plt.plot(range(len(h[0])), h[2], "green")
plt.legend(["S", "I", "R"], loc="upper right")
plt.xlabel("time")
plt.ylabel("number of agents")
plt.title("S I R over time (b = 1, k = 0.25, population size = 1000, I0 = 500, t = 50)")
plt.savefig("I0500ODE.png")


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


a = sim_agent(b=1, k=0.05, size=1000, prob_infect=1, initial_infect=5, t=50)
b = sim_agent(b=1, k=0.1, size=1000, prob_infect=1, initial_infect=5, t=50)
c = sim_agent(b=1, k=0.15, size=1000, prob_infect=1, initial_infect=5, t=50)
d = sim_agent(b=1, k=0.2, size=1000, prob_infect=1, initial_infect=5, t=50)
e = sim_agent(b=1, k=0.25, size=1000, prob_infect=1, initial_infect=5, t=50)
f = sim_agent(b=1, k=0.3, size=1000, prob_infect=1, initial_infect=5, t=50)
g = sim_agent(b=1, k=0.35, size=1000, prob_infect=1, initial_infect=5, t=50)
h = sim_agent(b=1, k=0.40, size=1000, prob_infect=1, initial_infect=5, t=50)


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
    "S vs I with varied k (b = 1, population size = 1000, I0 = 5, t = 50, probability of infection = 1)"
)
plt.savefig("PhaseKAgent.png")

# S I R over time (b = 1, k = 0.05, population size = 1000, I0 = 5, t = 50, probability of infection = 1) using agent model
plt.figure(figsize=(12, 8))
plt.plot(a[:, 0], a[:, 1], "blue")
plt.plot(a[:, 0], a[:, 2], "red")
plt.plot(a[:, 0], a[:, 3], "green")
plt.legend(["S", "I", "R"], loc="upper right")
plt.xlabel("time")
plt.ylabel("number of agents")
plt.title(
    "S I R over time (b = 1, k = 0.05, population size = 1000, I0 = 5, t = 50, probability of infection = 1)"
)
plt.savefig("K05Agent.png")

# S I R over time (b = 1, k = 0.40, population size = 1000, I0 = 5, t = 50, probability of infection = 1 using agent model
plt.figure(figsize=(12, 8))
plt.plot(h[:, 0], h[:, 1], "blue")
plt.plot(h[:, 0], h[:, 2], "red")
plt.plot(h[:, 0], h[:, 3], "green")
plt.legend(["S", "I", "R"], loc="upper right")
plt.xlabel("time")
plt.ylabel("number of agents")
plt.title(
    "S I R over time (b = 1, k = 0.40, population size = 1000, I0 = 5, t = 50, probability of infection = 1"
)
plt.savefig("K40Agent.png")


a = sim_agent(b=1, k=0.15, size=1000, prob_infect=1, initial_infect=5, t=50)
b = sim_agent(b=2, k=0.15, size=1000, prob_infect=1, initial_infect=5, t=50)
c = sim_agent(b=3, k=0.15, size=1000, prob_infect=1, initial_infect=5, t=50)
d = sim_agent(b=4, k=0.15, size=1000, prob_infect=1, initial_infect=5, t=50)
e = sim_agent(b=5, k=0.15, size=1000, prob_infect=1, initial_infect=5, t=50)
f = sim_agent(b=10, k=0.15, size=1000, prob_infect=1, initial_infect=5, t=50)
g = sim_agent(b=20, k=0.15, size=1000, prob_infect=1, initial_infect=5, t=50)
h = sim_agent(b=50, k=0.15, size=1000, prob_infect=1, initial_infect=5, t=50)

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
    "S vs I with varied b (k = 0.15, population size = 1000, I0 = 5, t = 50, probability of infection = 1)"
)
plt.savefig("PhaseBAgent.png")

# S I R over time (b = 1, k = 0.15, population size = 1000, I0 = 5, t = 50, probability of infection = 1) using agent model
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
    "S I R over time (b = 1, k = 0.15, population size = 1000, I0 = 5, t = 50, probability of infection = 1)"
)
plt.savefig("b1Agent.png")

# S I R over time (b = 50, k = 0.15, population size = 1000, I0 = 5, t = 50, probability of infection = 1) using agent model
plt.figure(figsize=(12, 8))
plt.plot(h[:, 0], h[:, 1], "blue")
plt.plot(h[:, 0], h[:, 2], "red")
plt.plot(h[:, 0], h[:, 3], "green")
plt.legend(["S", "I", "R"], loc="upper right")
plt.xlabel("time")
plt.ylabel("number of agents")
plt.title(
    "S I R over time (b = 50, k = 0.15, population size = 1000, I0 = 5, t = 50, probability of infection = 1)"
)
plt.savefig("b50Agent.png")


a = sim_agent(b=1, k=0.25, size=1000, prob_infect=1, initial_infect=5, t=50)
b = sim_agent(b=1, k=0.25, size=1000, prob_infect=1, initial_infect=10, t=50)
c = sim_agent(b=1, k=0.25, size=1000, prob_infect=1, initial_infect=50, t=50)
d = sim_agent(b=1, k=0.25, size=1000, prob_infect=1, initial_infect=100, t=50)
e = sim_agent(b=1, k=0.25, size=1000, prob_infect=1, initial_infect=150, t=50)
f = sim_agent(b=1, k=0.25, size=1000, prob_infect=1, initial_infect=200, t=50)
g = sim_agent(b=1, k=0.25, size=1000, prob_infect=1, initial_infect=250, t=50)
h = sim_agent(b=1, k=0.25, size=1000, prob_infect=1, initial_infect=500, t=50)

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
    "S vs I with varied I0 (b = 1, k = 0.15, population size = 1000, t = 50, probability of infection = 1)"
)
plt.savefig("PhaseI0Agent.png")

# S I R over time (b = 1, k = 0.25, population size = 1000, I0 = 5, t = 50, probability of infection = 1) using agent model
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
    "S I R over time (b = 1, k = 0.25, population size = 1000, I0 = 5, t = 50, probability of infection = 1)"
)
plt.savefig("I05Agent.png")

# S I R over time (b = 1, k = 0.25, population size = 1000, I0 = 500, t = 50, probability of infection = 1) using agent model
plt.figure(figsize=(12, 8))
plt.plot(h[:, 0], h[:, 1], "blue")
plt.plot(h[:, 0], h[:, 2], "red")
plt.plot(h[:, 0], h[:, 3], "green")
plt.legend(["S", "I", "R"], loc="upper right")
plt.xlabel("time")
plt.ylabel("number of agents")
plt.title(
    "S I R over time (b = 1, k = 0.25, population size = 1000, I0 = 500, t = 50, probability of infection = 1)"
)
plt.savefig("I0500Agent.png")
