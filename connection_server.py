from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
from controller import controller_mapping


# Definiamo la classe del gestore delle richieste che estende BaseHTTPRequestHandler
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    # Override del metodo do_GET per gestire le richieste GET
    def do_GET(self):
        # Parsing del percorso della richiesta
        parsed_path = urllib.parse.urlparse(self.path)
        controller_mapping.mappa_request_get(parsed_path, self)

    # Override del metodo do_POST per gestire le richieste POST
    def do_POST(self):
        # Parsing del percorso della richiesta
        parsed_path = urllib.parse.urlparse(self.path)
        controller_mapping.mappa_request_post(parsed_path, self)

# Definiamo la funzione principale per avviare il server.
def run():
    # Specifica l'indirizzo IP(local) e la porta su cui ascoltare
    server_address = ('', 8000)
    # Crea un'istanza del server HTTP
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    # Avvia il server
    print('Server in esecuzione...')
    try:
        httpd.serve_forever()
    # CTRL+c per interrompere il server.
    except KeyboardInterrupt:
        print("Server interrotto...")
        httpd.server_close()


# Avviamo il server chiamando la funzione run
if __name__ == '__main__':
    run()
