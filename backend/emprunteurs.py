import connection as c


class Emprunteurs:

    def __init__(self):
        pass

    def get_all(self):
        # On recupere tous les emprunteurs
        return c.request('select * from emprunteurs')

    def get(self, id):
        # On recupere un emprunteur en fonction de son id
        return c.request_with_params('select * from emprunteurs where id = ?', (id,))

    def create(self, nom):
        # On ajoute un emprunteur
        return c.request_with_params('insert into emprunteurs (nom) values (?)', (nom,))

    def update(self, id, nom):
        # On modifie un emprunteur
        return c.request_with_params('update emprunteurs set nom = ? where id = ?', (nom, id))

    def delete(self, id):
        # Avant de supprimer un emprunteur, on regarde si il a des emprunts en cours
        emprunts = self.get_emprunts(id)
        if len(emprunts) > 0:
            print("L'emprunteur a des emprunts en cours")
            return False
        else:
            # Si il n'a pas d'emprunts en cours, on le supprime
            return c.request_with_params('delete from emprunteurs where id = ?', (id,))

    def get_emprunts(self, id_emprunteur):
        # On recupere les emprunts d'un emprunteur
        return c.request_with_params('select * from emprunts where id_emprunteur = ?', (id_emprunteur,))

    def emprunter_livre(self, id_emprunteur, id_livre, date=None):
        # On vérifie si une date est passée en paramètre
        if date is None:
            # Si aucune date n'est passée en paramètre, on met la date du jour (défault en bdd)
            result = c.request_with_params('insert into emprunts (id_emprunteur, id_livre) values (?, ?)', (id_emprunteur, id_livre))
        else:
            # Si une date est passée en paramètre, on l'utilise
            result = c.request_with_params('insert into emprunts (id_emprunteur, id_livre, date) values (?, ?, ?)', (id_emprunteur, id_livre, date))

    def rendre_livre(self, id_emprunteur, id_livre):
        # On supprime l'emprunt
        return c.request_with_params('delete from emprunts where id_emprunteur = ? and id_livre = ?', (id_emprunteur, id_livre))