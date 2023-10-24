import connection as c
from backend.livres import Livres


class Auteurs:

    def __init__(self):
        pass

    def get_all(self):
        return c.request('select * from auteurs')

    def get(self, id):
        return c.request_with_params('select * from auteurs where id = ?', (id,))

    def create(self, nom):
        return c.request_with_params('insert into auteurs (nom) values (?)', (nom,))

    def update(self, id, nom):
        return c.request_with_params('update auteurs set nom = ? where id = ?', (nom, id))

    def delete(self, id):
        livres = Livres().get_by_auteur(id)
        if len(livres) > 0:
            print("L'auteur est associé à des livres")
            return False
        else:
            return c.request_with_params('delete from auteurs where id = ?', (id,))
