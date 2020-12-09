import sys

sys.path.append("./sir/")
import reinfect_ode
import matplotlib.pyplot as plt

e = 0.005
b = 1
k = 0.25
i0 = 0.1
N = 10000
T = 60


def SimulateReinfection(i0, N, b, k, g, e, t):
    """
    Run a simulation of reinfection.
    """
    x = reinfect_ode.ODEReinfection(i0, N, b, k, g, e)
    x._infect(t)
    time = x._give_time()
    s, i, r, d = x._give_values()
    return s, i, r, d, time


g = [0.05, 0.10, 0.15]

for n in g:
    s, i, r, d, t = SimulateReinfection(i0, N, b, k, n, e, T)
    print(f"S, g={n}: {s}")
    print(f"I, g={n}: {i}")
    print(f"R, g={n}: {r}")
    print(f"D, g={n}: {d}")
    plt.plot(t, s, "b-", label="susceptible")
    plt.plot(t, i, "r-", label="infected")
    plt.plot(t, r, "g-", label="recovered")
    plt.plot(t, d, "k-", label="dead")
    plt.legend()
    plt.xlabel("time")
    plt.ylabel("proportion")
    plt.title(f"Reinfection with g = {n}")
    plt.savefig(f"reinfectg_{n}.png")
    plt.clf()
