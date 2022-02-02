from HE60PY.HE60_magister import AC9Simulation
import numpy as np
from tqdm import tqdm

if __name__ == "__main__":
    path_to_user_files = r'/Users/braulier/Documents/HE60/run/Light'
    ssl_list = np.linspace(0.01, 0.20, 20)

    for ssl_thickness in tqdm(ssl_list):
        ssl_thickness = round(ssl_thickness, 2)

    # Simulation example, as described in Mobley et al. 1998: MODELING LIGHT PROPAGATION IN SEA ICE
    # mobley_sim = AC9Simulation(path=path_to_user_files, batch_name='Mobley_1998_example')
    # mobley_sim.build_and_run_mobley_1998_example()

        # Bonnie Light 3 layers example with constant absorption (0.4)
        user_built_sim = AC9Simulation(path=path_to_user_files, batch_name='BL_ssl_{}'.format(str(ssl_thickness).replace('.', '_')))
        user_built_sim.set_z_grid(z_max=1.25)
        user_built_sim.add_layer(z1=0.0, z2=ssl_thickness, abs=0.4, scat=1700, bb=0.0132)
        user_built_sim.add_layer(z1=ssl_thickness, z2=0.30, abs=0.4, scat=250, bb=0.0132)
        user_built_sim.add_layer(z1=0.30, z2=1.26, abs=0.4, scat=16, bb=0.0132)     # last z2 must be greater then z_max
        user_built_sim.run_built_model()
