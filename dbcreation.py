
import os
import logging
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from tqdm import tqdm

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def upload_htmls():
    load_dotenv()
    api_key = os.getenv("OPEN_API_KEY")

    logging.info("Starting to load HTML pages.")
    
    # Load all the HTML pages in the given folder structure recursively using Directory Loader
    loader = DirectoryLoader(path=r"E:\aditi works\purpleslate\udemy\chatbot\GoT")
    documents = loader.load()
    logging.info(f"{len(documents)} Pages Loaded")

    # Split loaded documents into chunks using CharacterTextSplitter
    logging.info("Starting to split documents into chunks.")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=50, separators=["\n\n", "\n", " ", ""]
    )

    split_documents = []
    for doc in tqdm(documents, desc="Splitting Documents"):
        split_documents.extend(text_splitter.split_documents(documents=[doc]))

    logging.info(f"Split into {len(split_documents)} Documents")

    # Upload chunks as vector embeddings into FAISS
    logging.info("Starting to upload chunks as vector embeddings into FAISS.")
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    db = FAISS.from_documents(split_documents, embeddings)
    
    # Save the FAISS DB locally
    logging.info("Saving the FAISS DB locally.")
    db.save_local("faiss_index")
    logging.info("FAISS DB saved successfully.")

def faiss_query():
    load_dotenv()
    api_key = os.getenv("OPEN_API_KEY")

    logging.info("Loading FAISS DB.")
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

    query = "can you give me a summary of House of the Dragons S1 E1?"
    logging.info(f"Querying the FAISS DB with: {query}")
    docs = new_db.similarity_search(query)

    # Print all the extracted Vectors from the above Query
    for doc in docs:
        logging.info("##---- Page ---##")
        logging.info(doc.metadata['source'])
        logging.info("##---- Content ---##")
        logging.info(doc.page_content)

if __name__ == "__main__":
    # The below code 'upload_htmls()' is executed only once and then commented as the Vector Database is now built and ready for your further 
    # experiments
    upload_htmls()   
    # The below function is experimental to trigger a semantic search on the Vector DB
    faiss_query()
