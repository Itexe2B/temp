import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from backend.genres import Genres
from backend.auteurs import Auteurs
from backend.emprunteurs import Emprunteurs
from backend.livres import Livres
from backend.emprunts import Emprunts
class MainWindow(QMainWindow):
    TYPE_TABLE = None
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

        # Ajout d'un QTableWidget
        self.table = QTableWidget(self)

        # Connecter le signal cellChanged au slot update_bdd
        self.table.cellChanged.connect(self.update_bdd)

        # Boutons pour ajouter et supprimer des lignes
        self.add_button = QPushButton("Ajouter", self)
        self.add_button.clicked.connect(self.add_row)
        self.delete_button = QPushButton("Supprimer", self)
        self.delete_button.clicked.connect(self.delete_row)


        # Ajout d'un menu
        self.menu = self.menuBar()
        self.charger = QMenu("Charger", self)
        self.auteurs = QAction("Auteurs", self)
        self.emprunteurs = QAction("Emprunteurs", self)
        self.emprunts = QAction("Emprunts", self)
        self.genres = QAction("Genres", self)
        self.livres = QAction("Livres", self)

        self.charger.addAction(self.auteurs)
        self.charger.addAction(self.emprunteurs)
        self.charger.addAction(self.emprunts)
        self.charger.addAction(self.genres)
        self.charger.addAction(self.livres)



        self.auteurs.triggered.connect(lambda: self.get_all(Auteurs(), 'Auteurs'))
        self.emprunteurs.triggered.connect(lambda: self.get_all(Emprunteurs(), 'Emprunteurs'))
        self.emprunts.triggered.connect(lambda: self.get_all(Emprunts(), 'Emprunts'))
        self.genres.triggered.connect(lambda: self.get_all(Genres(), 'Genres'))
        self.livres.triggered.connect(lambda: self.get_all(Livres(), 'Livres'))

        self.menu.addMenu(self.charger)

        self.get_all(Auteurs(), 'Auteurs')

        # Configuration du layout
        layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
        layout.addLayout(button_layout)
        layout.addWidget(self.table)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def get_all(self, classe, type_table):
        self.table.cellChanged.disconnect(self.update_bdd)
        MainWindow.TYPE_TABLE = type_table
        self.setWindowTitle("Gestion BDD - " + type_table)
        result = classe.get_all()
        self.table.reset()
        self.table.setRowCount(len(result))
        self.table.setColumnCount(len(result[0]))
        self.table.setHorizontalHeaderLabels(self.CONFIG_TABLE.get(type_table))
        for row in range(len(result)):
            for col in range(len(result[row])):
                self.table.setItem(row, col, QTableWidgetItem(str(result[row][col])))
        self.table.cellChanged.connect(self.update_bdd)


        return True
    def add_row(self):
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
        selected_row = self.table.currentRow()
        if self.table.currentRow() > -1:  # Si une ligne est sélectionnée
            first_cell = self.table.item(selected_row, 0)
            if not first_cell:
                raise ('Impossible de supprimer une ligne vide')

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
        id = self.table.item(row, 0).text()
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
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())