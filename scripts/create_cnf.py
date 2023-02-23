import os
import subprocess
import numpy as np
import argparse as ap
############# NOTE###############
# Press enter at the end of the run
#################################

gen_path = "/scratch/mhuang_lab/mburns13/sat_generators/Power-Law-Random-SAT-Generator"

o_path = "/scratch/mhuang_lab/ISING_MACHINES/GSET/CUSTOM_SAT/"


parser = ap.ArgumentParser()
parser.add_argument('--alpha', type=float, default=4.25)
parser.add_argument('--beta', type=float, default = 5.0)
parser.add_argument('--n', type=int, nargs='+', required=True)
parser.add_argument('--power', action='store_true', default=False)
parser.add_argument('--inst', type=int, default=10)
args = parser.parse_args()


alpha = args.alpha
cla_len = 3
nvars = np.array(args.n)# np.arange(10, 60, 10)
nclas = np.round(nvars * alpha)
breakpoint()

g = "p" if args.power else 'u'# power-law(p)/uniform(u)
inst = args.inst
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
                        "{:}/CreateSAT -g {:} -v {:} -c {:} -k {:} -p {:} -f {:} -u 1 -s {:}\n".format(\
                        gen_path, g, v, c, cla_len, args.beta,\
                        filename, s))
    # print(cmd)
    stdout = subprocess.Popen(['/bin/bash', output])


if __name__ == '__main__':
    main()
