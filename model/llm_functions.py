# Questa funzione si occupa di inviare effettivamente la richiesta al modello.
def sendQuery(prompt, llm):
    response_text = llm.invoke(prompt)
    return response_text.content
