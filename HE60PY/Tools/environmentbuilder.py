import os
import shutil
import subprocess
import numpy as np
import datetime

from HE60PY.Tools.olympus import ThisNeedToExist
from HE60PY.Tools import header_library
from HE60PY.Tools.path import Path

_path = Path()
path_to_HE60 = _path.to_HE60


def create_irrad_file(wavelength_Ed, total_path):
    header, footer = header_library.irrad()
    with open(total_path, 'w+') as file:
        file.write(header)
        np.savetxt(file, wavelength_Ed, fmt='%1.9e', delimiter='\t')
        file.write(footer)
    ThisNeedToExist(total_path)


def create_null_pure_water_file(path):
    H2O_default_data = np.genfromtxt(f'{path_to_HE60}/Contents/data/H2OabsorpTS.txt', skip_header=16, skip_footer=1)
    H2O_NULL_WATER_PROP = np.array(H2O_default_data, dtype=np.float16)
    H2O_NULL_WATER_PROP[:, 1], H2O_NULL_WATER_PROP[:, 2], H2O_NULL_WATER_PROP[:, 3] = 0.0, 0.0, 0.0
    header, footer = header_library.null_water()
    with open(path, 'w+') as file:
        file.write(header)
        np.savetxt(file, H2O_NULL_WATER_PROP, fmt='%1.5e', delimiter='\t')
        file.write(footer)


def create_null_water_file_if_needed():
    path_null_water_properties = f"{path_to_HE60}/Contents/data/null_H2Oabsorps.txt"
    if not os.path.isfile(path_null_water_properties):
        create_null_pure_water_file(path_null_water_properties)

def create_inert_surface_file():
    path_inert_surface_file = f"{path_to_HE60}/Contents/data/sea_surfaces/HydroLight/CoxMunk_iso/surface_1000.0"
    t = np.ravel(np.diag(np.diag(np.ones((130,130)))))
    r = np.ravel(np.zeros((130,130)).ravel())
    header, footer = header_library.surface_file()
    with open(path_inert_surface_file, 'w+') as file:
        file.write(header)
        format = '   %1.5E0'
        np.savetxt(file, [t[i*10:(i+1)*10].T for i in range(1690)], fmt=format, delimiter='') # that1
        np.savetxt(file, [t[i*10:(i+1)*10].T for i in range(1690)], fmt=format, delimiter='') # that1
        np.savetxt(file, [r[i*10:(i+1)*10].T for i in range(1690)], fmt=format, delimiter='') # that1
        np.savetxt(file, [r[i*10:(i+1)*10].T for i in range(1690)], fmt=format, delimiter='') # that1
        np.savetxt(file, [t[i*10:(i+1)*10].T for i in range(1690)], fmt=format, delimiter='') # that1
        np.savetxt(file, [t[i*10:(i+1)*10].T for i in range(1690)], fmt=format, delimiter='') # that1
        np.savetxt(file, [r[i*10:(i+1)*10].T for i in range(1690)], fmt=format, delimiter='') # that1
        np.savetxt(file, [r[i*10:(i+1)*10].T for i in range(1690)], fmt=format, delimiter='') # that1

        file.write(footer)

def load_surface_file(surface_filename="surface_1000.0", skip_header=5):
    path = f"{path_to_HE60}/Contents/data/sea_surfaces/HydroLight/CoxMunk_iso/" + surface_filename
    unshaped_surface_matrix = np.genfromtxt(path, skip_header=skip_header, skip_footer=1)
    return unshaped_surface_matrix

def save_surface_file(surface_matrix, surface_filename="surface_1000.0"):
    path = f"{path_to_HE60}/Contents/data/sea_surfaces/HydroLight/CoxMunk_iso/" + surface_filename
    header, footer = header_library.surface_file()
    with open(path, 'w+') as file:
        file.write(header)
        np.savetxt(file, surface_matrix, fmt='   %1.5E0', delimiter='')
        file.write(footer)
    ThisNeedToExist(path)



class EnvironmentBuilder:
    def create_simulation_environnement(self):
        if self.whoamI == 'AC9Simulation':
            self.create_backscattering_file(self.path)
            self.create_ac9_file(self.ac9_path )

        elif self.whoamI == 'SeaIceSimulation':
            self.create_dddpf_file(folder_path=f'{path_to_HE60}/Contents/data/phase_functions/')
            self.create_ac9_file(self.ac9_path )
        create_null_water_file_if_needed()

    def create_run_delete_bash_file(self, print_output):
        time_stamp = str(datetime.datetime.now()).replace('.', '_').replace(' ', '_').replace(':', '_')
        bash_file_path = f"{path_to_HE60}/Contents/backend/{time_stamp}.sh"
        with open(bash_file_path, "w+") as file:
            file.write("#!/bin/bash\n"
                       f"./HydroLight6 < {self.usr_path}/Documents/HE60/run/batch/{self.root_name}.txt")
        bash_command = f'./{time_stamp}.sh'
        path_to_he60 = f'{path_to_HE60}/Contents/backend'
        command_chmod = 'chmod u+x ' + bash_file_path
        chmod_process = subprocess.Popen(command_chmod.split(), stdout=subprocess.PIPE)
        chmod_process.communicate()
        HE60_process = subprocess.Popen(bash_command, stdout=subprocess.PIPE, cwd=path_to_he60, bufsize=1,
                                        universal_newlines=True)
        if print_output:
            with HE60_process as p:
                for line in p.stdout:
                    print(line, end='')
        else:
            HE60_process.communicate()
        # os.remove(bash_file_path)
        # os.remove(self.ac9_path)

    def create_backscattering_file(self, path):
        header, footer = header_library.backscattering_file(self.wavelengths)
        with open(path + '/backscattering_file.txt', 'w') as file:
            file.write(header)
            np.savetxt(file, self.z_bb_grid, fmt='%1.5e', delimiter='\t')
            file.write(footer)
        _path_to_HE60 = f"{path_to_HE60}/Contents/data/phase_functions/HydroLight/user_defined/"
        shutil.copy(src=path + '/backscattering_file.txt',
                    dst=_path_to_HE60+'backscattering_file.txt')

    def create_ac9_file(self, path):
        header, footer = header_library.ac9_file(self.wavelengths)
        with open(path, 'w+') as file:
            file.write(header)
            np.savetxt(file, self.z_ac_grid, fmt='%1.9e', delimiter='\t')
            file.write(footer)
            
    def create_dddpf_file(self, folder_path):
        with open(folder_path + 'Py_DDDPF_list.txt', 'w+') as file:
            self.hermes.get['z_boundaries_dddpf'] = self.z_boundaries_dddpf
            self.hermes.get['dpf_filenames'] = self.dpf_filenames
            boundaries, assym_coeff = [], []

            for i, (boundary, dpf_filename) in enumerate(zip(self.z_boundaries_dddpf, self.dpf_filenames)):
                # First verify that this boundary is different then the previous one, to avoid error from user input
                if i != 0 and np.isclose(self.z_boundaries_dddpf[i-1], boundary, atol=1e-6):
                    boundary += 0.00001         # To avoid two boundaries that are equals to each other.
                # Verify that the dpf file the user gave exists, if it does not, an error is raised
                ThisNeedToExist(path=f'{folder_path}HydroLight/{dpf_filename}')
                file.write(f"{boundary:.5f}    {dpf_filename}\n")
                boundaries.append(boundary)
            for dpf_obj in self.dpf_objects:
                try:
                    mean_cosine = dpf_obj.moment(n=1) # assymetry g parameter will not be computed if a filename has been passed instead of the class instance
                    assym_coeff.append(mean_cosine)
                except:
                    assym_coeff.append(999)
                    print('Warning: Asymmetry coefficient could not be compiled in the results because the phase functions'
                          'was provided with a string instead of the class. ')

            self.hermes.get['dpf_boundaries_table'] = [boundaries, assym_coeff] # store results if results succeeded.


if __name__ == "__main__":
    john_surface_file = load_surface_file(surface_filename="john_surface_1000.0")
    bastian_surface_file = load_surface_file(surface_filename="#surface_1000.0", skip_header=7)
    john_surface_file[john_surface_file < 0.1] = 0.0
    print(john_surface_file.sum(), bastian_surface_file.sum())
    save_surface_file(john_surface_file, surface_filename="surface_1001.0")
    save_surface_file(bastian_surface_file, surface_filename="surface_1000.0")
    # create_inert_surface_file()
    current_surface_file = load_surface_file(surface_filename="surface_1000.0", skip_header=7)
    print("current surface file",current_surface_file.sum())