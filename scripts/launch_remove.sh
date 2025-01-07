#!/bin/sh
#SBATCH -p preempt -o remove.log --mem=4G -t 12:00:00
PYPATH=/gpfs/fs2/scratch/mhuang_lab/mburns13/.conda/envs/venv/bin/python
SCRIPT=/gpfs/fs2/scratch/mhuang_lab/mburns13/sat_generators/Power-Law-Random-SAT-Generator/scripts/remove_unsat.py
$PYPATH $SCRIPT