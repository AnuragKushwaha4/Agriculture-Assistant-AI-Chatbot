import os
from dotenv import load_dotenv
load_dotenv()
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
os.environ["LANGCHAIN_PROJECT"]=os.getenv("LANGCHAIN_PROJECT")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["HF_API_KEY"]=os.getenv("HF_API_KEY")

from flask import Flask,request,jsonify
import requests
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

from langchain_groq import ChatGroq


app = Flask(__name__)
llm = ChatGroq(model="llama-3.3-70b-versatile")


def CreateVector(document):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=100)
    splited_docs = splitter.split_documents(documents=document)
    embeddings =HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorStore = Chroma.from_documents(documents=splited_docs, embedding=embeddings, persist_directory="./chroma_db")
    vectorStore.persist()
    retriever = vectorStore.as_retriever()
    return retriever

def dataFetching(query,num_papers = 5):
    url = "https://api.openalex.org/works"
    params = {"filter": f"title.search:{query}", "per_page": num_papers}
    res = requests.get(url, params=params)
    data = res.json()
    papers = []

    for work in data.get("results", []):
        title = work.get("display_name", "")
        abstract_data = work.get("abstract_inverted_index", {})
        abstract_text = " ".join(abstract_data.keys()) if abstract_data else ""
        papers.append(f"Title: {title}\n Abstract: {abstract_text}")
    return papers


@app.route("/query_research", methods=["POST"])
def querySearch():
    data = request.get_json()
    user_query = data.get("query")

    if not user_query:
        return jsonify({"error": "Query missing"}), 400
    
    papers = dataFetching(user_query)
    if not papers:
        return jsonify({"response": "No relevant research found for this topic."})
    
    retriever = CreateVector(papers)

    prompts =ChatPromptTemplate.from_template(
        '''
            Hey You are Intelligent AI Assistant for Agriculture Students and Scientists Help them in their research by solving their doubts on the basic of the Provided context.

            {context}

            question:{input}
        '''
        )
    document_chain =create_stuff_documents_chain(llm=llm,prompt=prompts)
    retrieval_chain = create_retrieval_chain(retriever,document_chain)

    try:
        response = retrieval_chain.invoke({"input":user_query})
        return jsonify({"response": response})
    except:
        return jsonify({"response":"No Result Found"})
    

if __name__ == "__main__":
    app.run(debug=True)