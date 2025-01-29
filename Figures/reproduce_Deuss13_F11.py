# Reproduce Fig. 11 of Deuss 2013
import sys
import numpy as np
sys.path.append('../Classes/')
from mode import Mode

def read_mode_from_file(file):
    n, l = file.readline().split()
    n = int(n)
    l = int(l)
    M = Mode(n, 'S', l)

    # Get the Csts:
    # There will be from s = 2 to s = 2l s values (even only) for self coupling

    # Loop over the s values for the mode
    for s in np.arange(2, 2 * l + 1, 2):
        # Initialise the Csts
        cst_vals = np.zeros(s + 1, dtype=complex)
        cst_errs = np.zeros(s + 1, dtype=complex)

        flinemarker = file.tell()
        vals = np.array(file.readline().split()).astype(float)
        # If the length is even then the line for the vals is a new mode and we need to bail out:
        if (len(vals) % 2 == 0):
            file.seek(flinemarker)

            break
        else:
            errs = np.array(file.readline().split()).astype(float)
            cst_vals[0] = vals[0]
            cst_errs[0] = errs[0]

            for t in range(s):
                cst_vals[1 + t] = vals[2 * t + 1] + vals[2 * t + 2] * 1j
                cst_errs[1 + t] = errs[2 * t + 1] + errs[2 * t + 2] * 1j

        M.cst.vals[s] = cst_vals
        M.cst.error[s] = cst_errs

    return M




modes = {}

# Open the file and read line by line:
fname = '../Data/Deuss_2013_GJI/cst_sc.dat'
skiplines = 5

with open(fname) as file:

    for i in range(skiplines):
        line = file.readline()

    # Read the n and l values
    for imode in range(164):
        mode = read_mode_from_file(file)
        modes[mode.name] = mode


print()