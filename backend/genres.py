import connection as c
from backend.livres import Livres


class Genres:

    def __init__(self):
        pass

    def get_all(self):
        # On recupere tous les genres
        return c.request('select * from genres')

    def get(self, id):
        # On recupere un genre en fonction de son id
        return c.request('select * from genres where id = ?', (id,))

    def create(self, nom):
        # On ajoute un genre
        return c.request_with_params('insert into genres (nom) values (?)', (nom,))

    def update(self, id, nom):
        # On modifie un genre
        return c.request_with_params('update genres set nom = ? where id = ?', (nom, id))

    def delete(self, id):
        # Avant de supprimer un genre, on regarde si il est associé à des livres
        livres = Livres().get_by_genre(id)
        if len(livres) > 0:
            print("Le genre est associé à des livres")
            return False
        else:
            # Si il n'est pas associé à des livres, on le supprime
            return c.request_with_params('delete from genres where id = ?', (id,))
