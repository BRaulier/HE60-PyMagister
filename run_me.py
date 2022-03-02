from HE60PY.ac9simulation import AC9Simulation


if __name__ == "__main__":
    path_to_user_files = r'/Users/braulier/Documents/HE60/run/mobley'

    mobley_sim = AC9Simulation(path=path_to_user_files, run_title='test', root_name='Mobley_1998_example', mode='sea_ice', Nwavel=17)
    mobley_sim.build_and_run_mobley_1998_example()

    # user_built_sim = AC9Simulation(path=path_to_user_files, batch_name='user_built_example')
    # user_built_sim.set_z_grid(z_max=2.0)
    # user_built_sim.add_layer(z1=0.0, z2=0.5, abs=0.5, scat=1000, bb=0.0109)
    # user_built_sim.add_layer(z1=0.5, z2=2.01, abs=0.4, scat=200, bb=0.0042)
    # user_built_sim.run_built_model(printOutput=True)