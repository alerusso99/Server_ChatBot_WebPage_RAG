from model import model_definition
from model import llm_functions
from model import vector_db_functions
import prompt_definition.prompt_default
import prompt_definition.prompt_function
from model import relational_db_functions
from model import product_information


# Definiamo il percorso del db vettoriale.
CHROMA_PATH = "../chroma"


# Creiamo un oggetto embeddingsVariable richiamando la funzione embeddings_functions() presente nel file
# model_definition.py
embeddingsVariable = model_definition.embeddings_functions()
# Creiamo un oggetto llmVariable richiamando la funzione model_functions() presente nel file model_definition
llmVariable = model_definition.model_functions()
# Creiamo un istanza del db creato precedentemente nel file create_vector_db.py
db = vector_db_functions.prepareDB(embeddingsVariable)
# Creiamo un oggetto llmVariableCreative richiamando la funzione model_functions_creative() presente nel file
# model_definition. Differenza principale rispetto ad llmVariable, è che viene istanziato un modello con temperature(
# creatività) più alto rispetto al modello istanziato per llmVariable.
llmVariableCreative = model_definition.model_functions_creative()


# Funzione che invia una query all'LLM. Chiediamo di presentarsi e di chiederci quale tipologia di borsa desideriamo.
def recupera_tipologia_borsa():
    tipologia_borsa = llm_functions.sendQuery(prompt_definition.prompt_default.presentation_message, llmVariable)
    return tipologia_borsa


# Funzione che invia una query all'LLM. Chiediamo di domandarci quale materiale desideriamo per la nostra borsa.
def recupera_materiale_borsa(chat_history):
    # Ci colleghiamo al db relazionale.
    connection = relational_db_functions.connect_to_db()
    # Apriamo un cursore, per effettuare delle query al db.
    cursor = relational_db_functions.open_cursor(connection)
    # Effettuiamo una query al db, e ricaviamo la lista dei materiali aggiornati.
    lista_materiali = relational_db_functions.query_search_material(cursor)
    # Chiudiamo il cursore del db.
    relational_db_functions.close_cursor(cursor)
    # Chiudiamo la connessione al db.
    relational_db_functions.close_connection(connection)
    # Creiamo una stringa contenente tutti i materiali precedentemente ottenuti dal db.
    materiali_stringa = "\n".join([materiale[0] for materiale in lista_materiali])
    # Creiamo un prompt personalizzato, così da aggiungere alla query la chat_history e i materiali disponibili.
    prompt = prompt_definition.prompt_function.prepareCustomPrompt(chat_history,prompt_definition.prompt_default.material_message, materiali_stringa)
    # Inviamo una query al modello, per ottenere una domanda da porre all'utente, che dovrà scegliere uno dei
    # materiali disponibili.
    materiale_borsa = llm_functions.sendQuery(prompt, llmVariable)
    return materiale_borsa


# Funzione che invia una query all'LLM. Chiediamo di domandarci quale colore desideriamo per la nostra borsa.
def recupera_colore_borsa(chat_history):
    # Ci colleghiamo al db relazionale.
    connection = relational_db_functions.connect_to_db()
    # Apriamo un cursore, per effettuare delle query al db.
    cursor = relational_db_functions.open_cursor(connection)
    # Effettuiamo una query al db, e ricaviamo la lista dei colori aggiornata.
    lista_colori = relational_db_functions.query_search_color(cursor)
    # Chiudiamo il cursore del db.
    relational_db_functions.close_cursor(cursor)
    # Chiudiamo la connessione al db.
    relational_db_functions.close_connection(connection)
    # Creiamo una stringa contenente tutti i colori precedentemente ottenuti dal db.
    colori_stringa = "\n".join([colore[0] for colore in lista_colori])
    # Creiamo un prompt personalizzato, così da aggiungere alla query la chat_history e i colori disponibili.
    prompt = prompt_definition.prompt_function.prepareCustomPrompt(chat_history, prompt_definition.prompt_default.color_message, colori_stringa)
    # Inviamo una query al modello, per ottenere una domanda da porre all'utente, che dovrà scegliere uno dei
    # colori disponibili.
    colore_borsa = llm_functions.sendQuery(prompt, llmVariable)
    return colore_borsa


# Funzione che invia una query all'LLM. Chiediamo di domandarci quale prezzo desideriamo per la nostra borsa.
def recupera_prezzo_borsa(chat_history):
    # Creiamo un prompt personalizzato, così da aggiungere alla query la chat_history(cronologia della chat).
    prompt = prompt_definition.prompt_function.preparePromptNew(chat_history, prompt_definition.prompt_default.price_message_now)
    # Inviamo una query al modello, per ottenere una domanda da porre all'utente, che dovrà scegliere una fascia di
    # prezzo.
    prezzo_borsa = llm_functions.sendQuery(prompt, llmVariable)
    return prezzo_borsa


# Funzione che invia una query all'LLM. Chiediamo di domandarci se abbiamo intenzione di inserire una descrizione.
def recupera_descrizione_borsa(chat_history):
    # Creiamo un prompt personalizzato, così da aggiungere alla query la chat_history(cronologia della chat).
    prompt = prompt_definition.prompt_function.preparePromptNew(chat_history, prompt_definition.prompt_default.description_message_now)
    # Inviamo una query al modello, per ottenere una domanda da porre all'utente, che dovrà decidere se inserire una
    # descrizione.
    descrizione_borsa = llm_functions.sendQuery(prompt, llmVariable)
    return descrizione_borsa


# Funzione che chiede inizialmente al modello di formattare le nostre risposte in modo schematico,
# così da interrogare con maggior successo il db vettoriale.
def recupero_finale(chat_history):
    # Prepariamo il prompt da inviare al modello, inserendo la chat_history.
    prompt_final = prompt_definition.prompt_function.preparePromptNew(chat_history, prompt_definition.prompt_default.final_message_now)
    # Inviamo al LLM la query finale, chiedendo se può farci un resoconto delle risposte ottenute.
    borsa_finale = llm_functions.sendQuery(prompt_final, llmVariable)
    # Effettuiamo la ricerca nel DB vettoriale con la funzione searchDB()
    borse_simili = vector_db_functions.searchDB(borsa_finale, db)
    # Se non è stato trovato alcun risultato oppure se c'è una distanza minore di 0.3 stampa un messaggio d'errore.
    if len(borse_simili) == 0 or borse_simili[0][1] < 0.3:
        risposta = "Non è stato trovato nessun risultato."
    else:
        # Prepara il prompt, unendo i risultati ottenuti dal DB e le scelte dell'utente, da mandare al modello.
        prompt = prompt_definition.prompt_function.preparePrompt(borse_simili, borsa_finale)
        # Invio la query al modello
        risposta = llm_functions.sendQuery(prompt, llmVariable)
    return risposta


# Funzione che ci permette di effettuare domande generiche al modello(ovviamente sempre riguardanti le borse).
def domanda_generale(chat_history, user_query):
    # Creiamo un prompt personalizzato, così da aggiungere alla query la chat_history(cronologia della chat) e la
    # query dell'utente.
    prompt = prompt_definition.prompt_function.preparePromptGeneral(chat_history, user_query, prompt_definition.prompt_default.general_message)
    # Inviamo la query al modello, ottenendo poi la risposta.
    risposta_generale = llm_functions.sendQuery(prompt, llmVariableCreative)
    return risposta_generale


# Funzione che ci permette di aggiornare il db relazionale.
def update_db(nome, prezzo, descrizione, materiale, colore, dimensione, img_url, product_url):
    # Creiamo un oggetto prodotto.
    prodotto = product_information.Prodotto(nome, prezzo, descrizione, materiale, colore, dimensione, img_url, product_url)
    # Ci colleghiamo al db.
    connection = relational_db_functions.connect_to_db()
    # Apriamo un cursore del db.
    cursor = relational_db_functions.open_cursor(connection)
    # Effettuiamo l'inserimento nel db, del nuovo prodotto.
    relational_db_functions.query_insert_db(cursor, connection, prodotto)
    # Chiudiamo il cursore.
    relational_db_functions.close_cursor(cursor)
    # Chiudiamo la connessione.
    relational_db_functions.close_connection(connection)


# Questa funzione aggiorna il file di testo, che utilizzeremo poi per aggiornare il db vettoriale.
def update_file(nome, prezzo, descrizione, materiale, colore, dimensione, product_url):
    # Apri il file in modalità append
    with open("txt_file/Borse.txt", "a") as file:
        # Scrivi i dati nel file
        file.write(f"Nome:\"{nome}\",\n")
        file.write(f"Descrizione:\"{descrizione}\",\n")
        file.write(f"Materiale:\"{materiale}\",\n")
        file.write(f"Colore:\"{colore}\",\n")
        file.write(f"Dimensione:\"{dimensione}\",\n")
        file.write(f"Prezzo:\"{prezzo}\",\n")
        file.write(f"URL:\"{product_url}\"")
        file.write("\n\n")
        file.flush()


# Questa funzione si occupa di ricavare la lista degli URL delle immagini dei prodotti presenti nella lista
# lista_url_product.
def recupera_url_immagini(lista_url_product):
    # Ci colleghiamo al db.
    connection = relational_db_functions.connect_to_db()
    # Apriamo un cursore del db.
    cursor = relational_db_functions.open_cursor(connection)
    # Iniziamo la ricerca nel db, per individuare gli URL delle immagini.
    lista_url_immagini = relational_db_functions.query_search_url_immagini(cursor, lista_url_product)
    # Chiudiamo il cursore del db.
    relational_db_functions.close_cursor(cursor)
    # Chiudiamo la connessione del db.
    relational_db_functions.close_connection(connection)
    return lista_url_immagini