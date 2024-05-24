import json


# Questa funzione ci permette di preparare una risposta nel formato json da inviare al client.
def prepare_response_json(risposta, self):
    try:
        # Impostiamo il codice di stato della risposta a 200 (OK)
        self.send_response(200)
        # Impostiamo l'header Content-type per indicare che stiamo restituendo un JSON
        self.send_header(
            'Content-type', 'application/json'
        )
        # Facciamo terminare l'header con una riga vuota
        self.end_headers()
        # Prepara il dizionario di risposta
        response_data = {
            'Risposta': '{}'.format(risposta)
        }
        # Serializziamo il dizionario in una stringa JSON
        response_json = json.dumps(response_data)
        print("\nRISPOSTA JSON SERVER\n", response_json)
        print("\n--------------------\n")
        # Scriviamo il contenuto della risposta nel messaggio.
        self.wfile.write(response_json.encode('utf-8'))
    except TypeError as e:
        error_message = "Errore di serializzazione JSON: {}".format(e)
        print(error_message)
        send_error_response_json(self, error_message)
    except OSError as e:
        error_message = "Errore di I/O durante la scrittura della risposta: {}".format(e)
        print(error_message)
        send_error_response_json(self, error_message)


# Questa funzione viene invocata se si entra in un eccezzione generata dalla funzione prepare_response_json.
def send_error_response_json(self, error_message):
    # Imposta il codice di stato della risposta a 500 (Internal Server Error)
    self.send_response(500)
    # Imposta l'header Content-type per indicare che stiamo restituendo un JSON
    self.send_header(
        'Content-type', 'application/json'
    )
    # Facciamo terminare l'header con una riga vuota
    self.end_headers()
    # Prepara il dizionario di Risposta
    error_data = {
        'Risposta': error_message
    }
    # Serializziamo il dizionario in una stringa JSON
    error_json = json.dumps(error_data)
    # Scriviamo il contenuto della risposta d'errore nel messaggio.
    self.wfile.write(error_json.encode('utf-8'))


# Questa funzione ci permette di preparare una risposta nel formato text da inviare al client.
def prepare_response_text(risposta, self):
    try:
        # Impostiamo il codice di stato della risposta a 200 (OK)
        self.send_response(200)
        # Impostiamo l'header Content-type per indicare che stiamo restituendo un text
        self.send_header(
            'Content-type', 'text/plain'
        )
        content_length = len(risposta)
        # Impostiamo l'header Content-Length
        self.send_header('Content-Length', str(content_length))
        # Facciamo terminare l'header con una riga vuota
        self.end_headers()
        # Scriviamo il contenuto della risposta nel messaggio.
        self.wfile.write(risposta.encode('utf-8'))
    except OSError as e:
        error_message = "Errore di I/O durante la scrittura della risposta: {}".format(e)
        print(error_message)
        send_error_response_text(self, error_message)


# Questa funzione viene invocata se si entra in un eccezzione generata dalla funzione prepare_response_text.
def send_error_response_text(self, error_message):
    # Imposta il codice di stato della risposta a 500 (Internal Server Error)
    self.send_response(500)
    # Imposta l'header Content-type per indicare che stiamo restituendo un text
    self.send_header(
        'Content-type', 'text/plain'
    )
    # Calcola la lunghezza del messaggio di errore
    content_length = len(error_message)
    # Imposta l'header Content-Length
    self.send_header('Content-Length', str(content_length))
    # Facciamo terminare l'header con una riga vuota
    self.end_headers()
    # Scriviamo il contenuto della risposta d'errore nel messaggio.
    self.wfile.write(error_message.encode('utf-8'))