import os
import shutil
import subprocess
import numpy as np
import datetime

from .olympus import ThisNeedToExist
from . import header_library


def create_irrad_file(wavelength_Ed, total_path):
    header, footer = header_library.irrad()
    with open(total_path, 'w+') as file:
        file.write(header)
        np.savetxt(file, wavelength_Ed, fmt='%1.9e', delimiter='\t')
        file.write(footer)


def create_null_pure_water_file(path):
    H2O_default_data = np.genfromtxt('/Applications/HE60.app/Contents/data/H2OabsorpTS.txt', skip_header=16, skip_footer=1)
    H2O_NULL_WATER_PROP = np.array(H2O_default_data, dtype=np.float16)
    H2O_NULL_WATER_PROP[:, 1], H2O_NULL_WATER_PROP[:, 2], H2O_NULL_WATER_PROP[:, 3] = 0.0, 0.0, 0.0
    header, footer = header_library.null_water()
    with open(path, 'w+') as file:
        file.write(header)
        np.savetxt(file, H2O_NULL_WATER_PROP, fmt='%1.5e', delimiter='\t')
        file.write(footer)


def create_null_water_file_if_needed():
    path_null_water_properties = "/Applications/HE60.app/Contents/data/null_H2Oabsorps.txt"
    if not os.path.isfile(path_null_water_properties):
        create_null_pure_water_file(path_null_water_properties)

# def create_inert_surface_file():



class EnvironmentBuilder:
    def create_simulation_environnement(self):
        if self.whoamI == 'AC9Simulation':
            self.create_backscattering_file(self.path)
            self.create_ac9_file(self.path)

        elif self.whoamI == 'SeaIceSimulation':
            self.create_dddpf_file(folder_path='/Applications/HE60.app/Contents/data/phase_functions/')
            self.create_ac9_file(self.path)
        create_null_water_file_if_needed()

    def create_run_delete_bash_file(self, print_output):
        time_stamp = str(datetime.datetime.now()).replace('.', '_').replace(' ', '_').replace(':', '_')
        bash_file_path = f"/Applications/HE60.app/Contents/backend/{time_stamp}.sh"
        with open(bash_file_path, "w+") as file:
            file.write("#!/bin/bash\n"
                       f"./HydroLight6 < {self.usr_path}/Documents/HE60/run/batch/{self.root_name}.txt")
        bash_command = f'./{time_stamp}.sh'
        path_to_he60 = '/Applications/HE60.app/Contents/backend'
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
        os.remove(bash_file_path)

    def create_backscattering_file(self, path):
        header, footer = header_library.backscattering_file(self.wavelengths)
        with open(path + '/backscattering_file.txt', 'w') as file:
            file.write(header)
            np.savetxt(file, self.z_bb_grid, fmt='%1.5e', delimiter='\t')
            file.write(footer)

        shutil.copy(src=path + '/backscattering_file.txt',
                    dst=r'/Applications/HE60.app/Contents/data/phase_functions/HydroLight/user_defined/backscattering_file.txt')

    def create_ac9_file(self, path):
        header, footer = header_library.ac9_file(self.wavelengths)
        with open(path + '/ac9_file.txt', 'w+') as file:
            file.write(header)
            np.savetxt(file, self.z_ac_grid, fmt='%1.9e', delimiter='\t')
            file.write(footer)
            
    def create_dddpf_file(self, folder_path):
        
        with open(folder_path + 'Py_DDDPF_list.txt', 'w+') as file:
            self.hermes.get['z_boundaries_dddpf'] = self.z_boundaries_dddpf
            self.hermes.get['dpf_filenames'] = self.dpf_filenames
            for i, boundary in enumerate(self.z_boundaries_dddpf):
                dpf_filename = self.dpf_filenames[i]
                # First verify that this boundary is different then the previous one, to avoid error from user input
                if i != 0 and np.isclose(self.z_boundaries_dddpf[i-1], boundary, atol=1e-6):
                    boundary += 0.00001         # To avoid two boundaries that are equals to each other.
                # Verify that the dpf file the user gave exists, if it does not, an error is raised
                ThisNeedToExist(path=f'{folder_path}HydroLight/{dpf_filename}')
                file.write(f"{boundary:.5f}    {dpf_filename}\n")



