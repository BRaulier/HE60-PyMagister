from HE60_magister import Simulation

if __name__ == "__main__":
    path_to_user_files = r'/Users/braulier/Documents/HE60/run/mobley'

    # Simulation example, as described in Mobley et al. 1998: MODELING LIGHT PROPAGATION IN SEA ICE
    mobley_sim = Simulation(path=path_to_user_files, batch_name='Mobley_1998_example')
    mobley_sim.build_and_run_mobley_1998_example()

    # User built example
    user_built_sim = Simulation(path=path_to_user_files, batch_name='user_built_example')
    user_built_sim.set_z_grid(z_max=1.0)
    user_built_sim.add_layer(z1=0.0, z2=0.1, abs=0.5, scat=1000, bb=0.0109)
    user_built_sim.add_layer(z1=0.1, z2=1.01, abs=0.4, scat=200, bb=0.0042)
    user_built_sim.run_built_model(printOutput=True)
