from sir.agent.agent import *
from sir.ode.sirODE import *
import matplotlib.pyplot as plt


def sim_getphase_ODE(i0, N, b, k, t):
    sim = OdeSir(i0=i0, N=N, b=b, k=k)
    sim._infect(t=t)
    s, i, r = sim._give_values()
    vals = np.array([s, i, r])
    return vals


x = sim_getphase_ODE(i0=0.1, N=10000, b=1, k=0.0001, t=5)
print(x[0])
print(x[1])

plt.figure()
plt.plot(x[0], x[1], "red")
plt.show()