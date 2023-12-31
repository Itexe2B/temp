import connection as c

class Emprunts:

    def __init__(self):
        pass

    def get_all(self):
        # On recupere tous les emprunts
        return c.request('select * from emprunts')

    def delete(self, id):
        # On supprime un emprunt
        return c.request_with_params('delete from emprunts where id = ?', (id,))

    def update(self, id, id_livre, id_emprunteur, date):
        # On modifie un emprunt
        return c.request_with_params('update emprunts set id_livre = ?, id_emprunteur = ?, date = ? where id = ?', (id_livre, id_emprunteur, date, id))