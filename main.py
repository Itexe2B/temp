import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from backend.genres import Genres
from backend.auteurs import Auteurs
from backend.emprunteurs import Emprunteurs
from backend.livres import Livres
from backend.emprunts import Emprunts
class MainWindow(QMainWindow):
    # TYPE_TABLE permet de savoir quelle table est actuellement affichée
    TYPE_TABLE = None

    # CONFIG_TABLE permet de configurer les noms des colonnes pour chaque table
    # L'utilisation du schema sql est plus propre mais plus compliquée à mettre en place
    CONFIG_TABLE = {
        'Auteurs': ['id', 'nom'],
        'Emprunteurs': ['id', 'nom'],
        'Emprunts': ['id', 'id_livre', 'id_emprunteur', 'date'],
        'Genres': ['id', 'nom'],
        'Livres': ['id', 'titre', 'id_auteur', 'id_genre']
    }

    def __init__(self):
        super().__init__()

        # Configuration de la fenêtre
        self.setWindowTitle("Gestion BDD")
        self.setGeometry(100, 100, 800, 600)

        # Ajout d'un QTableWidget (Datagrid) pour afficher les données
        self.table = QTableWidget(self)

        # Connecter le signal cellChanged au slot update_bdd pour mettre à jour la bdd
        # Lors du changement d'une cellule dans le tableau (QTableWidget) on appelle la fonction update_bdd
        self.table.cellChanged.connect(self.update_bdd)

        # Boutons pour ajouter et supprimer des lignes
        # On connecte les boutons à des fonctions pour ajouter et supprimer des lignes
        self.add_button = QPushButton("Ajouter", self)
        self.add_button.clicked.connect(self.add_row)
        self.delete_button = QPushButton("Supprimer", self)
        self.delete_button.clicked.connect(self.delete_row)


        # Ajout d'un menu
        self.menu = self.menuBar()
        # Ajout d'un menu Charger
        self.charger = QMenu("Charger", self)
        # Ajout des actions du menu Charger (Auteurs, Emprunteurs, Emprunts, Genres, Livres)
        self.auteurs = QAction("Auteurs", self)
        self.emprunteurs = QAction("Emprunteurs", self)
        self.emprunts = QAction("Emprunts", self)
        self.genres = QAction("Genres", self)
        self.livres = QAction("Livres", self)

        # On connecte les actions à des fonctions pour charger les données
        self.charger.addAction(self.auteurs)
        self.charger.addAction(self.emprunteurs)
        self.charger.addAction(self.emprunts)
        self.charger.addAction(self.genres)
        self.charger.addAction(self.livres)


        # On connecte les actions à des fonctions pour charger les données
        # On utilise une fonction lambda pour passer des paramètres à la fonction get_all
        # Une fonction lambda est une fonction temporaire
        self.auteurs.triggered.connect(lambda: self.get_all(Auteurs(), 'Auteurs'))
        self.emprunteurs.triggered.connect(lambda: self.get_all(Emprunteurs(), 'Emprunteurs'))
        self.emprunts.triggered.connect(lambda: self.get_all(Emprunts(), 'Emprunts'))
        self.genres.triggered.connect(lambda: self.get_all(Genres(), 'Genres'))
        self.livres.triggered.connect(lambda: self.get_all(Livres(), 'Livres'))

        # On ajoute le menu Charger au menu principal
        self.menu.addMenu(self.charger)

        # On charge les données de la table Auteurs par défaut
        self.get_all(Auteurs(), 'Auteurs')

        # Configuration du layout
        # QVBoxLayout permet de mettre les boutons et le tableau les uns en dessous des autres
        layout = QVBoxLayout()

        # QHBoxLayout permet de mettre les boutons côte à côte
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)

        # On ajoute le layout des boutons au layout principal
        layout.addLayout(button_layout)

        # On ajoute le tableau au layout principal
        layout.addWidget(self.table)

        # On ajoute le layout principal à un widget pour pouvoir l'afficher
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def get_all(self, classe, type_table):
        # On déconnecte le signal cellChanged pour éviter de mettre à jour la bdd lors du chargement des données
        self.table.cellChanged.disconnect(self.update_bdd)
        # On met à jour le type de table
        MainWindow.TYPE_TABLE = type_table
        # On met à jour le titre de la fenêtre
        self.setWindowTitle("Gestion BDD - " + type_table)
        # On récupère les données de la table
        result = classe.get_all()

        # On met à jour le tableau
        self.table.reset()
        # On met à jour le nombre de lignes et de colonnes
        self.table.setRowCount(len(result))
        self.table.setColumnCount(len(result[0]))

        # On met à jour les noms des colonnes
        self.table.setHorizontalHeaderLabels(self.CONFIG_TABLE.get(type_table))

        # On met à jour les données du tableau avec les données récupérées de la bdd
        for row in range(len(result)):
            for col in range(len(result[row])):
                self.table.setItem(row, col, QTableWidgetItem(str(result[row][col])))

        # On reconnecte le signal cellChanged pour mettre à jour la bdd en cas de changement de cellule
        self.table.cellChanged.connect(self.update_bdd)
        return True
    def add_row(self):
        # On ajoute une ligne vide au tableau en fonction du type de table
        # On utilise la fonction create de chaque classe pour ajouter une ligne
        # On utilise la fonction get_all pour recharger les données

        # L'ajout des données manquantes (puisque ligne vide) se fera dans la fonction update_bdd lors
        # du changement de la cellule (quand on aura fini de remplir la ligne)
        if MainWindow.TYPE_TABLE == 'Auteurs':
            Auteurs().create('')
            self.get_all(Auteurs(), 'Auteurs')
        elif MainWindow.TYPE_TABLE == 'Emprunteurs':
            Emprunteurs().create('')
            self.get_all(Emprunteurs(), 'Emprunteurs')
        elif MainWindow.TYPE_TABLE == 'Emprunts':
            Emprunteurs().emprunter_livre('', '')
            self.get_all(Emprunts(), 'Emprunts')
        elif MainWindow.TYPE_TABLE == 'Genres':
            Genres().create('')
            self.get_all(Genres(), 'Genres')
        elif MainWindow.TYPE_TABLE == 'Livres':
            Livres().create('', '', '')
            self.get_all(Livres(), 'Livres')
        else:
            raise('Type de table inconnu')

    def delete_row(self):
        # On supprime une ligne du tableau en fonction du type de table
        selected_row = self.table.currentRow()

        # On vérifie qu'une ligne est sélectionnée
        if self.table.currentRow() > -1:  # Si une ligne est sélectionnée
            first_cell = self.table.item(selected_row, 0)
            # On vérifie qu'une cellule est sélectionnée
            if not first_cell:
                raise ('Impossible de supprimer une ligne vide')
            # On utilise la fonction delete de chaque classe pour supprimer une ligne
            # On utilise la fonction get_all pour recharger les données
            if MainWindow.TYPE_TABLE == 'Auteurs':
                Auteurs().delete(first_cell.text())
                self.get_all(Auteurs(), 'Auteurs')
            elif MainWindow.TYPE_TABLE == 'Emprunteurs':
                Emprunteurs().delete(first_cell.text())
                self.get_all(Emprunteurs(), 'Emprunteurs')
            elif MainWindow.TYPE_TABLE == 'Emprunts':
                Emprunts().delete(first_cell.text())
                self.get_all(Emprunts(), 'Emprunts')
            elif MainWindow.TYPE_TABLE == 'Genres':
                Genres().delete(first_cell.text())
                self.get_all(Genres(), 'Genres')
            elif MainWindow.TYPE_TABLE == 'Livres':
                Livres().delete(first_cell.text())
                self.get_all(Livres(), 'Livres')
            else:
                raise ('Type de table inconnu')

    def update_bdd(self, row, column):
        # On met à jour la bdd en fonction du type de table
        # On récupère l'id de la ligne modifiée
        id = self.table.item(row, 0).text()

        # On utilise la fonction update de chaque classe pour mettre à jour une ligne
        # Inutile de recharger les données a ce moment la.
        if MainWindow.TYPE_TABLE == 'Auteurs':
            Auteurs().update(id, self.table.item(row, 1).text())
        elif MainWindow.TYPE_TABLE == 'Emprunteurs':
            Emprunteurs().update(id, self.table.item(row, 1).text())
        elif MainWindow.TYPE_TABLE == 'Emprunts':
            Emprunts().update(id, self.table.item(row, 1).text(), self.table.item(row, 2).text())
        elif MainWindow.TYPE_TABLE == 'Genres':
            Genres().update(id, self.table.item(row, 1).text())
        elif MainWindow.TYPE_TABLE == 'Livres':
            Livres().update(id, self.table.item(row, 1).text(), self.table.item(row, 2).text(), self.table.item(row, 3).text())
        else:
            raise ('Type de table inconnu')

if __name__ == "__main__":
    # On lance l'application
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())