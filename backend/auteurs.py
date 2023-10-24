import connection as c
from backend.livres import Livres


class Auteurs:

    def __init__(self):
        pass

    def get_all(self):
        #On recupere tous les auteurs
        return c.request('select * from auteurs')

    def get(self, id):
        #On recupere un auteur en fonction de son id
        return c.request_with_params('select * from auteurs where id = ?', (id,))

    def create(self, nom):
        #On ajoute un auteur
        return c.request_with_params('insert into auteurs (nom) values (?)', (nom,))

    def update(self, id, nom):
        #On modifie un auteur
        return c.request_with_params('update auteurs set nom = ? where id = ?', (nom, id))

    def delete(self, id):
        #Avant de supprimer un auteur, on regarde si il est associé à des livres
        livres = Livres().get_by_auteur(id)
        if len(livres) > 0:
            print("L'auteur est associé à des livres")
            return False
        else:
            #Si il n'est pas associé à des livres, on le supprime
            return c.request_with_params('delete from auteurs where id = ?', (id,))
