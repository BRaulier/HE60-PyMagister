import numpy as np
import os
import subprocess
import matplotlib.pyplot as plt
from scipy.integrate import quad


def henvey_greenstein_pf(phi_deg, g):
    phi_rad = phi_deg*np.pi/180
    mu = np.cos(phi_rad)
    beta = (1/(4*np.pi))*((1-g**2)/(1+g**2-2*g*mu)**(3/2))
    return beta


def create_tabulated_file(angle_beta_array, tab_filename, pf_type):
    path = '/Applications/HE60.app/Contents/source_code/Phase_Function_code/PF_user_data/Py_Magister_PF/'+tab_filename+'.txt'
    header = "/begin_header \n" \
             "{} phase function \n"\
             "This file is on the HSF95 format for phase function discretization. \n" \
             "deg   1/(m sr)\n" \
             "/end_header\n" \
             "1.00\n".format(pf_type)
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
    cmd = ['sudo', './make_PFdiscretization6.sh']
    if os.path.isfile(path+'/make_PFdiscretization6.sh'):
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



if __name__ == '__main__':
    # create_executable_discretizer()
    # # run_executable_discretizer()
    # HE_angles, HE_beta = np.loadtxt('g0_90.txt').T
    #
    # angles = np.linspace(0, 180, 10000)
    # my_beta = henvey_greenstein_pf(phi=angles, g=0.90, normalize=True)
    # plt.plot(HE_angles, HE_beta)
    # plt.plot(angles, my_beta)
    # plt.show()
    create_OTHG_discretized_files()

