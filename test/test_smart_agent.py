"""
Conduct unit tests for `Agent` and `SIRModel`
"""
import unittest
import os
import sys
import random
import numpy as np

# Make an adjustment to where python will look for classes
# Since this script can be run from within `/test`, a sibling
# directory of `/sir`, or from the main project directory
if os.getcwd().split("/")[-1] == "test":
    sys.path.append("../sir")
else:
    sys.path.append("./sir")

# Import `Agent` and `SIRModel` classes.
from smartagent import *


class TestSmartAgentModel2D(unittest.TestCase):
    """
    Test the smart 2d agent model class
    """

    def setUp(self):
        """
        By convention
        """
        pass

    def test_init(self):
        """
        Test initializing the class with a variety of paramters, including
        `NoneType`s for the optional parameters
        """
        ps = [0, 0.25, 0.5]
        qs = [0, 0.25, 0.5]
        ks = [0.1, 0.2, 0.3]
        sz = [10, 20, 30]
        KTs = [1, 10, 20]
        FTs = [1, 10, 20]
        KDs = [0, 0.25, 0.5]
        FDs = [0, 0.25, 0.5]
        pr = [0.5, 0.2, None]
        ii = [3, 4, None]
        for p in ps:
            for q in qs:
                for k in ks:
                    for size in sz:
                        for kt in KTs:
                            for ft in FTs:
                                for kd in KDs:
                                    for fd in FDs:
                                        for prob_infect in pr:
                                            for initial_infect in ii:
                                                M = SmartAgentModel2D(
                                                    p,
                                                    q,
                                                    k,
                                                    size,
                                                    kt,
                                                    ft,
                                                    kd,
                                                    fd,
                                                    prob_infect,
                                                    initial_infect,
                                                )
                                                self.assertTrue(M.p == p)
                                                self.assertTrue(M.q == q)
                                                self.assertTrue(M.k == k)
                                                self.assertTrue(M.size == size)
                                                self.assertTrue(
                                                    M.knowledge_threshold == kt
                                                )
                                                self.assertTrue(M.fear_threshold == ft)
                                                self.assertTrue(
                                                    M.knowledge_distance == kd
                                                )
                                                self.assertTrue(M.fear_distance == fd)
                                                self.assertTrue(M.days_passed == 0)
                                                self.assertTrue(len(M.recovered) == 0)
                                                if prob_infect is None:
                                                    self.assertTrue(M.prob_infect == 1)
                                                else:
                                                    self.assertTrue(
                                                        M.prob_infect == prob_infect
                                                    )
                                                if initial_infect is None:
                                                    self.assertTrue(
                                                        M.initial_infect is None
                                                    )
                                                    self.assertTrue(
                                                        len(M.susceptible) == size
                                                    )
                                                    self.assertTrue(
                                                        len(M.infected) == 0
                                                    )
                                                else:
                                                    self.assertTrue(
                                                        M.initial_infect
                                                        == initial_infect
                                                    )
                                                    self.assertTrue(
                                                        len(M.susceptible)
                                                        == size - initial_infect
                                                    )
                                                    self.assertTrue(
                                                        len(M.infected)
                                                        == initial_infect
                                                    )

    def test_exogenous_infect(self):
        """
        Test the `exogenous_infect` method.
        Testing both parameterizations: randomly infecting `n` individuals, _or_
        infected precisely the individuals whose `Agent.id` is in a list of `indices`
        This, along with `test_step`, should each implicitly test `categorize_agents`
        method
        """
        p, q, k, size = 0.1, 0.1, 0.1, 100
        ns = [1, 10, 29]
        for n in ns:
            M = SmartAgentModel2D(p, q, k, size)
            M.exogenous_infect(n=n)
            self.assertTrue(len(M.susceptible) == size - n)
            self.assertTrue(len(M.infected) == n)
            self.assertTrue(len(M.recovered) == 0)

        ks = [10, 20, 30]
        for k in ks:
            indices = random.sample(list(range(size)), k=k)
            M = SmartAgentModel2D(p, q, k, size)
            M.exogenous_infect(indices=indices)
            # If the two lists are each subsets of each other, they are exactly equal
            self.assertTrue(set(M.infected).issubset(set(indices)))
            self.assertTrue(set(indices).issubset(set(M.infected)))
            # Ensure the effects on other lists are as expected
            self.assertTrue(len(M.susceptible) == size - k)
            self.assertTrue(len(M.recovered) == 0)

    def test_reset(self):
        """
        Ensure that the model can be reset to its initial state at any time
        """
        p, q, k, size = 0.1, 0.1, 0.1, 100
        M = SmartAgentModel2D(p, q, k, size)
        N = SmartAgentModel2D(p, q, k, size)
        N.step_t_days(15)
        N.reset()
        self.assertTrue(M.p == N.p)
        self.assertTrue(M.q == N.q)
        self.assertTrue(M.k == N.k)
        self.assertTrue(M.size == N.size)
        self.assertTrue(len(N.susceptible) == size)
        self.assertTrue(len(N.infected) == 0)
        self.assertTrue(len(N.recovered) == 0)
        self.assertTrue(M.days_passed == N.days_passed)
        self.assertTrue(M.prob_infect == N.prob_infect)

    def test_step(self):
        """
        Test that the model can reliably advance forward by one day's progress,
        and update model parameters
        """
        p, q, k, size, initial_infect = 0.1, 0.1, 0.1, 100, 5
        M = SmartAgentModel2D(p, q, k, size, initial_infect=initial_infect)
        day0, num_s0, num_i0, num_r0 = M.summarize_model()
        M.step()
        day1, num_s1, num_i1, num_r1 = M.summarize_model()

        # Checking that the day counter was advanced by `1`
        self.assertTrue(day1 - day0 == 1)
        # These effects are random, so checking logical upper/lower bounds
        self.assertTrue(0 <= num_s1 <= num_s0)
        self.assertTrue(0 <= num_i1 <= num_i0 * (1 + 100 * 3.14 * q ** 2))
        self.assertTrue(0 <= num_r1 <= num_r0 + num_i0)

    def test_step_t_days(self):
        """
        Test `step_t_days` method.
        This largely relies on the `step` method.
        Just need to check that the SIR return array is of the correct dimensions, and
        that the `days_passed` counter was updated correctly over many iterations, if these are true
        then it is clear that the other return value's will have correct dimension
        """
        ts = [5, 10, 15]
        p, q, k, size, initial_infect = 0.1, 0.1, 0.1, 100, 5
        for t in ts:
            M = SmartAgentModel2D(p, q, k, size, initial_infect=initial_infect)
            return_shape_SIR = M.step_t_days(t)[0].shape
            self.assertTrue(M.days_passed == t - 1)
            self.assertTrue(return_shape_SIR[0] == t)
            self.assertTrue(return_shape_SIR[1] == 4)


# Test `SmartAgent` functionality
class TestSmartAgent(unittest.TestCase):
    """
    Test methods for the `SmartAgent` class
    `Agent.status()` method is trivial, and also implictly tested by testing
    `infect()`, `recover()`, and `reset`
    """

    def setUp(self):
        """
        By convention
        """
        pass

    def test_init(self):
        """
        Ensure the agent is initialized with an `id`, as prescribed, as well as to the
        susceptible state
        """
        for ii in [5, 22, 89]:
            for pos in [[0.25, 0.25], [0.5, 0.5], None]:
                A = SmartAgent(ii, pos)
                s, i, r = A.status()
                self.assertTrue(A.id == ii)
                self.assertTrue(s == True)
                self.assertTrue(i == False)
                self.assertTrue(r == False)
                if pos == None:
                    self.assertTrue(A.pos[0] <= 1)
                    self.assertTrue(A.pos[1] <= 1)
                    self.assertTrue(A.pos[0] >= 0)
                    self.assertTrue(A.pos[1] >= 0)
                else:
                    self.assertTrue(A.pos == pos)

    def test_infect(self):
        """
        Testing the healthy agents can be infected, but recovered agents cannot
        """
        # Testing infection
        A = SmartAgent(1)
        A.infect()
        s, i, r = A.status()
        self.assertTrue(s == False)
        self.assertTrue(i == True)
        self.assertTrue(r == False)

        # An agent who is already recovered shouldn't be infected
        A.recover()
        A.infect()
        s, i, r = A.status()
        self.assertTrue(s == False)
        self.assertTrue(i == False)
        self.assertTrue(r == True)

    def test_recover(self):
        """
        Testing that infected agents can be recovered, but susceptible and already
        recovered agents cannnot
        """
        # An agent who isn't sick can't recover
        # So this should not change anything
        A = SmartAgent(1)
        s, i, r = A.status()
        A.recover()
        self.assertTrue(s == True)
        self.assertTrue(i == False)
        self.assertTrue(r == False)

        # This also shouldn't change anything
        A.recover()
        s, i, r = A.status()
        self.assertTrue(s == True)
        self.assertTrue(i == False)
        self.assertTrue(r == False)

        # Testing the actual use case
        A.infect()
        A.recover()
        s, i, r = A.status()
        self.assertTrue(s == False)
        self.assertTrue(i == False)
        self.assertTrue(r == True)

    def test_reset(self):
        """
        Ensure that the agent can be reset to its initial state at any time
        """
        A = SmartAgent(1)
        A.reset()
        s, i, r = A.status()
        self.assertTrue(s == True)
        self.assertTrue(i == False)
        self.assertTrue(r == False)
        self.assertTrue(A.id == 1)
        self.assertTrue(A.pos[0] <= 1)
        self.assertTrue(A.pos[1] <= 1)
        self.assertTrue(A.pos[0] >= 0)
        self.assertTrue(A.pos[1] >= 0)

        A.infect()
        A.reset()
        s, i, r = A.status()
        self.assertTrue(s == True)
        self.assertTrue(i == False)
        self.assertTrue(r == False)
        self.assertTrue(A.id == 1)
        self.assertTrue(A.pos[0] <= 1)
        self.assertTrue(A.pos[1] <= 1)
        self.assertTrue(A.pos[0] >= 0)
        self.assertTrue(A.pos[1] >= 0)

        A.infect()
        A.recover()
        A.reset()
        self.assertTrue(s == True)
        self.assertTrue(i == False)
        self.assertTrue(r == False)
        self.assertTrue(A.id == 1)
        self.assertTrue(A.pos[0] <= 1)
        self.assertTrue(A.pos[1] <= 1)
        self.assertTrue(A.pos[0] >= 0)
        self.assertTrue(A.pos[1] >= 0)

    def test_move(self):
        """
        Ensure that the agent always makes a legal move
        """
        A = SmartAgent(1)
        ps = [0.1, 0.2, 0.5]
        fts = [0, 5, 10]
        nb = [np.random.rand(100, 2)]
        for p in ps:
            for ft in fts:
                A_pos_1 = A.pos
                A.move(p, ft, nb)
                self.assertTrue(np.round(np.linalg.norm(A_pos_1 - A.pos), 3) <= p)

    def test_learn(self):
        """
        Ensure that the agent does not get a lower knowledge level after learning
        """
        A = SmartAgent(1)
        ns = [10, 20, 50]
        for n in ns:
            A_k_1 = A.knowledge
            A.learn(n)
            self.assertTrue(A_k_1 <= A.knowledge)

    def test_learn(self):
        """
        Ensure that the agent does not get a lower fear level after reacting
        """
        A = SmartAgent(1)
        ns = [10, 20, 50]
        for n in ns:
            A_f_1 = A.fear
            A.react(n)
            self.assertTrue(A_f_1 <= A.fear)