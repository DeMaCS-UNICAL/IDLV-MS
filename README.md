# IDLV+MS
**IDLV+MS** is a new **ASP** system that integrates an efficient grounder, namely [**I-DLV**](https://github.com/DeMaCS-UNICAL/I-DLV/wiki), with an automatic solver selector: machine-learning techniques are applied for inductively choose the best solver, depending on some inherent features of the instantiation produced by I-DLV. 

I-DLV+MS currently supports the two state-of-the-art ASP solvers [**clasp**](https://github.com/potassco/clingo) and [**wasp**](https://github.com/alviano/wasp)

### Usage

In order to use I-DLV+MS just type:

```sh
$ cat filename | ./run PREDICATE_TO_FILTER
```
The parameter PREDICATE_TO_FILTER is a comma-separated list of output predicate names.

# Core Team
* [Francesco Calimeri](https://www.mat.unical.it/calimeri) 
* Davide Fuscà
* Simona Perri
* Jessica Zangari

For any problems or suggestions contact us at i-dlv@googlegroups.com.
