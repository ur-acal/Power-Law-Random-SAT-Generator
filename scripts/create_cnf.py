import os
import subprocess
import numpy as np

############# NOTE###############
# Press enter at the end of the run
#################################

gen_path = "/scratch/mhuang_lab/ashar36/Power-Law-Random-SAT-Generator/"

o_path = "/scratch/mhuang_lab/ISING_MACHINES/GSET/CUSTOM_SAT/"

alpha = 4.25
cla_len = 3
nvars = np.arange(300, 600, 50)
nclas = np.round(nvars * alpha)
g = "u" # power-law(p)/uniform(u)
inst = 10

def main ():
    if not os.path.exists(o_path):
        os.mkdir(o_path)

    cmd = ""
    for i in range(len(nvars)):
        v = int(nvars[i])
        c = int(nclas[i])
        w = "cust-{:}{:}-{:}".format(g, v, c)

        w_path = "{:}/{:}/".format(o_path, w)
        if not os.path.exists(w_path):
            os.mkdir(w_path)

        for s in range(inst):
            s = s+1
            filename = "{:}/cust-{:}{:}-0{:}".format(w_path, g, v, s)

            cmd += "{:}/CreateSAT -g {:} -v {:} -c {:} -k {:} -p 2.5 -f {:} -u 1 -s {:};".format(\
            gen_path, g, v, c, cla_len, \
            filename, s)
    
    # print(cmd)
    stdout = subprocess.Popen(['/bin/bash', '-c', cmd])


if __name__ == '__main__':
    main()