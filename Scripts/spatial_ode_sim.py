"""
Simulations for spatial ODE model
"""

import sys

sys.path.append("./sir/")
import ode
import matplotlib.pyplot as plt


def SimulateSpatial(i0, N, b, k, p, t, M=200, **kwargs):
    """
    Run a spatial ode simulation.
    """
    x = ode.SpatialSirOde(i0, N, b, k, p, M, **kwargs)
    x._infect(t)
    s, i, r = x._give_summary()
    T = x._give_time()
    return s, i, r, T


i0 = 0.10
N = 10000
b = 1
k = 0.05
p = [0.0000125, 0.000025, 0.00005, 0.000125]
t = 60

for n in p:
    s, i, r, T = SimulateSpatial(i0, N, b, k, n, t)
    print(f"S, p={n}: {s}")
    print(f"I, p={n}: {i}")
    print(f"R, p={n}: {r}")
    plt.plot(T, s, "b-", label="susceptible")
    plt.plot(T, i, "r-", label="infected")
    plt.plot(T, r, "g-", label="recovered")
    plt.legend()
    plt.xlabel("time")
    plt.ylabel("proportion")
    plt.title(f"Spatial model with p = {n}")
    plt.savefig(f"spatialp_{n}.png")
    plt.clf()

s, i, r, T = SimulationSpatial(i0, N, b, k, 0.000075, t, position="center")
print(f"S, center: {s}")
print(f"I, center: {i}")
print(f"R, center: {r}")
plt.plot(T, s, "b-", label="susceptible")
plt.plot(T, i, "r-", label="infected")
plt.plot(T, r, "g-", label="recovered")
plt.legend()
plt.xlabel("time")
plt.ylabel("proportion")
plt.title(f"Spatial model center")
plt.savefig(f"spatial_center.png")
plt.clf()

s, i, r, T = SimulationSpatial(i0, N, b, k, 0.000075, t, position="corner")
print(f"S, corner: {s}")
print(f"I, corner: {i}")
print(f"R, corner: {r}")
plt.plot(T, s, "b-", label="susceptible")
plt.plot(T, i, "r-", label="infected")
plt.plot(T, r, "g-", label="recovered")
plt.legend()
plt.xlabel("time")
plt.ylabel("proportion")
plt.title(f"Spatial model center")
plt.savefig(f"spatial_corner.png")
plt.clf()

s, i, r, T = SimulationSpatial(i0, N, b, k, 0.000075, t)
print(f"S, random: {s}")
print(f"I, random: {i}")
print(f"R, random: {r}")
plt.plot(T, s, "b-", label="susceptible")
plt.plot(T, i, "r-", label="infected")
plt.plot(T, r, "g-", label="recovered")
plt.legend()
plt.xlabel("time")
plt.ylabel("proportion")
plt.title(f"Spatial model center")
plt.savefig(f"spatial_random.png")
plt.clf()
