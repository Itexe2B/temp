import connection as c


class Livres:
    def __init__(self):
        pass

    def get_all(self):
        return c.request('select * from livres')

    def get(self, id):
        return c.request_with_params('select * from livres where id = ?', (id,))

    def create(self, titre, id_auteur, id_genre):
        return c.request_with_params('insert into livres (titre, id_auteur, id_genre) values (?, ?, ?)', (titre, id_auteur, id_genre))

    def update(self, id, titre, id_auteur, id_genre):
        return c.request_with_params('update livres set titre = ?, id_auteur = ?, id_genre = ? where id = ?', (titre, id_auteur, id_genre, id))

    def delete(self, id):
        emprunts = self.get_emprunts(id)
        if len(emprunts) > 0:
            print("Le livre a des emprunts en cours")
            return False
        else:
            return c.request_with_params('delete from livres where id = ?', (id,))

    def get_by_auteur(self, id_auteur):
        return c.request_with_params('select * from livres where id_auteur = ?', (id_auteur,))

    def get_by_genre(self, id_genre):
        return c.request_with_params('select * from livres where id_genre = ?', (id_genre,))

    def get_emprunts(self, id_livre):
        return c.request_with_params('select * from emprunts where id_livre = ?', (id_livre,))
