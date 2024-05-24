from langchain.prompts import ChatPromptTemplate
import prompt_definition.prompt_default


# Questa funzione si occupa di inviare all'LLM il prompt finale contenente contesto e query dell'utente,
# così da ottenere i prodotti che più si avvicinano alla descrizione dell'utente.
def preparePrompt(results, query_text):
    # Per ogni tupla, viene estratto il contenuto del documento (doc.page_content) e viene aggiunto alla lista(
    # context_text). Alla fine, questa lista conterrà il contenuto di tutti i documenti trovati nei risultati della
    # ricerca. La funzione join() viene utilizzata per concatenare tutti gli elementi della lista ottenuta,
    # separandoli con la sequenza "\n\n---\n\n".
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    # Questa funzione crea un oggetto prompt_template che contiene la versione di template definita sopra.
    prompt_template = ChatPromptTemplate.from_template(prompt_definition.prompt_default.PROMPT_TEMPLATE)
    # Questa funzione serve a formattare il prompt che invieremo al modello, consentendo di specificare il contesto e
    # la domanda.
    prompt = prompt_template.format(context=context_text, question=query_text)
    return prompt


# Funzione che ci permette di preparare i prompt da inviare al modello, contenente la chat_history.
def preparePromptNew(chat_history, promptType):
    prompt_template = ChatPromptTemplate.from_template(promptType)
    prompt = prompt_template.format(chat_history=chat_history)
    return prompt


# Funzione che ci permette di preparare i prompt da inviare al modello, quando entriamo nella fase delle domande
# libere da parte dell'utente, quindi inseriremo nei prompt la chat_history e la query dell'utente.
def preparePromptGeneral(chat_history, user_query, promptType):
    prompt_template = ChatPromptTemplate.from_template(promptType)
    prompt = prompt_template.format(chat_history=chat_history, user_query=user_query)
    return prompt


# Funzione che ci permette di preparare i prompt da inviare al modello, quando vogliamo aggiungere oltre alla
# chat_history una lista generica di informazioni.
def prepareCustomPrompt(chat_history, promptType, lista):
    prompt_template = ChatPromptTemplate.from_template(promptType)
    prompt = prompt_template.format(chat_history=chat_history, details=lista)
    return prompt