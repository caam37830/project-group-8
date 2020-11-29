#!/bin/bash
#SBATCH --job-name=smart_agent_sim.py
#SBATCH --error=smart_agent_sim.err
#SBATCH --time=01:20:00
#SBATCH --partition=broadwl
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=14
#SBATCH --mem-per-cpu=4000

module load python
python midterm_checkin_plots.py
