"""
Conduct unit tests for `ConwayAgent` and `ConwayModel`
"""
import os
import sys
import random
import unittest
import numpy as np

# Make an adjustment to where python will look for classes
# Since this script can be run from within `/test`, a sibling
# directory of `/sir`, or from the main project directory
if os.getcwd().split("/")[-2] == "project-group-8":
    sys.path.append("../sir")
else:
    sys.path.append("./sir")
from conway_agent import ConwayAgent, ConwayModel


class TestConwayAgent(unittest.TestCase):
    """
    Test the `ConwayAgent` class
    """

    def setUp(self):
        """
        By convention
        """
        pass

    def test_init(self):
        """
        Test the initialization of the class
        """
        ids = 1, 2, 3, 4, 5
        is_alive = True, False, True, True, False
        for integer, boolean in zip(ids, is_alive):
            A = ConwayAgent(integer, boolean)
            self.assertTrue(A.id == integer)
            self.assertTrue(A.is_alive == boolean)
            self.assertTrue(A.s == True)
            self.assertTrue(A.i == A.r == False)

    def test_infect(self):
        """
        Testing `infect()` method
        i. Living agents who are susceptible may be infected
        ii. Dead agents may not be infected
        """
        # Should infect a living agent who is susceptible
        A = ConwayAgent(23, True)
        self.assertTrue(A.status() == 1)
        A.infect()
        self.assertTrue(A.status() == 2)

        # Should not infect a recovered agent
        A.recover()
        A.infect()
        self.assertTrue(A.status() == 3)

        # Should not infect a dead agent
        A.reset()
        A.kill()
        A.infect()
        self.assertTrue(A.status() == 0)

    def test_recover(self):
        """
        Testing `recover()` method
        Only living, infected agents may be recovered
        """
        # Should work
        A = ConwayAgent(23, True)
        A.infect()
        A.recover()
        self.assertTrue(A.status() == 3)

        # Should do nothing
        A.reset()
        A.recover()
        self.assertTrue(A.status() == 1)

        # Should also do nothing
        A.infect()
        A.kill()
        A.recover()
        self.assertTrue(A.status() == 0)

    def test_born(self):
        """
        Testing the `born()` method
        """
        A = ConwayAgent(23, False)
        self.assertTrue(A.status() == 0)
        A.born()
        self.assertTrue(A.status() == 1)

    def test_kill(self):
        """
        Testing the `kill()` method
        """
        A = ConwayAgent(23, True)
        self.assertTrue(A.status() == 1)
        A.kill()
        self.assertTrue(A.status() == 0)


class TestConwayModel(unittest.TestCase):
    """
    Test the `ConwayAgent` class
    """

    def setUp(self):
        """
        By convention
        """
        pass

    def test_init(self):
        """
        Verify that the class is initalized properly
        """
        m, n = 5, 5
        k, p = 0.2, 0.7
        agents = [ConwayAgent(ii, ii & 0x1 == 1) for ii in range(m * n)]
        C = ConwayModel(m, n, k, p, agents)
        self.assertTrue(C.m == m and C.n == n)
        self.assertTrue(C.k == k and C.p == p)
        self.assertTrue(len(C.alive_agents) == m * n // 2)
        self.assertTrue(len(C.agents) == m * n)

    def test_get_alive_agents(self):
        """
        Verify that alive agents has the correct agents stored
        """
        m, n = 5, 5
        k, p = 0.2, 0.7
        agents = [ConwayAgent(ii, ii & 0x1 == 1) for ii in range(m * n)]
        C = ConwayModel(m, n, k, p, agents)
        alive_ids = [A.id for A in C.alive_agents]
        self.assertTrue(all([lambda x: x & 0x1 == 1 for x in alive_ids]))

    def test_count_neighbors(self):
        """
        Test that the neighbor-counting method works as expected
        """
        m, n = 5, 5
        k, p = 0.2, 0.7
        agents = [ConwayAgent(ii, ii & 0x1 == 1) for ii in range(m * n)]
        C = ConwayModel(m, n, k, p, agents)

        to_count = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
        expected = np.array([[1, 1, 2], [2, 3, 1], [0, 2, 1]])
        result = C.count_neighbors(to_count)
        self.assertTrue(np.all(expected == result))

    def test_step_t_days(self):
        days = 5, 10, 20, 30
        for d in days:
            m, n = 5, 5
            k, p = 0.2, 0.7
            agents = [ConwayAgent(ii, ii & 0x1 == 1) for ii in range(m * n)]
            C = ConwayModel(m, n, k, p, agents)
            result = C.step_t_days(d)
            self.assertTrue(result.shape[0] == d and result.shape[1] == 4)
            self.assertTrue(C.days_passed == d - 1)
