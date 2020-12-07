import numpy as np
from scipy.integrate import solve_ivp
from scipy.sparse.csgraph import laplacian
from scipy.integrate import solve_bvp
import scipy.sparse as sparse
import scipy.sparse.linalg as spla
import math
import sys
sys.path.append("./")
from ode import OdeSir

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
