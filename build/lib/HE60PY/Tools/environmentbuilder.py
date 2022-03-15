import os
import shutil
import subprocess
import numpy as np
import datetime


def create_irrad_file(wavelength_Ed, total_path):
    header = "\\begin_header\n" \
             "HydroLight standard format for total (Ed_total) Irradiance \n" \
             "Total irradiance includes sun + sky sea level irradiance\n" \
             "wavelength    Ed_total\n" \
             "(nm)    (W/m^2 nm)" \
             "\\end_header\n"
    footer = "\\end_data"
    with open(total_path, 'w+') as file:
        file.write(header)
        np.savetxt(file, wavelength_Ed, fmt='%1.9e', delimiter='\t')
        file.write(footer)

def create_null_pure_water_file(path):
    H2O_default_data = np.genfromtxt('/Applications/HE60.app/Contents/data/H2OabsorpTS.txt', skip_header=16, skip_footer=1)
    H2O_NULL_WATER_PROP = np.array(H2O_default_data, dtype=np.float16)
    H2O_NULL_WATER_PROP[:, 1], H2O_NULL_WATER_PROP[:, 2], H2O_NULL_WATER_PROP[:, 3] = 0.0, 0.0, 0.0
    header = "\\begin_header \n" \
             "This null pure water data file is used when simulating a non immersed in water medium using the \n" \
             "measured IOP option. This way, Hydro Light will add null IOP's when addind the water contribution to\n " \
             "the scattering and absorption. See section 2.7 of HydroLight technical documentation.\n" \
             "wavelen[nm]  aref[1/m]  PsiT[(1/m)/deg C] PsiS[(1/m)/ppt] \n" \
             "\\end_header\n"
    footer = "\\end_data"
    with open(path, 'w+') as file:
        file.write(header)
        np.savetxt(file, H2O_NULL_WATER_PROP, fmt='%1.5e', delimiter='\t')
        file.write(footer)


def create_null_water_file_if_needed():
    path_null_water_properties = "/Applications/HE60.app/Contents/data/null_H2Oabsorps.txt"
    if not os.path.isfile(path_null_water_properties):
        create_null_pure_water_file(path_null_water_properties)


class EnvironmentBuilder:
    def create_simulation_environnement(self):
        self.create_backscattering_file(self.path)
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
        header = "\\begin_header\n" \
                 "Backscattering file used to find a corresponding Fournier-Forand phase \n" \
                 "function. As described in https://www.oceanopticsbook.info/view/scattering/the-fournier-forand-phase-function\n" \
                 "Column headers (depth in m and bb in 1/m):\n" \
                 "depth {} ".format('\tbb'.join([str(int(i)) for i in self.wavelengths])) + "\n" \
                                                                                            "The first data record gives the number of wavelengths and the wavelengths.\n" \
                                                                                            "\\end_header\n"
        first_line = "{}\t{}\n".format(int(self.n_wavelengths), '\t'.join([str(i) for i in self.wavelengths]))
        footer = "\\end_data"
        with open(path + '/backscattering_file.txt', 'w') as file:
            file.write(header)
            file.write(first_line)
            np.savetxt(file, self.z_bb_grid, fmt='%1.5e', delimiter='\t')
            file.write(footer)

        shutil.copy(src=path + '/backscattering_file.txt',
                    dst=r'/Applications/HE60.app/Contents/data/phase_functions/HydroLight/user_defined/backscattering_file.txt')

    def create_ac9_file(self, path):
        header = "\\begin_header\n" \
                 "ac9 file used to describe the arbitrary chosen medium \n" \
                 "Column headers (depth in m; and and c in 1/m): \n" \
                 "depth {} {} ".format('a\t'.join([str(int(i)) for i in self.wavelengths]),
                                       '\tc'.join([str(int(i)) for i in self.wavelengths])) + "\n" \
                                                                                              "The first data record gives the number of wavelengths and the wavelengths.\n" \
                                                                                              "\\end_header\n"
        first_line = "{}\t{}\n".format(int(self.n_wavelengths), '\t'.join([str(i) for i in self.wavelengths]))
        footer = "\\end_data"
        with open(path + '/ac9_file.txt', 'w+') as file:
            file.write(header)
            file.write(first_line)
            np.savetxt(file, self.z_ac_grid, fmt='%1.9e', delimiter='\t')
            file.write(footer)



