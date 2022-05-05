import numpy as np
import os
import subprocess
import matplotlib.pyplot as plt
from scipy.integrate import quad
import olympus
from scipy.interpolate import interp1d
from scipy import integrate


def henvey_greenstein_pf(phi_deg, g):
    phi_rad = phi_deg*np.pi/180
    mu = np.cos(phi_rad)
    beta = (1/(4*np.pi))*((1-g**2)/(1+g**2-2*g*mu)**(3/2))
    return beta

def henvey_greenstein_2pf(phi_deg, gs, b):
    g1, g2 = gs
    phi_rad = phi_deg*np.pi/180
    mu = np.cos(phi_rad)
    G_1 = (1/(4*np.pi))*((1-g1**2)/(1+g1**2-2*g1*mu)**(3/2))
    G_2 = (1/(4*np.pi))*((1-g2**2)/(1+g2**2-2*g2*mu)**(3/2))
    beta = b*G_1 + (1-b)*G_2
    return beta

def create_tabulated_file(angle_beta_array, tab_filename, pf_type):
    path = '/Applications/HE60.app/Contents/source_code/Phase_Function_code/PF_user_data/Py_Magister_PF/'+tab_filename+'.txt'
    header = "/begin_header \n" \
             f"{pf_type} phase function \n"\
             "This file is on the HSF95 format for phase function discretization. \n" \
             "deg   1/(m sr)\n" \
             "/end_header\n" \
             "1.00\n"
    footer = "    -1.0    -1.0"
    with open(path, 'w+') as file:
        file.write(header)
        np.savetxt(file, angle_beta_array.T, fmt='%1.5e', delimiter='\t')
        file.write(footer)
    return tab_filename


def create_input_file(input_filename, dpf_filename, tab_filename, comment='If it ain’t broke, don’t fix it :).'):
    path = '/Applications/HE60.app/Contents/source_code/Phase_Function_code/PF_PyMagister_input/'+input_filename+'.txt'
    with open(path, 'w+') as file:
        file.write(dpf_filename+'\n')
        file.write(comment+'\n')
        file.write('Py_Magister_PF/'+tab_filename+'.txt\n')
    return path


def create_executable_discretizer():
    path = '/Applications/HE60.app/Contents/source_code/Phase_function_code'
    path_to_PFdis = '/Applications/HE60.app/Contents/backend/PFdiscretization6'
    cmd = ['sudo', './make_PFdiscretization6.sh']
    if olympus.DoesThisExist(path_to_PFdis):
        pass  # Do not run this time consuming command if the file already exists.
    else:
         subprocess.run(cmd, cwd=path, capture_output=True, check=True)


def run_executable_discretizer(input_filename):
    path = '/Applications/HE60.app/Contents/backend'
    cmd = ['sudo ./PFdiscretization6 < ../source_code/Phase_Function_code/PF_PyMagister_input/'+input_filename+'.txt']
    subprocess.run(cmd, cwd=path, capture_output=True, check=True, shell=True)


def create_OTHG_discretized_files():
    create_executable_discretizer()
    g_values = np.array([0.90, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.98, 0.99], dtype=np.float16)
    angle_values = np.hstack((np.linspace(0.1, 0.9, 9), np.linspace(1, 180, 180)))
    for g_value in g_values:
        tab_filename = 'OTHG_{:.2f}'.format(g_value).replace('.', '_')
        input_filename = tab_filename

        beta_values = henvey_greenstein_pf(phi_deg=angle_values, g=g_value)
        angle_beta_array = np.vstack((angle_values.T, beta_values.T))
        create_tabulated_file(angle_beta_array=angle_beta_array, tab_filename=tab_filename, pf_type=tab_filename)
        create_input_file(input_filename=input_filename, dpf_filename=tab_filename, tab_filename=tab_filename)
        run_executable_discretizer(input_filename=input_filename)

def create_OTHG2_discretized_files():
    create_executable_discretizer()
    g1_values = np.array([0.60, 0.65, 0.70, 0.75], dtype=np.float16)
    g2_values = np.array([-.55, -0.15, -0.25, -0.15], dtype=np.float16)
    b_values = np.array([0.9, 0.70, 0.85, 0.80], dtype=np.float16)
    angle_values = np.hstack((np.linspace(0.1, 0.9, 9), np.linspace(1, 180, 180)))
    for g1, g2, b in zip(g1_values, g2_values, b_values):
        tab_filename = 'OTHG2_g1{:.2f}_g2{:.2f}_b{:.2f}'.format(g1, g2, b).replace('.', '_')
        input_filename = tab_filename
        beta_values = henvey_greenstein_2pf(phi_deg=angle_values, gs=(g1,g2), b=b)
        angle_beta_array = np.vstack((angle_values.T, beta_values.T))
        create_tabulated_file(angle_beta_array=angle_beta_array, tab_filename=tab_filename, pf_type=tab_filename)
        create_input_file(input_filename=input_filename, dpf_filename=tab_filename, tab_filename=tab_filename)
        run_executable_discretizer(input_filename=input_filename)

def create_brine_discretized_files(angle_values, beta_values):
    create_executable_discretizer()
    beta_values = beta_values/0.988216
    tab_filename = "brine_1_96"
    input_filename = 'brine_1_96'
    angle_beta_array = np.vstack((angle_values.T, beta_values.T))
    create_tabulated_file(angle_beta_array=angle_beta_array, tab_filename=tab_filename, pf_type=tab_filename)
    create_input_file(input_filename=input_filename, dpf_filename=tab_filename, tab_filename=tab_filename)
    run_executable_discretizer(input_filename=input_filename)


def interpolate_and_compute_g(angle, pf):
    # Interpolation
    pf_func = interp1d(angle, pf, kind='linear')
    new_angles = np.linspace(0.0001, 179.9999, 10000)
    new_pf = pf_func(new_angles)
    g = calculate_assym(new_angles, new_pf)
    plt.semilogy(angle, pf, label="Sans interpolation")
    plt.semilogy(new_angles, new_pf, label="Avec interpolation linéaire")
    plt.legend()
    plt.show()
    print(g)

def calculate_assym(theta, pf):
    theta_rad = theta * np.pi / 180
    return 2 * np.pi * integrate.simps(pf * np.cos(theta_rad) * np.sin(theta_rad), x=theta_rad)


if __name__ == '__main__':
    g1_values = np.array([0.98, 0.65, 0.70, 0.75], dtype=np.float16)
    g2_values = np.array([-.15, -0.15, -0.25, -0.15], dtype=np.float16)
    b_values = np.array([0.99, 0.70, 0.85, 0.80], dtype=np.float16)
    angles = np.linspace(0, 180, 180)
    g98 = henvey_greenstein_pf(angles, 0.98)
    for g1, g2, b in zip(g1_values, g2_values, b_values):
        beta = henvey_greenstein_2pf(angles, (g1, g2), b)
        plt.semilogy(angles, beta)
    plt.semilogy(angles, g98, color='black', label="HG 0.98")
    plt.legend()
    plt.show()
    # path = "/Users/braulier/Documents/HE60_PY/ressources/PF_tab_brine_196_.txt"
    # n, angle_values, beta_values = np.loadtxt(path, skiprows=1, delimiter=",").T
    # interpolate_and_compute_g(angle_values, beta_values)
    # print(calculate_assym(angle_values, beta_values))
    # angles = np.linspace(0, 181, 100000)
    # pf_hg = henvey_greenstein_pf(angles, 0.99)
    # interpolate_and_compute_g(angles, pf_hg)
    # create_executable_discretizer()
    # # run_executable_discretizer()
    # HE_angles, HE_beta = np.loadtxt('g0_90.txt').T
    #
    # angles = np.linspace(0, 180, 10000)
    # my_beta = henvey_greenstein_pf(phi=angles, g=0.90, normalize=True)
    # plt.plot(HE_angles, HE_beta)
    # plt.plot(angles, my_beta)
    # plt.show()
    # create_OTHG_discretized_files()
    # create_brine_discretized_files(angle_values, beta_values)
    create_OTHG2_discretized_files()