# Server ChatBot WebPage RAG

## Descrizione dell'applicativo

Questo progetto consiste in un server scritto in Python che funge da intermediario tra un client utilizzante un chatbot e LLM. Lo scopo principale del server è fornire al client una lista di borse che corrispondono alle preferenze dell'utente raccolte tramite il chatbot. La selezione delle borse che più si avvicinano alle preferenze dell'utente avviene tramite tecniche RAG, utilizzando il DB vettoriale ChromaDB.

## Funzionalità

Il server implementa le seguenti funzionalità:

- Comunicazione con un LLM (Language Model), un database vettoriale e un database PostgreSQL.
- Risposta ad un client che utilizza un chatbot per raccogliere preferenze sulle borse.
- Utilizzo di un'API di Gemini per rispondere in modo conversazionale.
- Interrogazione del database vettoriale per trovare borse che corrispondono alle preferenze dell'utente.
- Implementazione di un'architettura Model-View-Controller per gestire le richieste del client e preparare le risposte.

## Architettura dell'applicazione

Il server è basato su un'architettura Model-View-Controller (MVC):

- **Model**: Contiene la logica di business e le operazioni di accesso ai dati. Qui vengono eseguite le operazioni sul database vettoriale, su PostgreSQL e la comunicazione con il modello Gemini.
- **View**: Prepara le risposte da inviare al client. Gestisce la formattazione e la presentazione dei dati.
- **Controller**: Riceve le richieste dal client, filtra e valida i dati, e inoltra le richieste ai metodi appropriati nel Model. Coordina il flusso di dati tra Model e View.

## Prerequisiti

Prima di avviare il server, assicurati di avere installato:

- Python 3.10
- Dipendenze Python elencate nel file `requirements.txt`
- Accesso ai database ChromaDB e PostgreSQL
- Connessione stabile a Internet per l'accesso all'API di Gemini.