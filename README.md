# Analyse comparative des solveurs

Projet IRL réalisé par Léa Petit-Jean Genat sous l'encadrement de Nadia Brauner en collaboration avec Cléophée Robin.
Le rapport détaillé s'intitule `lea_irl_rapport.pdf`.
Ce répertoire a pour objectif de montrer le code des différents modèles réalisés pendant ce stage.

Pour faire fonctionner le programme, il faut installer les modules Python :

* [docplex](https://pypi.org/project/docplex/)

* [ortools](https://developers.google.com/optimization/install/)

* [localsolver](https://www.localsolver.com/download.html/)

Il est peut-être nécessaire d'installer d'autres modules comme [matplolib](https://matplotlib.org/stable/users/installing/index.html) ou [pandas](https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html) selon les utilisations.

Le programme principal est `main.py`, il fournit des actions de base mais pour faire des expérimentations spécifiques,
il faut modifier le code.

Pour fonctionner, les instances du problème doivent être de la forme :
```
n = 2;  
r = [0, 0];  
deadline = [4, 4];  
p = [2, 2];  
d = [1, 3];  
w = [3, 1];
```
Les modèles CPO et LocalSolver ont été verifiés respectivement par Hadrien Cambazard et Julien Darlay.

# Comparative analysis of solvers

Léa Petit-Jean Genat introduction to research project under the supervision of Nadia Brauner and Cléophée Robin.
The intership report is `lea_irl_rapport.pdf` but is written in French.
This repertory is designed to show the differents models made during the intership.

To run the program, you need to install the following Python modules :

* [docplex](https://pypi.org/project/docplex/)

* [ortools](https://developers.google.com/optimization/install/)

* [localsolver](https://www.localsolver.com/download.html/)

It may be necessary to install other modules like [matplolib](https://matplotlib.org/stable/users/installing/index.html) or [pandas](https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html) depending on the use. 

The main program is `main.py` and it gives the basic actions but to do specific experiments, you have to modify the code.

To work, the problem data must be structured as :
```
n = 2;  
r = [0, 0];  
deadline = [4, 4];  
p = [2, 2];  
d = [1, 3];  
w = [3, 1];
```
Hadrien Cambazard and Julien Darlay have respectively verified the CPO and LocalSolver models. 
