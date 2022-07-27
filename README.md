# Analyse comparative des solvers

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
