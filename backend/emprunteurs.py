import connection as c


class Emprunteurs:

    def __init__(self):
        pass

    def get_all(self):
        return c.request('select * from emprunteurs')

    def get(self, id):
        return c.request_with_params('select * from emprunteurs where id = ?', (id,))

    def create(self, nom):
        return c.request_with_params('insert into emprunteurs (nom) values (?)', (nom,))

    def update(self, id, nom):
        return c.request_with_params('update emprunteurs set nom = ? where id = ?', (nom, id))

    def delete(self, id):
        emprunts = self.get_emprunts(id)
        if len(emprunts) > 0:
            print("L'emprunteur a des emprunts en cours")
            return False
        else:
            return c.request_with_params('delete from emprunteurs where id = ?', (id,))

    def get_emprunts(self, id_emprunteur):
        return c.request_with_params('select * from emprunts where id_emprunteur = ?', (id_emprunteur,))

    def emprunter_livre(self, id_emprunteur, id_livre, date=None):
        if date is None:
            date = 'CURRENT_DATE'
            result = c.request_with_params('insert into emprunts (id_emprunteur, id_livre) values (?, ?)', (id_emprunteur, id_livre))
        else:
            result = c.request_with_params('insert into emprunts (id_emprunteur, id_livre, date) values (?, ?, ?)', (id_emprunteur, id_livre, date))

    def rendre_livre(self, id_emprunteur, id_livre):
        return c.request_with_params('delete from emprunts where id_emprunteur = ? and id_livre = ?', (id_emprunteur, id_livre))