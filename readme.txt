pip install -r requirements.txt
py main.py

si pip non reconnue :
py -m pip install -r requirements.txt
py main.py



Explications :
Chaque table est représentée par une classe pour simuler un ORM (Object Relational Mapping).
On "map" chaque table à notre objet afin de pouvoir faire des opérations SQL basiques dessus.

Une fois toutes les opérations communes implémentées CRUD - Create Read Update Delete, on peut commencer à faire
l'interface graphique appelant alors nos méthodes implémentées dans chaque objet.

Au niveau de l'interface graphique, on fait quelque chose de simple.
Un layout vertical contenant un layout horizontal pour nos boutons ajouter et supprimer ;
et une datagrid pour afficher les données de la table et l'utiliser comme interface de modification.

Après avoir créé les layouts, boutons et datagrid, on les ajoute à notre fenêtre principale.
Une fois les événements connectés, il nous reste à brancher le côté "backend" à notre "frontend".

Ce style d'architecture est très simple et permet de faire des applications très rapidement.
Cependant, il est très limité et ne permet pas de faire des applications complexes (pas de décomposition du frontend).
Il peut s'inscrire dans une architecture micro-service où chaque élément du backend (auteurs, livres, emprunts, etc.)
est un micro-service qui peut être appelé par une application ce qui permet une grande flexibilitée.