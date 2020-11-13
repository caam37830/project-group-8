#!/bin/bash
#SBATCH --job-name=midterm_checkin_plots.py
#SBATCH --error=example_sbatch.err
#SBATCH --time=01:20:00
#SBATCH --partition=broadwl
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=14
#SBATCH --mem-per-cpu=2000

module load python
python midterm_checkin_plots.py
