import db_postgre.db_connection_postgre


# Questa funzione ha l'obiettivo di stabilire una connessione con il db.
def connect_to_db():
    conn = db_postgre.db_connection_postgre.connect_to_db()
    return conn


# Apriamo il cursore che ci consentirà di interagire con il db.
def open_cursor(conn):
    cur = conn.cursor()
    return cur


# Questa funzione ci permette di chiudere il cursore quando abbiamo completato le nostre operazioni.
def close_cursor(cur):
    cur.close()


# Questa funzione ci permette di chiudere la connessione con il db.
def close_connection(conn):
    conn.close()


# Questa funzione si occupa di inserire un nuovo prodotto nel db.
def query_insert_db(cur, conn, prodotto):
    query = "INSERT INTO borsa (nome, prezzo, descrizione, materiale, colore, dimensione, img_url, product_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cur.execute(query, (prodotto.nome, prodotto.prezzo, prodotto.descrizione, prodotto.materiale, prodotto.colore, prodotto.dimensione, prodotto.url_immagine, prodotto.url_product))
    conn.commit()


# Questa funzione ci permette di ottenere la lista di tutti i materiali disponibili per le borse.
def query_search_material(cur):
    query = "SELECT DISTINCT LOWER(materiale) FROM borsa ORDER BY LOWER(materiale);"
    cur.execute(query)
    records = cur.fetchall()
    return records


# Questa funzione ci permette di ottenere la lista di tutti i colori disponibili per le borse.
def query_search_color(cur):
    query = "SELECT DISTINCT LOWER(colore) FROM borsa ORDER BY LOWER(colore);"
    cur.execute(query)
    records = cur.fetchall()
    return records


# Questa funzione ci permette di ottenere la lista di tutti gli url delle immagini, dei prodotti presenti in
# lista_url_produtct.
def query_search_url_immagini(cur, lista_url_product):
    lista_immagini = []
    for url in lista_url_product:
        query = "SELECT img_url FROM borsa WHERE product_url = %s"
        cur.execute(query, (url,))
        record = cur.fetchone()
        lista_immagini.append(record)
    return lista_immagini