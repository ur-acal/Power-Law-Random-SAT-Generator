import os
import subprocess
import numpy as np

############# NOTE###############
# Press enter at the end of the run
#################################

gen_path = "/scratch/mhuang_lab/mburns13/scripts/Power-Law-Random-SAT-Generator"

o_path = "/scratch/mhuang_lab/ISING_MACHINES/GSET/CUSTOM_SAT/"

work = "p"

alpha = 4.25
cla_len = 3
nvars = np.array([25,35])# np.arange(10, 60, 10)
nclas = np.round(nvars * alpha)
g = "u" # power-law(p)/uniform(u)
inst = 50
output = os.path.dirname(gen_path) + '/gen_cmd.sh'
def main ():
    if not os.path.exists(o_path):
        os.mkdir(o_path)

    cmd = ""
    with open(output, mode='w') as sh_file:
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

                sh_file.write(
                    "{:}/CreateSAT -g {:} -v {:} -c {:} -k {:} -p 2.5 -f {:} -u 1 -s {:}\n".format(\
                        gen_path, g, v, c, cla_len, \
                        filename, s))
    # print(cmd)
    stdout = subprocess.Popen(['/bin/bash', output])


if __name__ == '__main__':
    main()
