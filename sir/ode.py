import numpy as np
from scipy.integrate import solve_ivp


class OdeSir:
    """
    A class for setting up an ODE simulation of the S,I,R model
    """

    def __init__(self, i0, N, b, k):
        """
        Pass the class i0, the initial infected fraction of the

        population, and n, the size of the population. Initializes

        s0, r0, S0, R0, and I0 based on these values. Also requires

        values for b, the interaction constant, and k, the rate of spread.
        """
        self.i0 = i0
        self.N = N
        self.s0 = 1 - i0
        self.r0 = 0
        self.I0 = i0 * N
        self.S0 = self.s0 * N
        self.R0 = 0
        self.S = self.S0
        self.R = self.R0
        self.I = self.I0
        self.i = self.i0
        self.r = self.r0
        self.s = self.s0
        self.b = b
        self.k = k
        self.func = lambda t, y: np.array(
            [-self.b * y[0] * y[2], self.k * y[2], self.b * y[0] * y[2] - self.k * y[2]])
        self.start = np.array([self.s0, self.r0, self.i0])
        self.infection = None

    def _give_start(self):
        """
        Returns the vector of initial conditions.
        """
        return self.start

    def _infect(self, t):
        """
        Solves system to simulate infection.

        Accepts t as the length of time to simulate.
        """
        time = (0, t)
        self.infection = solve_ivp(self.func, time, self.start)
        self.s = self.infection.y[0]
        self.r = self.infection.y[1]
        self.i = self.infection.y[2]
        self.S = self.s * self.N
        self.R = self.r * self.N
        self.I = self.i * self.N
        return self.infection

    def _reset(self):
        """
        Resets the model to the original s, i, r values.
        """
        self.i = self.i0
        self.r = self.r0
        self.s = self.s0
        self.I = self.I0
        self.S = self.S0
        self.R = self.R0

    def _give_values(self):
        """
        Returns s, i, r arrays.
        """
        return self.s, self.i, self.r

    def _give_final_values(self):
        """
        Returns final s, i, r values.
        """
        return self.s[-1], self.i[-1], self.r[-1]

    def _give_totals(self):
        """
        Returns final values of S, I, R values.
        """
        return self.S, self.I, self.R

    def _give_time(self):
        """
        Returns time vector.
        """
        return self.infection.t
