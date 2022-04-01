from HE60PY.ac9simulation import AC9Simulation
from HE60PY.seaicesimulation import SeaIceSimulation
from HE60PY.data_manager import DataFinder

if __name__ == "__main__":
    path_to_user_files = r'/Users/braulier/Documents/HE60/run'
    #
    # mobley_sim = AC9Simulation(path=path_to_user_files, run_title='test', root_name='Mobley_1998_example', mode='sea_ice')
    # mobley_sim.build_and_run_mobley_1998_example()
    # mobley_results = DataFinder(mobley_sim.hermes)
    # results = mobley_results.get_Eudos_lambda()
    # results.to_csv('TEMPORARY_example_results.txt')

    user_built_sim =SeaIceSimulation(path=path_to_user_files, run_title='test', Nwave=2,
                                   root_name='simple_built_example', mode='sea_ice'
                                   ,iIOPmodel=6, _5g_line2 = '4,0,550,0.01,0')
    user_built_sim.set_z_grid(z_max=2.0)
    user_built_sim.add_layer(z1=0.0, z2=0.10, abs=0.5, scat=100, dpf='dpf_OTHG_0_98.txt')
    user_built_sim.add_layer(z1=0.10, z2=0.5, abs=0.5, scat=100, dpf='dpf_OTHG_0_98.txt')
    user_built_sim.add_layer(z1=0.5, z2=2.01, abs=0.4, scat=200, dpf='dpf_OTHG_0_98.txt')
    user_built_sim.run_simulation(printoutput=True)

    # wavelength_abs_built_sim = AC9Simulation(path=path_to_user_files, run_title='test', root_name='abs_example', mode='HE60DORT')
    # wavelength_abs_built_sim.set_z_grid(z_max=2.0, wavelength_list=[484, 544, 602])
    # wavelength_abs_built_sim.add_layer(z1=0.0, z2=0.5, abs={'484': 0.0430, '544': 0.0683, '602': 0.12}, scat=1000, bb=0.0109)
    # wavelength_abs_built_sim.add_layer(z1=0.5, z2=2.01, abs={'484': 0.0430, '544': 0.0683, '602': 0.12}, scat=200, bb=0.0042)
    # wavelength_abs_built_sim.run_simulation(printoutput=True)



    # for station_file_name in station_file_names:
    #     for input_file in input_files:
    #         lisa_sim = AC9Simulation(path=path_to_user_files,
    #                                  mode='Lisa',
    #                                  root_name='RG100od_C10',
    #                                  run_title='Chl a profiles based on real data: b - baseline, 10 - 10% to 100 - 100% ',
    #                                  station_filename='RG100od',
    #                                  ac9_filename='aActot_homChl10.txt',
    #                                  chlaz_filename='Chlaz_homChl10.txt')
    #         lisa_sim.run_simulation(printoutput=True)
