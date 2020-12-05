"""
Definition of the `OdeSir` class
"""

import numpy as np
from scipy.integrate import solve_ivp
from scipy.sparse.csgraph import laplacian
from scipy.integrate import solve_bvp
import scipy.sparse as sparse
import scipy.sparse.linalg as spla
import math


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
        self.n = math.ceil(i0 * (self.M ** 2))
        self.i0 = np.zeros((self.M, self.M))
        self.s0 = np.ones((self.M, self.M))
        if position == None:
            self.ind_i = np.random.choice(self.M ** 2, self.n)
            self.i0 = np.ravel(self.i0)
            self.s0 = np.ravel(self.s0)
            for ind in self.ind_i:
                self.i0[ind] = 1
                self.s0[ind] = 0
            self.i0 = np.reshape(self.i0, (self.M, self.M))
            self.s0 = np.reshape(self.s0, (self.M, self.M))
        elif position == 'corner':
            ind_i = np.arange(self.n)
            self.i0 = np.ravel(self.i0)
            self.s0 = np.ravel(self.s0)
            for ind in ind_i:
                self.i0[ind] = 1
                self.s0[ind] = 0
            self.i0 = np.reshape(self.i0, (self.M, self.M))
            self.s0 = np.reshape(self.s0, (self.M, self.M))
        elif position == 'center':
            center = round((self.M ** 2) / 2)
            start = center - round((self.n) / 2)
            end = center + round((self.n) / 2)
            ind_i = np.arange(start, end)
            self.i0 = np.ravel(self.i0)
            self.s0 = np.ravel(self.s0)
            for ind in ind_i:
                self.i0[ind] = 1
                self.s0[ind] = 0
            self.i0 = np.reshape(self.i0, (self.M, self.M))
            self.s0 = np.reshape(self.s0, (self.M, self.M))
        self.r0 = np.zeros((self.M, self.M))
        self.i = self.i0
        self.s = self.s0
        self.r = self.r0
        self.weight = (1 / self.M) ** 2
        self.start = np.array([self.s0, self.r0, self.i0])
        self.diffusion_s = laplacian(self.s)
        self.diffusion_i = laplacian(self.i)
        self.diffusion_r = laplacian(self.r)
        self.diffusion = None
        self.s_f = []
        self.r_f = []
        self.i_f = []
        self.fun = lambda t, y: np.array(
            [-self.b * y[0] * y[2] + self.p * self.weight * self.diffusion[0], self.k * y[2] + self.p * self.weight * self.diffusion[1],
                self.b * y[0] * y[2] - self.k * y[2] + self.p * self.weight * self.diffusion[2]])

    def _infect(self, t):
        """
        Solves system to simulate infection.
        """
        self.t = t
        self.time = (0, self.t)
        t_vals = []
        for l in range(self.t):
            t_vals.append(l)
        s = np.zeros((self.M, self.M, self.t))
        r = np.zeros((self.M, self.M, self.t))
        i = np.zeros((self.M, self.M, self.t))
        for j in range(self.M):
            for k in range(self.M):
                self.diffusion = np.array(
                    [self.diffusion_s[j, k], self.diffusion_r[j, k], self.diffusion_i[j, k]])
                y0 = np.array([self.s0[j, k], self.r0[j, k], self.i0[j, k]])
                self.infection = solve_ivp(
                    self.fun, self.time, y0, t_eval=t_vals)
                s[j, k] = self.infection.y[0]
                r[j, k] = self.infection.y[1]
                i[j, k] = self.infection.y[2]
        self.s = s
        self.r = r
        self.i = i
        return self.infection

    def _give_values(self):
        """
        Convert grid solutions to proportions and return S, I, R values.
        """
        for t in range(self.t):
            temp_s = 0
            temp_i = 0
            temp_r = 0
            for j in range(self.M):
                for k in range(self.M):
                    temp_s = temp_s + self.s[j, k, t]
                    temp_i = temp_i + self.i[j, k, t]
                    temp_r = temp_r + self.r[j, k, t]
            self.s_f.append(temp_s)
            self.i_f.append(temp_i)
            self.r_f.append(temp_r)
        self.s_f = np.asarray(self.s_f) / (self.M ** 2)
        self.i_f = np.asarray(self.i_f) / (self.M ** 2)
        self.r_f = np.asarray(self.r_f) / (self.M ** 2)
        return self.s_f, self.i_f, self.r_f
