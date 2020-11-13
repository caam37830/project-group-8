"""
Implement unittests for ODE method.
"""
from scipy.integrate import odeint
from scipy.integrate import solve_ivp
import numpy as np
import unittest
import sys

sys.path.append("../sir/")
from ode import OdeSir

class TestSolver(unittest.TestCase):
    def setUp(self):
        pass

    def test_ode(self):
        """
        Test that the ODE satisfies the equations.
        """
        test = OdeSir(0.1, 100, 0.5, 0.5)
        test._infect(25)
        s, i, r = test._give_values()
        time = test._give_time()
        a = np.asarray(np.where(abs(25 - time) <= 0.001))
        dt = time[a] - time[a-1]
        ds = s[a] - s[a-1]
        ds_dt = ds / dt
        sols = -0.5 * s[a-1] * i[a-1]
        dr = r[a] - r[a-1]
        dr_dt = dr / dt
        solr = 0.5 * i[a-1]
        di = i[a] - i[a-1]
        di_dt = di / dt
        soli = 0.5 * s[a-1] * i[a-1] - 0.5 * i[a-1]
        self.assertTrue(abs(ds_dt - sols) <= 0.001 and abs(di_dt - soli)
                        <= 0.001 and abs(dr_dt - solr) <= 0.001)

    def test_give_values(self):
        """
        Test _give_func
        """
        test = OdeSir(0.1, 100, 0.5, 0.5)
        s, i, r = test._give_values()
        self.assertTrue(s == 0.9 and r == 0 and i == 0.1)

    def test_give_start(self):
        """
        Test the give start function
        """
        test = OdeSir(0.1, 100, 0.5, 0.5)
        start = np.array([0.9, 0, 0.1])
        out = test._give_start()
        diff = start - out
        self.assertTrue(abs(diff).all() <= 0.001)

    def test_infect(self):
        """
        Test the _infect function.
        """
        test = OdeSir(0.1, 100, 0.5, 0.5)

        def func(t, y):
            return np.array(
                [-0.5 * y[0] * y[2], 0.5 * y[2], 0.5 * y[0] * y[2] - 0.5 * y[2]]
            )

        start = np.array([0.9, 0, 0.1])
        tspan = (0, 5)
        out = solve_ivp(func, tspan, start)
        infect = test._infect(5).y
        diff = out.y - infect
        self.assertTrue(abs(diff).all() <= 0.001)

    def test_reset(self):
        """
        Test the reset function.
        """
        test = OdeSir(0.1, 100, 0.5, 0.5)
        s1, i1, r1 = test._give_values()
        test._infect(5)
        test._reset()
        s, i, r = test._give_values()
        self.assertTrue(i == i1 and s == s1 and r == r1)

    def test_totals(self):
        """
        Test that s + i + r = 1

        and S + I + R = N
        """
        test = OdeSir(0.1, 100, 0.5, 0.5)
        test._infect(5)
        s, i, r = test._give_values()
        S, I, R = test._give_totals()
        t = s + i + r
        T = S + I + R
        self.assertTrue(t.all() == 1 and abs(100 - T).all() <= 0.001)

    def test_give_time(self):
        """
        Test the _give_time function.
        """
        test = OdeSir(0.1, 100, 0.5, 0.5)
        test._infect(5)

        def func(t, y):
            return np.array(
                [-0.5 * y[0] * y[2], 0.5 * y[2], 0.5 * y[0] * y[2] - 0.5 * y[2]]
            )

        start = np.array([0.9, 0, 0.1])
        tspan = (0, 5)
        out = solve_ivp(func, tspan, start)
        t_out = out.t
        t_test = test._give_time()
        self.assertTrue(abs(t_out - t_test).all() <= 0.001)
