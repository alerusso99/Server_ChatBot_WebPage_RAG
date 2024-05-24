# Definiamo una classe Prodotto
class Prodotto:
    def __init__(self, nome, prezzo, descrizione, materiale, colore, dimensione, url_immagine, url_product):
        self.nome = nome
        self.prezzo = prezzo
        self.descrizione = descrizione
        self.materiale = materiale
        self.colore = colore
        self.dimensione = dimensione
        self.url_immagine = url_immagine
        self.url_product = url_product

    def __str__(self):
        return f"{self.nome} - {self.prezzo} €\nDescrizione: {self.descrizione}\nMateriale: {self.materiale}\nColore: {self.colore}\nDimensione: {self.dimensione}\nURL Immagine: {self.url_immagine}\nURL Prodotto: {self.url_product}"