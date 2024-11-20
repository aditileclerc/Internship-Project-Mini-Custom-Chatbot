from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
import os
import pandas as pd
from IPython.display import display
from dotenv import load_dotenv

load_dotenv()
api_key= os.getenv("OPEN_API_KEY")

embeddings = OpenAIEmbeddings(openai_api_key=api_key)
new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)


def show_vstore(store):
    vector_df = store_to_df(store)
    display(vector_df)

def store_to_df(store):
    v_dict= store.docstore._dict
    data_rows=[]
    for k in v_dict.keys():
        doc_name = v_dict[k].metadata['source'].split('/')[-1]
        page_number = v_dict[k].metadata.get('page', -1)+1
        content = v_dict[k].page_content
        data_rows.append({"chunk_id":k, "document":doc_name, "page": page_number, "content":content})
    vector_df = pd.DataFrame(data_rows)
    vector_df.to_csv("faiss.csv", sep='\t')
    return vector_df


print(show_vstore(new_db))
