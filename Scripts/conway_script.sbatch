#!/bin/bash
#SBATCH --job-name=conway_agent.py
#SBATCH --output=conway_agent.out
#SBATCH --error=conway_agent.err
#SBATCH --time=08:00:00
#SBATCH --partition=broadwl
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=4000

module load python
python conway_script.py
