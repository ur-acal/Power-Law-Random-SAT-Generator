import re
import os
import sys
import glob
import numpy as np
import subprocess as sp
from itertools import product

sat_re = re.compile(r'^s\s+SATISFIABLE', re.MULTILINE)
local_path = '/home/matt/Documents/remote'
# Differentiate execution between linux box and bluehive
if os.path.exists(local_path):
    _main = local_path
    _library = '/home/matt/Documents/SAT'
else:
    _main = '/scratch/mhuang_lab/mburns13'
    _library = '/scratch/mhuang_lab/ISING_MACHINES/GSET'

_exec = os.path.join(_main, 'sat_solvers/kissat-1.0.3-79d8d8f2/build/kissat')

def check_sat(dimacs: str) -> bool:
    """Check if the CNF formula is SAT

    Runs KISSAT in a subprocess to determine if satisfiable
    Args:
        dimacs (str): Path to DIMACS-formatted file

    Returns:
        bool: Whether the problem is satisfiable
    """
    completed = sp.run([_exec, dimacs], capture_output=True)
    if re.search(sat_re, completed.stdout.decode()) is None:
        return False
    return True

# Construct variable paths to loop over
alpha = 4.25 # Ratio of clauses:variables
_n = np.array([25, 35]) # Variable counts
# _n = np.arange(5, 8).astype(int)
_m = (_n * alpha).round().astype(int) # clause counts (rounded to nearest int)
# Formatting strings for the problem class (variable and clause counts)
#   and the problem instance (variable count and problem number)
problem_base = 'cust-u{:}-{:}'
instance_base = 'cust-u{:}-0{:}.cnf'

remove_index = lambda x: x[:x.rfind('-')] # Lambda expression to remove the trailing number from a problem instance

instances = range(1, 200) # Which problem instances to check/remove

problems = [problem_base.format(n, m) for n, m in zip(_n, _m)]# Construct list of problem classes

# Construct list of specific problem instances
problem_instances = [os.path.join(p, instance_base.format(n, i))
                     for (p, n), i in product(zip(problems, _n), instances)]

# Subdirectory of `_main` to search
work = 'CUSTOM_SAT'
# Construct list of (extant) paths as a numpy array to allow for conditional indexing
paths = [os.path.join(_library, work, prob) for prob in problem_instances]
paths = np.array([p for p in paths if os.path.exists(p)])
# Check which paths are unsat
is_sat = np.array([check_sat(p) for p in paths])
# Get the unsatisfiable problem paths and remove them
unsat_paths = paths[is_sat == False]
for i in unsat_paths:
    os.remove(i)

# Rename the remaining files to avoid gaps in the instance IDs
for pdir in problems:

    dirpath = os.path.join(_library, work, pdir) # Path to problem directory

    files = glob.glob(os.path.join(dirpath, '*')) # All DIMACS files in that directory

    indices = range(1, len(files) + 1) # List of integers equal to the length of remaining files

    namelist = [] # List to store temporary names, new names
    # Rename all files to temporary, avoid accidentally overwriting files
    for f, index in zip(files, indices):
        oldname = f
        tempname = f + '.temp'
        os.rename(oldname, tempname)
        newname = remove_index(f) + '-0{:}.cnf'.format(index)
        namelist.append((tempname, newname))
    # Rename all temp files to new names
    for temp, new in namelist:
        os.rename(temp, new)
