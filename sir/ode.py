"""
Definition of the `OdeSir` class
"""

import numpy as np
from scipy.integrate import solve_ivp
from scipy.sparse.csgraph import laplacian
from scipy.integrate import solve_bvp


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
            [-self.b * y[0] * y[2], self.k * y[2],
                self.b * y[0] * y[2] - self.k * y[2]]
        )
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


class SpatialSirOde(OdeSir):
    """
    The SIR method solved with ODEs including spatial components.
    """

    def __init__(self, i0, N, b, k, p, position=None, M=200):
        """
        Initialize the class.
        """
        super(SpatialSirOde, self).__init__(i0, N, b, k)
        self.M = M
        self.p = p
        self.S0 = (1 - i0) * self.N
        self.n = round(i0 * self.M)
        self.i0 = np.zeros((self.M, self.M))
        self.s0 = np.ones((self.M, self.M))
        if position == None:
            self.ind_i = np.random.choice(self.M, self.n)
            self.ind_j = np.random.choice(self.M, self.n)
            for ind in self.ind_i:
                for j in self.ind_j:
                    self.i0[ind, j] = 1
                    self.s0[ind, j] = 0
        elif position == 'corner':
            ind_i = np.arange(self.n)
            for ind in ind_i:
                for j in ind_i:
                    self.i0[ind, j] = 1
                    self.s0[ind, j] = 0
        elif position == 'center':
            center = round(self.M / 2)
            start = center - round((self.n) / 2)
            end = center + round((self.n) / 2)
            ind_i = np.arange(start, end)
            for ind in ind_i:
                for j in ind_i:
                    self.i0[ind, j] = 1
                    self.s0[ind, j] = 0
        self.r0 = np.zeros((self.M, self.M))
        self.i = self.i0
        self.s = self.s0
        self.r = self.r0
        self.weight = (1 / self.M) ** 2
        self.y0 = np.array([self.s0, self.r0, self.i0])
        self.x = np.linspace(0, self.N, self.M)

        self.bc = lambda ya, yb: np.array([ya[0], yb[0]])

        def fun(t, y): return np.array(
            [-self.b * y[0] * y[2] + self.p * self.weight * laplacian(y[0]), self.k * y[2] + self.p * self.weight * y[1],
                self.b * y[0] * y[2] - self.k * y[2] + self.p * self.weight * y[2]])
        self.fun = np.vectorize(fun)

    def _infect(self):
        """
        Solves system to simulate infection.
        """
        self.infection = solve_bvp(self.fun, self.bc, self.x, self.y0)
        self.s = self.infection.y[0:, ]
        self.r = self.infection.y[1:, ]
        self.i = self.infection.y[2:, ]
        self.S = self.s * self.N
        self.R = self.r * self.N
        self.I = self.i * self.N
        return self.infection

    def _give_position(self):
        """
        Return the x values from the spatially solved system.
        """
        return self.infection.x[0:, ], self.infection.x[1:, ], self.infection.x[2:, ]


class ODEReinfection(OdeSir):
    """
    The SIR model solved using ODEs with reinfection 

    and death rate parameters.
    """

    def __init__(self, i0, N, b, k, g, e):
        """
        Initilize the system. New parameters g and e

        where g corresponds to the reinfection rate and e 

        corresponds to the death rate.
        """
        super(ODEReinfection, self).__init__(i0, N, b, k)
        self.e = e
        self.g = g
        self.d0 = 0
        self.d = self.d0
        self.D0 = 0
        self.D = self.D0
        self.func = lambda t, y: np.array(
            [-self.b * y[0] * y[2] + self.g * y[1], self.k * y[2] - self.g * y[1],
                self.b * y[0] * y[2] - self.k * y[2] - self.e * y[2], self.e * y[2]]
        )
        self.start = np.array([self.s0, self.r0, self.i0, self.d0])

    def _infect(self, t):
        """
        Update infection routine to also produce death rate.
        """
        super(ODEReinfection, self)._infect(t)
        self.d = self.infection.y[3]
        self.D = self.d * self.N
        return self.infection

    def _reset(self):
        """
        Resets the model to the original s, i, r, d values.
        """
        super(ODEReinfection, self)._reset()
        self.D = self.D0
        self.d = self.d0

    def _give_values(self):
        """
        Returns s, i, r, d arrays.
        """
        return self.s, self.i, self.r, self.d

    def _give_final_values(self):
        """
        Returns final s, i, r, d values.
        """
        return self.s[-1], self.i[-1], self.r[-1], self.d[-1]

    def _give_totals(self):
        """
        Returns final values of S, I, R, D values.
        """
        return self.S, self.I, self.R, self.D
