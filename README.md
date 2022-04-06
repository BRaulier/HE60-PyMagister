# HE60-PyMagister:

PyMagister is a Python interface of Hydro Light MacOS version. It is useful to bypass the graphic user interface of 
HydroLight. It is then possible to run many simulations without any human intervention. This Python interface
is also intented to work with a modified version of HydroLight that includes a "SeaIceIOP" mode. This homemade mode
enables the use of depth dependant discretized phase function (dddpf). 


Please note that knowledge of
HydroLight is necessary in order to fully exploit the features of this interface.

## Installation

Download zip file and use the package manager [pip](https://pip.pypa.io/en/stable/) to install package.
```bash
 pip3 install [path/to/extracted/zip]
```
## Classes calling scheme
![image info](./ressources/pymagister_scheme.png)
### SeaIceSimulation
#### Examples
```python
from HE60PY.seaicesimulation import SeaIceSimulation
simple_example_SeaIce =SeaIceSimulation(run_title='simple_example_SeaIce', 
                                        root_name='simple_example_SeaIce')
simple_example_SeaIce.set_z_grid(z_max=2.0)
simple_example_SeaIce.add_layer(z1=0.0, z2=0.10, abs=0.5, scat=100, dpf='dpf_OTHG_0_98.txt')
simple_example_SeaIce.add_layer(z1=0.10, z2=0.5, abs=0.5, scat=100, dpf='dpf_OTHG_0_98.txt')
simple_example_SeaIce.add_layer(z1=0.5, z2=2.01, abs=0.4, scat=200, dpf='dpf_OTHG_0_98.txt')
simple_example_SeaIce.run_simulation(printoutput=True)
```

```python
from HE60PY.seaicesimulation import SeaIceSimulation
example_SeaIce = SeaIceSimulation(run_title='example_SeaIce', 
                                  root_name='example_SeaIce')
example_SeaIce.set_z_grid(z_max=3.00, wavelength_list=[484, 544, 602])
example_SeaIce.add_layer(z1=0.0, z2=0.20, abs={'484': 0.0430, '544': 0.0683, '602': 0.12}, scat=2277, dpf='dpf_OTHG_0_95.txt')
example_SeaIce.add_layer(z1=0.20, z2=0.80, abs={'484': 0.0430, '544': 0.0683, '602': 0.12}, scat=303, dpf='dpf_OTHG_0_98.txt')
example_SeaIce.add_layer(z1=0.80, z2=2.00, abs={'484': 0.0430, '544': 0.0683, '602': 0.12}, scat=79, dpf='dpf_OTHG_0_98.txt')
example_SeaIce.add_layer(z1=2.0, z2=3.01, abs={'484': 1.36e-2, '544': 5.11e-2, '602': 2.224e-1}, scat=0.1, dpf='dpf_OTHG_0_98.txt')
example_SeaIce.run_simulation(printoutput=True)
```

### AC9Simulation
#### Calling example


## Acknowledgements
I would like to thank Dr John Hedley, founder of [Numerical Optics Ltd](https://www.numopt.com/index.html), who was very generous in answering my many questions about Hydro Light and its operation. 

For questions and comments please see Bastian Raulier, [Takuvik Joint International Team](http://www.takuvik.ulaval.ca/), Université Laval, Quebec City, [contact](mailto:bastian.raulier.1@ulaval.ca). 
