import sqlite3

#Nom de fichier de connection à la base de données
DATABASE_NAME = 'database'
def connect():
    #Utilisation de la librairie sqlite3 pour se connecter à la base de données
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    #La connexion et le curseur sont retournés pour pouvoir les utiliser dans les autres classes
    #Ils servent notamment à faire les requêtes
    cursor.execute('PRAGMA foreign_keys = ON;') #On active les foreign keys
    conn.commit()
    return conn, cursor

def close(conn):
    #Fermeture de la connexion pour éviter les problèmes de sécurité
    conn.close()

def request(request):
    #On se connecte à la base de données
    conn, cursor = connect()
    #On exécute la requête
    cursor.execute(request)
    #On commit les changements. C'est à dire qu'on les enregistre dans la base de données
    conn.commit()
    #On récupère le résultat de la requête
    return_val = cursor.fetchall()
    #On ferme la connexion
    conn.close()
    #On retourne le résultat de la requête
    return return_val

def request_with_params(request, params):
    conn, cursor = connect()
    cursor.execute(request, params)
    conn.commit()
    return_val = cursor.fetchall()
    conn.close()
    return return_val
