from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.vectorstores.chroma import Chroma
import os
import shutil
import model.model_definition


CHROMA_PATH = "chroma"
DATA_PATH = "txt_file"


# Questa è la funzione che genera effettivamente il database vettoriale, inizialmente carica i documenti,
# poi splitta i documenti in parti più piccole chiamati chunks, per poi richiamare la funzione save_to_chroma che si
# occupa di convertire i chunks in vettoriale per poi salvarli sul db chroma.
def generate_data_store(embeddings):
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks, embeddings)


# Effettuiamo il caricamento di tutti i documenti .txt presenti nella cartella di destinazione del percorso
# DATA_PATH
def load_documents():
    loader = DirectoryLoader(DATA_PATH, glob="*.txt", show_progress=True)
    # L'oggetto documents sarà una lista.
    documents = loader.load()
    return documents


# Questa funzione si occupa dello split del documento.
def split_text(documents: list[Document]):  # Prende in input una serie di documenti
    text_splitter = RecursiveCharacterTextSplitter(  # Questa funzione si occupa dello split effettivo del documento
        chunk_size=600,  # Ogni chunk avrà lunghezza massima di 600 caratteri
        chunk_overlap=1,  # Raramente ci sarà al massimo un carattere di overlap
        length_function=len,  # La funzione che utilizziamo per il conteggio dei caratteri è la funzione length.
        is_separator_regex=False,  # Trattare il documento come una stringa letterale
    )
    # Andiamo ad eseguire lo split del documento. L'oggetto chunks sarà una lista contenente tutti i vari split.
    chunks = text_splitter.split_documents(documents)
    print(f"Abbiamo Splittato {len(documents)} documenti in {len(chunks)} chunks.")
    return chunks


# Funzione che si occupa dell'effettivo salvataggio dei chunks nel DB vettoriale
def save_to_chroma(chunks: list[Document], embeddings):
    # Se esiste già un db Chroma nel path CHROMA_PATH, eliminalo.
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # Creiamo un nuovo db Chroma vettoriale. Diamo in input i chunks creati prima. Lo scopo principale dell'oggetto
    # embeddings è generare rappresentazioni numeriche (embedding) così da poterle salvare nel DB vettoriale. Questi
    # embedding catturano il significato semantico e le relazioni tra parole e frasi, abilitando diverse attività a
    # valle come applicazioni di elaborazione del linguaggio naturale (NLP). persist_directory specifica il percorso
    # della directory in cui l'archivio dati verrà salvato su disco.
    db = Chroma.from_documents(chunks, embeddings, persist_directory=CHROMA_PATH)
    db.persist()  # Effettuiamo l'effettivo salvataggio del DB.
    print(f"Hai Salvato {len(chunks)} chunks nel path {CHROMA_PATH}.")


def create_db():
    # Creiamo un oggetto embeddingsVariable richiamando la funzione embeddings_functions() presente nel file
    # model_definition.py
    embeddingsVariable = model.model_definition.embeddings_functions()
    # Generiamo il DB vettoriale
    generate_data_store(embeddingsVariable)


if __name__ == "__main__":
    create_db()