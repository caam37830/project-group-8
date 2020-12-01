# Introduction to SIR method and terminology
The SIR model is a method for modeling the spread of disease in a population based on the idea that the individuals in the population fall in to one of three categories: susceptible, removed, or infected. Susceptible individuals have not yet gotten the disease and are in danger of contracting it. Infected individuals are carriers of the disease and spread it to others. Removed individuals have either recovered from the disease or died, so are no longer susceptible to it. We have implemented this method using both an Agent-based model and a system of ODEs. Furthermore, we explore the SIR model both with a spatial component and without. For the spatial case, both methods use parameters `p`, `q` and `k` to represent how the disease spreads. The parameter `p` represents the maximum distance that an agent can move per period, `q` represents the radius around and infected individual that the disease can spread, and `k` represents the fraction of the infected population that recovers each day. In the traditional SIR model with no spatial component, `p` and `q` are replaced with one variable `b`, which represents the number of infected agents per infected agent per period. In our discussion of these models we have used the following notation:
  
  `i = fraction of the population that is infected (initial conditions i0)`
  
  `I = absolute number of infected individuals (initial conditions I0)`
  
  `r = fraction of the population that is removed (initial conditions r0)`
  
  `R = absolute number of removed individuals (initial conditions R0)`
  
  `s = fraction of the population that is susceptible (initial conditions s0)`
  
  `S = absolute number of susceptible individuals (initials conditions S0)`
  
  `N = number of individuals in the population`
  
  `t = time`

The Agent-based model uses interactions between infected individuals and susceptible individuals to trace the spread of the disease. The ODE method uses time dependent variables for each of the three possible states to model the spread of the disease. The evolution of these variables is described by the system of equations:
  
  `ds/dt = -b * s(t) * i(t)`
  
  `dr/dt = k * i(t)`
  
  `di/dt = b * s(t) * i(t) - k * i(t)`

We also explore three extensions to the above models, two of them being related to the agent based model and the other being related to the ODE model. We provide a brief introduction to each:
1.  We explore how the spread of the virus is effected if the agents take some effort to socially distance themselves from others, if given enough information about the disease. We define the following parameters that are specific to this extension:

    `knowledge_distance (kd) = the radius around an individual from which they can gather knowledge` 

    `knowledge = the cumulative sum of infected and recovered individuals within the knowledge_distance of an individual`

    `knowledge_threshold (kt) = the knowledge score that an infected agent must have to socially distance itself from healthy agents`

    `fear_distance (fd) = the radius around an individual from which they can gather become more fearful of the disease` 

    `fear = the cumulative sum of infected individuals within the fear_distance of an individual`

    `fear_threshold (ft) = the fear score that a healthy agent must have to socially distance themselves from infected agents`

Once a healthy agent achieves a fear score above the threshold level, they will then chose the location within a distance `p` that maximizes the sum of distances between them and any infected agents that are within the `fear_distance` from them. Furthermore, once an infected agent achieves a knowledge score above the threshold level, they will maximizes the sum of distances between them and healthy individuals within the `knowledge_distance` from them. Recovered individuals, and individuals that have not surpassed threshold levels do not act in any intelligent manner so they just chose a random location, within radius `p`, to move to each period.

# Structure of SIR python package

The `sir` package contains thee submodules: One, `agent`, contains class definitions for `Agent` and `DiscreteAgentModel`, which are necessary to carry out the discrete agent simulations with no spatial component. Two, `ode`, contains the class definition for `OdeSir`, which is necessary to carry out the ODE version of the problem. Three, `smartagent`, contains class definitions for `SmartAgent` and `SmartAgentModel2D`, which are necessary to carry out the discrete agent simulations with spatial component, and can be used to model "inteligent" agent behavior along with the standard random behavior.
  

# Basic SIR model

We investigate a variety of different simulations and will discuss only the most interesting in this section (for more on this model and a discussion of other simulations see the midterm checkpoint). The choice of `b` and `k` is of great importance in how both of these methods model the spread of disease through a population. The higher `k` is the faster any given individual will recover from the disease, and thus the less time they will be able to infect people. On the other hand, a high `b` will lead to many agents being infected each period. Ultimately, increasing the initial number infected or `b` generally will lead to more people getting infected faster and the disease being more successful overall, while increasing `k` will have the opposite effect.

Generally the ODE model and the agent based model provide similar dynamics to how the virus will progress through a population. However, we chose to highlight a simulation in which the two approaches do not agree:
![image](../checkpoint/plots/k40Agent.png)
![image](../checkpoint/plots/k40ODE.png)

These two models have the same parameters, yet the the ODE model seems to create drastically different results than the agent based approach. This seems odd at first, but a small nudge in the direction of increased infections can lead to a much worse outcome overall. For example, consider that the infection rate is the same as the recovery rate if there are 50 agents that are infected. Then, we could expect the number of agents who are sick to not increase that much. However, if we nudge that number up a little bit, say to 70, then we have pushed the system out of equilibrium and the infections may get out of control, this is the idea of flattening the curve and trying to keep the number of infections manageable. This example is important to keep in mind for not only the spatial model, but the extensions as well as it indicates how important our model assumptions are to the dynamics of a disease.

# SIR model with spatial component

For the discrete agent spatial model we first need to understand how our choice of parameters effects the timeline of the virus. Unlike in the non-spatial model, the population size plays a huge role in the dynamics of the virus since we fix the world to a 1x1 square. Thus, the higher the population the more densely packed our agents are and this leads to the virus spreading more quickly even with a low value of `q`. Both `p` and `q` have positive relationships with the rate of spread, which makes sense. If individuals have a large radius of infection, then they infect more people per period, and if they move a large distance, then the chance that an infected person interacts with agents that they haven't interacted with before also increases. This leads to our first simulation in which we start with 5 infected agents at the center of the population and see how the virus spreads holding all constant between simulations but the distance that agents can move per period `p`.


# Smart Agent extension

Throughout history, we have faced various diseases and have found that social distancing and quarantines have been one of the best ways to combat the spread (Roos (2020)). So, we propose the question: How does the course of a disease spreading change if the agents make intelligent decisions to slow its spread? 

We first observe a baseline simulation (with parameters p = 0.01, q = 0.01, k = 0.05, size = 10000) of a disease where agents do not do anything to slow the spread ():
![image](plots/nolearn.png)

# extension 2

# extension 3

# extension conclusions

# Bibliography

Roos, Dave. “Social Distancing and Quarantine Were Used in Medieval Times to Fight the Black Death.” History.com, A&amp;E Television Networks, 25 Mar. 2020, www.history.com/news/quarantine-black-death-medieval. 
