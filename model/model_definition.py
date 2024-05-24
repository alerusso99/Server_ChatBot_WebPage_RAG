import gemini_llm.definition_llm_gemini


# Questa funzione ci ritorna un riferimento all'oggetto embeddings che sarà utilizzato per convertire i file
# spezzettati in embedding(vettori)
def embeddings_functions():
    embeddings = gemini_llm.definition_llm_gemini.embeddings_functions()
    return embeddings


# Questa funzione ci ritorna un riferimento al modello gemini 1.0, a cui potremmo inviare delle query e ricevere
# delle risposte. Assegnamo al modello temperature=0.1 così da limitare la creatività del modello e avere risposte
# più gestibili.
def model_functions():
    llm = gemini_llm.definition_llm_gemini.model_functions()
    return llm


# Questa funzione ci ritorna un riferimento al modello gemini 1.5 pro, a cui potremmo inviare delle query e ricevere
# delle risposte. Di default la temperature del modello è settata al massimo, così da ricevere risposte più creative.
def model_functions_creative():
    llm = gemini_llm.definition_llm_gemini.model_functions_creative()
    return llm