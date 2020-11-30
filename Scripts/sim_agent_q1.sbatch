#!/bin/bash
#SBATCH --job-name=sim_agent_q1.py
#SBATCH --output=sim_agent_q1.out
#SBATCH --error=sim_agent_q1.err
#SBATCH --time=08:00:00
#SBATCH --partition=broadwl
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=4000

module load python
python sim_agent_q1
