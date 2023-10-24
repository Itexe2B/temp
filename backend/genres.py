import connection as c
from backend.livres import Livres

class Genres:

    def __init__(self):
        pass

    def get_all(self):
        return c.request('select * from genres')

    def get(self, id):
        return c.request('select * from genres where id = ?', (id,))

    def create(self, nom):
        return c.request_with_params('insert into genres (nom) values (?)', (nom,))

    def update(self, id, nom):
        return c.request_with_params('update genres set nom = ? where id = ?', (nom, id))

    def delete(self, id):
        livres = Livres().get_by_genre(id)
        if len(livres) > 0:
            print("Le genre est associé à des livres")
            return False
        else:
            return c.request_with_params('delete from genres where id = ?', (id,))
