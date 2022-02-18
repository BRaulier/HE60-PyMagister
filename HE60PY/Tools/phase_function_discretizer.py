import numpy as np
import subprocess
import matplotlib.pyplot as plt
from scipy.integrate import quad


def henvey_greenstein_pf(phi, g, normalize=False):
    phi_rad = phi*np.pi/180
    mu = np.cos(phi_rad)
    beta = (1/(4*np.pi))*((1-g**2)/(1+g**2-2*g*mu)**(3/2))
    delta_phi = phi_rad
    delta_phi[1:] -= delta_phi[:-1].copy()
    if normalize:
        beta_normed = 2*np.pi*np.sum(beta*np.sin(phi_rad)*delta_phi)
        print(beta_normed)
        beta_normed = 2*np.pi*np.sum(beta*np.sin(phi_rad)*1.80018002e-02*np.pi/180)
        print(beta_normed)
        print(delta_phi)
    return beta


def create_tabulated_file(filename, pf_type):
    header = "/begin_header \n" \
             "{} phase function \n"\
             "This file is on the HSF95 format for phase function discretization. \n" \
             "deg   1/(m sr)\n" \
             "/end_header\n" \
             "1.00\n".format(pf_type)
    footer = "    -1.0    -1.0"







def create_input_file():


def create_executable_discretizer():
    path = '/Applications/HE60.app/Contents/source_code/Phase_function_code'
    cmd = ['sudo', './make_PFdiscretization6.sh']
    subprocess.run(cmd, cwd=path, capture_output=True, check=True)


def run_executable_discretizer():
    path = '/Applications/HE60.app/Contents/backend'
    cmd = ['sudo ./PFdiscretization6 < ../source_code/Phase_Function_code/Input_test.txt']
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

