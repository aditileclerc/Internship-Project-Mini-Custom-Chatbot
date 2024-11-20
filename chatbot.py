
#you shouldve run dbcreation first so that faiss_index wouldve been created within the same directory
#dbcreation is also now in the same chaTBOT file - delete faiss and recreate


from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import FAISS
import os
import streamlit as st
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings 
from langchain_community.vectorstores import FAISS

#i removed the upload_html() function which i had commented out here
#for some reason streamlit was showing error - line 44 not readable

load_dotenv()
api_key= os.getenv("OPEN_API_KEY")

def query(question, chat_history):
    
    embeddings = OpenAIEmbeddings(openai_api_key = api_key)
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    # Initialize a ConversationalRetrievalChain
    query_chain = ConversationalRetrievalChain.from_llm(
        llm=llm, 
        retriever=new_db.as_retriever(), 
        return_source_documents=True)
    # Invoke the Chain with

    context_prompt = f"""
    Answer the following question based only on the Game of Thrones TV series, books and its spin-offs.
    If the user starts off by saying 'hi' or 'what's up' or anything related, reply in a friendly tone accordingly. 
    If the question is not related to the Game of Thrones TV series, books or its spin-offs, reply with 'I'm not sure'.
    If you don't have the relevant information in your database, reply with 'I have limited knowledge on that'.
    For any question asked, always give detailed answers not less than 150 words.
    If the user replies with other conversational phrases, reply accordingly.
    When the user replies with 'thanks' or any other variation of the same after you've answered, 
    reply with 'welcome' and stop giving answers related to the past question.
    Question: {question}
    """
    
    response = query_chain({"question": context_prompt, "chat_history": chat_history})
    answer = response["answer"]
    
    return {"answer": answer, "source_documents": response["source_documents"]}

def show_ui():

    #1. Implements the Streamlit UI
    st.title("your average GoT fan")    
    #cst.image("c4x-cbt.png")
    st.subheader("what's your question?")
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []   #attribute api
        st.session_state.chat_history = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("what do you want to know?: "):
       
        # Invoke the function with the Retriver with chat history and display responses in chat container in question-answer pairs 
        with st.spinner("Working on your query...."):     
            response = query(question=prompt, chat_history=st.session_state.chat_history)  #chatbot moment- as seen in documentation
                #llm function      
            with st.chat_message("user"):
                    st.markdown(prompt)
            with st.chat_message("assistant"):
                    st.markdown(response["answer"])    

        # Append user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.messages.append({"role": "assistant", "content": response["answer"]})
            st.session_state.chat_history.extend([(prompt, response["answer"])])

# Program Entry.....
if __name__ == "__main__":
    show_ui() 
    