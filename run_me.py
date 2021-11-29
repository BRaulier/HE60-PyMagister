from pyHE60 import Simulation

if __name__ == "__main__":
    path_to_user_files = r'/Users/braulier/Documents/HE60/run/mobley'

    mobley_sim = Simulation(path=path_to_user_files, batch_name='Mobley_1998_example')
    mobley_sim.build_and_run_mobley_1998_example()
