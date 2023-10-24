import connection as c


class Livres:
    def __init__(self):
        pass

    def get_all(self):
        # On recupere tous les livres
        return c.request('select * from livres')

    def get(self, id):
        # On recupere un livre en fonction de son id
        return c.request_with_params('select * from livres where id = ?', (id,))

    def create(self, titre, id_auteur, id_genre):
        # On ajoute un livre
        return c.request_with_params('insert into livres (titre, id_auteur, id_genre) values (?, ?, ?)', (titre, id_auteur, id_genre))

    def update(self, id, titre, id_auteur, id_genre):
        # On modifie un livre
        return c.request_with_params('update livres set titre = ?, id_auteur = ?, id_genre = ? where id = ?', (titre, id_auteur, id_genre, id))

    def delete(self, id):
        # Avant de supprimer un livre, on regarde si il a des emprunts en cours
        emprunts = self.get_emprunts(id)
        if len(emprunts) > 0:
            print("Le livre a des emprunts en cours")
            return False
        else:
            # Si il n'a pas d'emprunts en cours, on le supprime
            return c.request_with_params('delete from livres where id = ?', (id,))

    def get_by_auteur(self, id_auteur):
        # On recupere les livres d'un auteur
        return c.request_with_params('select * from livres where id_auteur = ?', (id_auteur,))

    def get_by_genre(self, id_genre):
        # On recupere les livres d'un genre
        return c.request_with_params('select * from livres where id_genre = ?', (id_genre,))

    def get_emprunts(self, id_livre):
        # On recupere la liste d'emprunts associée à un livre
        return c.request_with_params('select * from emprunts where id_livre = ?', (id_livre,))
