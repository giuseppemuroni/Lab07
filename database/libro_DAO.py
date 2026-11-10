from database.DB_connect import DBConnect
from model.libro_DTO import Libro

"""
    LIBRO DAO
    Gestisce le operazioni di accesso al database relative ai libri (Effettua le Query).
"""

class LibroDAO:
    def __init__(self):
        pass

    def get_generi(self):
        """Recupera la lista di tutti i generi distinti presenti nel database."""
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # DISTINCT evita di avere "Fantascienza" ripetuto decine di volte
            query = "SELECT DISTINCT genere FROM libro WHERE genere IS NOT NULL ORDER BY genere"
            cursor.execute(query)

            generi = []
            for row in cursor.fetchall():
                generi.append(row[0])

            cursor.close()
            conn.close()
            return generi

        except Exception as e:
            print(f"Errore DAO (LibroDAO - get_generi): {e}")
            return None

    def get_libri_filtrati(self, nome_biblioteca, genere):
        """
        Recupera i libri filtrati. Se nome_biblioteca o genere sono None,
        il filtro corrispondente viene ignorato grazie a COALESCE.
        """
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT l.* 
                FROM libro l
                JOIN biblioteca b ON l.id_biblioteca = b.id
                WHERE l.genere = COALESCE(%s, l.genere)
                  AND b.nome = COALESCE(%s, b.nome)
            """

            # Esegue la query passando i parametri (None viene tradotto in NULL in MySQL)
            cursor.execute(query, (genere, nome_biblioteca))

            risultato = []
            for row in cursor.fetchall():
                libro = Libro(
                    id=row['id'],
                    titolo=row['titolo'],
                    autore=row['autore'],
                    genere=row['genere'],
                    anno_pubblicazione=row['anno_pubblicazione'],
                    id_biblioteca=row['id_biblioteca']
                )
                risultato.append(libro)

            cursor.close()
            conn.close()
            return risultato

        except Exception as e:
            print(f"Errore DAO (LibroDAO - get_libri_filtrati): {e}")
            return None
