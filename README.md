
# Introduction:

This workflow calculates the exchange coupling between magnetic ions for a specific (user-defined) pair. To calculate it, a four-state mapping analysis (FSMA) approach is used,  which relies on DFT based code total energy calculations. This approach considered one specific pair at a time in the supercell. 
 
For spin orbit coupling, we consider Heisenberg spin hamiltonian         

<a href="https://www.codecogs.com/eqnedit.php?latex=H&space;=&space;\sum_{i<j}&space;J_{ij}~&space;S_i&space;S_j" target="_blank"><img src="https://latex.codecogs.com/gif.latex?H&space;=&space;\sum_{i<j}&space;J_{ij}~&space;S_i&space;S_j" title="H = \sum_{i<j} J_{ij}~ S_i S_j" /></a>

The total energy of the system can then be written as
 E = J<sub>12</sub> **S** <sub>1</sub> **S**<sub>2</sub> + **S** <sub>1</sub> . **K** <sub>1</sub> + **S** <sub>2</sub> . **K** <sub>2</sub> 
<br />

<a href="https://www.codecogs.com/eqnedit.php?latex=K_1&space;=&space;\sum_{j&space;\neq&space;2}&space;J_{1j}~S_j" target="_blank"><img src="https://latex.codecogs.com/gif.latex?K_1&space;=&space;\sum_{j&space;\neq&space;2}&space;J_{1j}~S_j" title="K_1 = \sum_{j \neq 2} J_{1j}~S_j" /></a>
 
<a href="https://www.codecogs.com/eqnedit.php?latex=K_2&space;=&space;\sum_{j&space;\neq&space;1}&space;J_{2j}~S_j" target="_blank"><img src="https://latex.codecogs.com/gif.latex?K_2&space;=&space;\sum_{j&space;\neq&space;1}&space;J_{2j}~S_j" title="K_2 = \sum_{j \neq 1} J_{2j}~S_j" /></a>

Where, **S** <sub>1</sub> **S** <sub>2</sub> is the exchange coupling between site 1 and 2. While **S** <sub>i</sub> . **K** <sub>i</sub> represents the coupling between site i and all the magnetic sites different from 1 and 2. E<sub>0</sub> represents the contribution to the energy stemming from the interaction between sites 1 and 2 and all the other non-magnetic sites. Finally, J<sub>12</sub> is the exchange integral. 
In this approach, we consider the following collinear spin state

| State | S<sub>1</sub> | S<sub>2</sub> |
|:------:|:--------:|:--------:|
|   1   | (0,0,S) | (0,0,S)  | 
|   2   | (0,0,-S) | (0,0,S) | 
|   3   | (0,0,S) | (0,0,-S) | 
|   4   | (0,0,-S) | (0,0,-S)| 


The other spin states are kept fixed, according to the ground-state spin configuration. Using the above four combinations of spin states in the total energy equation we will get four linear equations of total energy given below

E<sub>1</sub> = J<sub>12</sub> S <sup>2</sup>  + **S** <sub>1</sub> . **K** <sub>1</sub> + **S** <sub>2</sub> . **K** <sub>2</sub> + E <sub>0</sub>
<br />
E<sub>2</sub> =  -J<sub>12</sub> S <sup>2</sup>  + **S** <sub>1</sub> . **K** <sub>1</sub> - **S** <sub>2</sub> . **K** <sub>2</sub> + E <sub>0</sub>
<br />
E<sub>3</sub> =  -J<sub>12</sub> S <sup>2</sup>  - **S** <sub>1</sub> . **K** <sub>1</sub> + **S** <sub>2</sub> . **K** <sub>2</sub> + E <sub>0</sub>
<br />
E<sub>4</sub> = J<sub>12</sub> S <sup>2</sup>  - **S** <sub>1</sub> . **K** <sub>1</sub> - **S** <sub>2</sub> . **K** <sub>2</sub> + E <sub>0</sub>

The solution of the above linear system of 4 equations is

J<sub>12</sub> = (E<sub>1</sub> - E<sub>2</sub> - E<sub>3</sub> + E<sub>4</sub>)/4S<sup>2</sup>)
Where J<sub>12</sub> is the exchange parameter. 

This method is pretty accurate when the supercell used for the calculation is large enough.

# How to Run

To use this workflow one has to configure the configuration.json file. In this file several  parameters have to be provided by the user to calculate exchange coupling for any material.
For example: 
* **chosenAtomPair:** choose a magnetic pair to calculate JIJ
* **crystal_vectors:** cell vectors (lattice parameters) 
* **numberOfAtoms:** number of atoms in the unit cell
  * **crystal_atoms:**
* **x_positions:** x positions of all the atoms in the unit cell separated by comma
* **y_positions:** y positions of all the atoms in the unit cell separated by comma
* **z_positions:** y positions of all the atoms in the unit cell separated by comma
* **atom_names:** atoms name separated by comma

* **calculationFactoryName:** “PWscf” executable of Quantum Espresso (e.g quantumespresso.pw)
* **code_name:** code@computername
* **pseudo_family_name:** pseudopotential library (default SSSP)
* **element_name:** Material name
* **spinCombinationLabels:** ["a", "b","c", "d"]
* **noOfSuperCells:** supercell number 

* **parameters:** Quantum espresso input parameters
* **compoundElement1:** name of first element (e.g Cr)
* **compoundElement2:**  name of first element (e.g I)
* **nSpinValue:**: nspin value of quantum espresso (default 2)
* **kPointsDict:**: provide K points corresponds to supercell in the increasing order

* **builder_metadata_label:** label of your calculation
* **builder_metadata_description:**: description of your calculation
* **builder_metadata_options_resources_machine:**: specify the number of machines(a.k.a. cluster nodes)
* **builder_metadata_options_max_wallclock_seconds:**: maximum time allowed for the calculation in seconds

After configuring the .json file the only thing you need to do is run the workflow.py file through verdi.
For example  verdi run workflow.py 
Once you run the workflow.py AiiDA will generate its workflow id. Use this workflow id in resultviewer.py file to view the result of the exchange coupling.

# Example: 
To test this workflow we have taken CrI3 monolayer as an example. In this system we have computed exchange coupling between atom1 (Cr1) and atom2 (Cr2) in the unit cell. 
```js
"chosenAtomPair": [1,2],
  "crystal_vectors": [
    [7.007940,0,0],
    [-3.503970,6.069054,0],
    [0,0,15.000000]
  ],
  "numberOfAtoms": 8,
  "crystal_atoms": {
      "x_positions": [3.503972,0.000000,0.981684,1.261132,-2.242816,-0.981684,2.242818,-1.261134],
      "y_positions": [2.023019,4.046038,6.069044,2.184372,3.884699,6.069046,3.884698,2.184371],
      "z_positions": [9.031769,9.031769,7.464880,7.464880,7.464880,10.598656,10.598656,10.598656],
      "atom_names": ["Cr","Cr","I","I","I","I","I","I"]
    },


  "calculationFactoryName": "quantumespresso.pw",
  "code_name": "qe_code@Acessiblecomputer",
  "pseudo_family_name": "SSSP",
  "element_name": "CrI3",
  "spinCombinationLabels": ["a", "b","c", "d"],
  "noOfSuperCells": 5,
  "parameters": {
    "CONTROL": {
      "calculation": "scf",
      "verbosity": "high",
      "tstress": true,
      "tprnfor": true
    },
    "SYSTEM": {
      "ecutwfc": 40,
      "ecutrho": 320,
      "occupations": "smearing",
      "smearing": "cold",
      "degauss": 0.00002
    },
    "ELECTRONS": {
      "electron_maxstep": 200,
      "conv_thr": 0.0000001,
      "mixing_beta": 0.7000000
    }
  },
  "compoundElement1": "Cr",
  "compoundElement2": "I",
  "nSpinValue": 2,

  "kPointsDict": {
    "1": [12, 12, 1],
    "2": [6, 6, 1],
    "3": [4, 4, 1],
    "4": [3, 3, 1],
    "5": [2, 2, 1]
  },

  "builder_metadata_label": "PW test",
  "builder_metadata_description": "My AiiDA calculation of Fe with Quantum ESPRESSO",
  "builder_metadata_options_resources_machine": 1,
  "builder_metadata_options_max_wallclock_seconds": 604800
}

```js

The computed J<sub>ij</sub> value for CrI3 is -2.73meV with an accuracy of 0.01 meV.

![Convergence of exchange coupling parameter(J<sub>12</sub>) with the size of supercell](https://github.com/[DI1504]/[myRepository]/blob/[master]/jijcalculation/jij.png ?raw=true)












































