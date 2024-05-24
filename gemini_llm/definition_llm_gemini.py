from dotenv import load_dotenv
from langchain_google_genai import *


# Questa funzione ci ritorna un riferimento all'oggetto embeddings che sarà utilizzato per convertire i file
# spezzettati in embedding(vettori)
def embeddings_functions():
    # Richiamiamo questa funzione così da assegnare alla variabile d'ambiente GOOGLE_API_KEY la key per accedere al
    # modello Gemini.
    load_dotenv()
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    return embeddings


# Questa funzione ci ritorna un riferimento al modello gemini 1.0, a cui potremmo inviare delle query e ricevere
# delle risposte. Assegnamo al modello temperature=0.1 così da limitare la creatività del modello e avere risposte
# più gestibili.
def model_functions():
    # Richiamiamo questa funzione così da assegnare alla variabile d'ambiente GOOGLE_API_KEY la key per accedere al
    # modello Gemini.
    load_dotenv()
    llm = ChatGoogleGenerativeAI(model="gemini-1.0-pro", temperature= "0.1")
    return llm


# Questa funzione ci ritorna un riferimento al modello gemini 1.5 pro, a cui potremmo inviare delle query e ricevere
# delle risposte. Di default la temperature del modello è settata al massimo, così da ricevere risposte più creative.
def model_functions_creative():
    # Richiamiamo questa funzione così da assegnare alla variabile d'ambiente GOOGLE_API_KEY la key per accedere al
    # modello Gemini.
    load_dotenv()
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest")
    return llm