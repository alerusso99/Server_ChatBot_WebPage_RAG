from dotenv import load_dotenv
import psycopg2
import os


# Questa funzione ha l'obiettivo di stabilire una connessione con il db.
def connect_to_db():
    # Carichiamo le credenziali.
    load_dotenv()
    # Indichiamo il nome del db.
    dbname = "product_tramontano_server"
    # Indichiamo lo username dell'admin del db.
    user = os.getenv("USERNAME_PGADMIN")
    # Indichiamo la password dell'admin del db.
    password = os.getenv("PASSWORD_PGADMIN")
    # Indichiamo l'host del db.
    host = '172.17.0.2'
    # Indichiamo la porta su cui il db è in ascolto.
    port = '5432'
    try:
        # Effettuiamo la connessione al db.
        conn = psycopg2.connect(dbname=dbname, host=host, user=user, password=password, port=port)
        print("Connessione al database riuscita!")
    except psycopg2.Error as e:
        print("Errore durante la connessione al database:", e)
    return conn