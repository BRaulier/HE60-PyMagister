# HE60-PyMagister:

PyMagister is a Python interface of Hydro Light MacOS version. It is useful to bypass the graphic user interface of 
HydroLight. It is then possible to run many simulations without any human intervention. This Python interface
is also intented to work with a modified version of HydroLight that includes a "SeaIceIOP" mode. This homemade mode
enables the use of depth dependant discretized phase function (dddpf). 


Please note that knowledge of
HydroLight is necessary in order to fully exploit the features of this interface.

## Instructions:

Open _run_me.py_ to run (Mobley et al. 1998) and user built geometry examples.

### What HE60-PyMagister can do:
In "sea_ice" mode:
1. Create arbitrary IOP (absorption(z), scattering(z), bb(z)) profiles as they would have been measured with an ac9 profile.
2. Create automatically batch files
3. Create and run a bash (.sh) file to execute Hydro Light

In "Lisa"'s mode:
1. Load ac9 and Chla field profiles
3. Create automatically batch files
4. Create and run a bash (.sh) file to execute Hydro Light

### Classes calling scheme used in HE60-PyMagister
![image info](./ressources/pymagister_scheme.png)

For questions and comments please see Bastian Raulier ( [Takuvik Joint International Team](http://www.takuvik.ulaval.ca/), Université Laval) [contact](mailto:bastian.raulier.1@ulaval.ca). 

## Acknowledgements
I would like to thank Dr John Hedley, founder of [Numerical Optics Ltd](https://www.numopt.com/index.html), who was very generous in answering my many questions about Hydro Light and its operation. 

