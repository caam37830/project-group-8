
# Introduction to SIR method and terminology

# Structure of SIR python package

# Preliminary investigations

We investigate a variety of different simulations, all of the plots created can be found in the plots folder, but we will discuss a few of the most interesting outcomes in this section. Generally, it is important to understand the factors that drive a virus to spread and then use that information to best understand how to stop it. The first factor we will investigate is "b", the infections per day per agent

# Extensions
## Extension - Anna

A variation we would like to implement is to account for reinfection in the S, I, R model. With some viruses, even if infection leads to immunity in most, there is some probability of reinfection. Preliminary studies have found this to be the possible with coronavirus. 
1.	In the final report, we would like to show how reinfection influences the spread of the infection. This would include the size of infected population and the rate at which the infection spreads. 
2.	Implementing this from an ODE perspective, this would mean including in the rate of change of susceptible population a term connected with the recovered population’s probability of reinfection. This would also include accounting for recovered person’s who became infected again in the representation of the recovered population.
3.	If we want to model this as the coronavirus, limited information about reinfection rates can be found in a paper by Murillo-Zamora et al.
4.	Reference: Murillo-Zamora E.; Mendoza-Cano O.; Delgado-Enciso I.; Hernandez-Suarez C. M. Predictors of Severe Symptomatic Laboratory-Confirmed Sars-Cov-2 Reinfection. *medRxiv* **2020**, 2020.10.14.20212720.

## Extension - Jack


## Extension - Jarrod

The reactions of individuals and organizations is one of the most important factors in curbing the spread of a disease; however, information about what slows the spread, what harms the individuals, and who is susceptible to the disease is not always public information. Masks have been politicized and are widely used by certain groups whereas in others they are almost unanimously rejected as a valid form of defence against the virus. At one point we assumed that you could not be reinfected by the virus, while now there is information that supports that you can indeed get infected more than once. Overall, the virus is confusing and people act irrationally. We want to explore how the way people learn about the virus effects the spread of the disease, and how knowledge about the disease spreads in parallel to the disease itself.
1.  There are a variety of questions that are interesting, but mainly we want to study how information of the disease clusters and how that effects the spread of disease. Those in close proximity to the disease are likely to learn more about the disease itself, but at the same time they are more likely to get it. Also, what if there is a source of misinformation in the system, can this misinformation increase the rate of infection?
2.  We can implement this in the agent model in a 2 dimensional space, where agents learn about the virus from those around them getting infected. We can add parameters to the agent class such as "fear" (that would make an agent less likely to interact with others), "knowledge" (that would make agents less likely to contract the disease in and interaction), and a variety of other information based parameters. We also may be interested in allowing agents to move within the area of the simulation, does social distancing arise?
3.  This idea will not involve data, but it will be important to understand dynamics of interaction under knowledge sets. To support our assumptions about how agents react to information we may refer to ideas from economics. We cite some texts below that are related to optimizing given information sets.
4.  - Kamien, Morton I., and Nancy Lou Schwartz. Dynamic Optimization the Calculus of Variations and Optimal Control in Economics and Management. Dover Publications, 2012. 
    - Osborne, Martin J. An Introduction to Game Theory. Oxford University Press, 2017. 
    - Fleming, Nic. “Coronavirus Misinformation, and How Scientists Can Help to Fight It.” Nature News, Nature Publishing Group, 17 June 2020, www.nature.com/articles/d41586-020-01834-3. 



