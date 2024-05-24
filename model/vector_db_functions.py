from langchain.vectorstores.chroma import Chroma
import subprocess


CHROMA_PATH = "chroma"


# Questa funzione ci permette di definire un'istanza del db vettoriale.
def prepareDB(embeddings):
    # Creiamo un nuovo oggetto db. Passiamo come parametri, il path della directory in cui è stato salvato
    # precedentemente il db, e l'oggetto embeddings, così da trasformare la query in un embedding,
    # per poi interrogare il db.
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    return db


# Questa funzione ci permette di effettuare una ricerca di similarità del db vettoriale, dando in input la query
# dell'utente.
def searchDB(query_text, db):
    # Cerchiamo nel db similitudini con la query_text. Esegue una ricerca basata su embedding e restituisce un
    # elenco di risultati. Ogni risultato nell'elenco è una tupla contenente due elementi: doc è un riferimento
    # all'oggetto documento che corrisponde alla query, score è il punteggio di rilevanza (compreso tra 0 e 1) che
    # indica quanto il documento è simile alla query. Con il parametro k impostato su 5, vuol dire che ci restituirà
    # i 5 prodotti che più si avvicinano alla descrizione dell'utente.
    results = db.similarity_search_with_relevance_scores(query_text, k=5)
    return results


# Questa funzione ci permette di ricreare il db vettoriale, dopo che i dati sono stati aggiornati.
def create_db():
    subprocess.run(["python", "create_vector_db.py"])