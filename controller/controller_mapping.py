import json
import model.model_server
import view.prepare_response
import model.model_definition
import model.vector_db_functions


# Questa funzione viene mandata in esecuzione quando arriva una richiesta con il metodo GET
def mappa_request_get(parsed_path, self):
    if parsed_path.path == '/controller/recupero_tipologia_borse':
        # Recuperiamo le tipologie di borse disponibili.
        tipologia_borsa = model.model_server.recupera_tipologia_borsa()
        # Inviamo la risposta al client in formato json.
        view.prepare_response.prepare_response_json(tipologia_borsa, self)
    else:
        # Se il percorso richiesto non è gestito, restituisci un errore 404
        self.send_error(404, 'File Not Found: %s' % self.path)


# Questa funzione viene mandata in esecuzione quando arriva una richiesta con il metodo POST
def mappa_request_post(parsed_path, self):
    if parsed_path.path == '/controller/recupero_materiale_borsa':
        # Estrapoliamo dalla richiesta del client, la chat_history, con una funzione receive_data() dichiarata nel
        # file controller_mapping
        chat_history = recive_data(self)
        # Recuperiamo la lista dei materiali per le borse.
        materiale_borsa = model.model_server.recupera_materiale_borsa(chat_history)
        # Inviamo la risposta al client in formato json.
        view.prepare_response.prepare_response_json(materiale_borsa, self)
    elif parsed_path.path == '/controller/recupero_colore_borsa':
        # Estrapoliamo dalla richiesta del client, la chat_history, con una funzione receive_data() dichiarata nel
        # file controller_mapping
        chat_history = recive_data(self)
        # Recuperiamo la lista dei colori per le borse.
        colore_borsa = model.model_server.recupera_colore_borsa(chat_history)
        # Inviamo la risposta al client in formato json.
        view.prepare_response.prepare_response_json(colore_borsa, self)
    elif parsed_path.path == '/controller/recupero_prezzo_borsa':
        # Estrapoliamo dalla richiesta del client, la chat_history, con una funzione receive_data() dichiarata nel
        # file controller_mapping
        chat_history = recive_data(self)
        # Recuperiamo la lista delle fasce di prezzo per le borse.
        prezzo_borsa = model.model_server.recupera_prezzo_borsa(chat_history)
        # Inviamo la risposta al client in formato json.
        view.prepare_response.prepare_response_json(prezzo_borsa, self)
    elif parsed_path.path == '/controller/recupero_descrizione_borsa':
        # Estrapoliamo dalla richiesta del client, la chat_history, con una funzione receive_data() dichiarata nel
        # file controller_mapping
        chat_history = recive_data(self)
        # Recuperiamo la seguente domanda "vuoi inserire un ulteriore descrizione?"
        descrizione_borsa = model.model_server.recupera_descrizione_borsa(chat_history)
        # Inviamo la risposta al client in formato json.
        view.prepare_response.prepare_response_json(descrizione_borsa, self)
    elif parsed_path.path == '/controller/recupero_finale':
        # Estrapoliamo dalla richiesta del client, la chat_history, con una funzione receive_data() dichiarata nel
        # file controller_mapping
        chat_history = recive_data(self)
        # Recuperiamo i prodotti finali, più simili in base alle scelte dell'utente.
        recupero_finale = model.model_server.recupero_finale(chat_history)
        # Inviamo la risposta al client in formato json.
        view.prepare_response.prepare_response_json(recupero_finale, self)
    elif parsed_path.path == '/controller/domanda_generale':
        # Estrapoliamo dalla richiesta del client, il body del messaggio, con una funzione receive_data() dichiarata nel
        # file controller_mapping
        post_data_str = recive_data(self)
        # Estrapoliamo dal messaggio json la chat_history
        chat_history = extract_json('chat_history', post_data_str)
        # Estrapoliamo dal messaggio json la query dell'utente
        user_query = extract_json('user_query', post_data_str)
        # Recuperiamo la risposta del modello in base alla domanda generica fatta dall'utente.
        risposta_generale = model.model_server.domanda_generale(chat_history, user_query)
        # Inviamo la risposta al client in formato json.
        view.prepare_response.prepare_response_json(risposta_generale, self)
    elif parsed_path.path == '/controller/update_db':
        # Leggiamo la lunghezza del corpo del messaggio(numero di byte inviati)
        content_length = int(self.headers['Content-Length'])
        # Legge esattamente il numero di byte, precedentemente ricavato, dal body del messaggio.
        post_data = self.rfile.read(content_length)
        try:
            # Converti i dati JSON in un dizionario Python
            lista_prodotti = json.loads(post_data)
            # Per ogni prodottp della lista:
            for prodotto in lista_prodotti:
                # Estrapoliamo le varie informazioni dei prodotti.
                nome = prodotto['nome']
                prezzo = prodotto['prezzo']
                descrizione = prodotto['descrizione']
                materiale = prodotto['materiale']
                colore = prodotto['colore']
                dimensione = prodotto['dimensione']
                img_url = prodotto['url_immagine']
                product_url = prodotto['url_product']
                # Stampa a schermo il prodotto ricavato.
                print('Messaggio ricevuto dal client:', nome, prezzo, descrizione, materiale, colore, dimensione, img_url, product_url)
                # Aggiorniamo il db relazionale del server
                model.model_server.update_db(nome, prezzo, descrizione, materiale, colore, dimensione, img_url, product_url)
                # Aggiorniamo il file di testo, che utilizzeremo poi per ricreare il db vettoriale.
                model.model_server.update_file(nome, prezzo, descrizione, materiale, colore, dimensione, product_url)
            # Aggiorniamo il db vettoriale
            model.vector_db_functions.create_db()
            # Inviamo la risposta al client in formato text.
            view.prepare_response.prepare_response_text("Aggiornamento riuscito", self)
        # In caso di errore, invia un codice d'errore 400 al client.
        except Exception:
            self.send_response(400)
    elif parsed_path.path == '/controller/recupera_url_immagini':
        # Estrapoliamo dalla richiesta del client, il body, con una funzione receive_data() dichiarata nel
        # file controller_mapping
        post_data_str = recive_data(self)
        # Estrapoliamo dal messaggio la lista degli url dei prodotti
        lista_url_produtct = extract_json('lista', post_data_str)
        # Ricaviamo la lista degli url delle immagini, effettuando una query al db del server.
        lista_url_immagini = model.model_server.recupera_url_immagini(lista_url_produtct)
        # Inviamo la risposta al client in formato json.
        view.prepare_response.prepare_response_json(lista_url_immagini, self)
    else:
        # Se il percorso richiesto non è gestito, restituisci un errore 404 (Not Found)
        self.send_error(404, 'File Not Found: %s' % self.path)


# Questa funzione la utilizziamo per estrapolare il contenuto del messaggio ricevuto dal client
def recive_data(self):
    # Leggiamo la lunghezza del corpo del messaggio(numero di byte inviati)
    content_length = int(self.headers['Content-Length'])
    # Legge esattamente il numero di byte, precedentemente ricavato, dal body del messaggio.
    post_data = self.rfile.read(content_length)
    # Decodifica i dati da byte a stringa
    body_messaggio = post_data.decode('utf-8')
    return body_messaggio


# Questa funzione la utilizziamo per convertire il messaggio json ricevuto dal client in un dizionario python
def extract_json(key, post_data_str):
    # Converti i dati JSON in un dizionario Python
    try:
        data = json.loads(post_data_str)
        # Estrai il valore della chiave "key" se presente
        if key in data:
            value = data[key]
        else:
            print('Chiave non trovata nel JSON inviato dal client.')
    except json.JSONDecodeError as e:
        print('Errore durante il parsing del JSON:', e)
    return value