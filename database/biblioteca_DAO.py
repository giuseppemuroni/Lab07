from database.DB_connect import DBConnect
from model.biblioteca_DTO import Biblioteca

"""
    Biblioteca DAO
    Gestisce le operazioni di accesso al database relative alle biblioteche (Effettua le Query).
"""

class BibliotecaDAO:
    def __init__(self):
        pass

    def get_all(self):
        """Recupera tutte le biblioteche dal database."""
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            query = "SELECT * FROM biblioteca"
            cursor.execute(query)

            risultato = []
            for row in cursor.fetchall():
                # Creiamo l'oggetto DTO usando le chiavi del dizionario restituito
                biblio = Biblioteca(row['id'], row['nome'], row['indirizzo'])
                risultato.append(biblio)

            cursor.close()
            conn.close()
            return risultato

        except Exception as e:
            print(f"Errore DAO (BibliotecaDAO - get_all): {e}")
            return None
