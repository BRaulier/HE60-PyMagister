import numpy as np
import subprocess
import matplotlib.pyplot as plt
from scipy.integrate import quad


def henvey_greenstein_pf(phi, g):
    phi_rad = phi*np.pi/180
    mu = np.cos(phi_rad)
    beta = (1/(4*np.pi))*((1-g**2)/(1+g**2-2*g*mu)**(3/2))
    return beta


def create_tabulated_file(angle_beta_array, tab_filename, pf_type):
    path = '/Applications/HE60.app/Contents/source_code/Phase_Function_code/PF_user_data/'+tab_filename
    header = "/begin_header \n" \
             "{} phase function \n"\
             "This file is on the HSF95 format for phase function discretization. \n" \
             "deg   1/(m sr)\n" \
             "/end_header\n" \
             "1.00\n".format(pf_type)
    footer = "    -1.0    -1.0"
    with open(path, 'w+') as file:
        file.write(header)
        np.savetxt(file, angle_beta_array, fmt='%1.5e', delimiter='\t')
        file.write(footer)
    return filename

def create_input_file():


def create_executable_discretizer():
    path = '/Applications/HE60.app/Contents/source_code/Phase_function_code'
    cmd = ['sudo', './make_PFdiscretization6.sh']
    subprocess.run(cmd, cwd=path, capture_output=True, check=True)


def run_executable_discretizer(input_filename):
    path = '/Applications/HE60.app/Contents/backend'
    cmd = ['sudo ./PFdiscretization6 < ../source_code/Phase_Function_code/PF_PyMagister_input/{}'.format(input_filename)]
    subprocess.run(cmd, cwd=path, capture_output=True, check=True, shell=True)


if __name__ == '__main__':
    # create_executable_discretizer()
    # run_executable_discretizer()
    HE_angles, HE_beta = np.loadtxt('g0_90.txt').T

    angles = np.linspace(0, 180, 10000)
    my_beta = henvey_greenstein_pf(phi=angles, g=0.90, normalize=True)
    plt.plot(HE_angles, HE_beta)
    plt.plot(angles, my_beta)
    plt.show()

