import os
from dotenv import load_dotenv
load_dotenv()
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
os.environ["LANGCHAIN_PROJECT"]=os.getenv("LANGCHAIN_PROJECT")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["HF_API_KEY"]=os.getenv("HF_API_KEY")

from flask import Flask,request,jsonify
from flask_cors import CORS
import requests
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains.retrieval import create_retrieval_chain

# Simple Document class for LangChain 1.0.3
class Document:
    def __init__(self, page_content, metadata=None):
        self.page_content = page_content
        self.metadata = metadata or {}





from langchain_groq import ChatGroq


app = Flask(__name__)
CORS(app=app)
llm = ChatGroq(model="llama-3.3-70b-versatile")


def CreateVector(document):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=100)
    splited_docs = splitter.split_documents(documents=document)
    embeddings =HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorStore = Chroma.from_documents(documents=splited_docs, embedding=embeddings, persist_directory="./chroma_db")
    
    retriever = vectorStore.as_retriever()
    return retriever


def dataFetching(query, num_papers=5):
    url = "https://api.openalex.org/works"
    params = {"filter": f"title.search:{query}", "per_page": num_papers}
    res = requests.get(url, params=params)
    data = res.json()
    papers = []
   
    for work in data.get("results", []):
        title = work.get("display_name", "")
        abstract_data = work.get("abstract_inverted_index", {})
        abstract_text = " ".join(abstract_data.keys()) if abstract_data else ""
        papers.append(Document(f"Title: {title}\nAbstract: {abstract_text}"))
    return papers



@app.route("/query_research", methods=["POST"])
def querySearch():
    data = request.get_json()
    user_query = data.get("query")
    problem_statement = data.get("problem")

    if not user_query:
        return jsonify({"error": "Query missing"}), 400
    
    elif not problem_statement:
        return jsonify({"error": "Enter Problem statment"}), 400
    
    papers = dataFetching(user_query)
    if not papers:
        return jsonify({"response": "No relevant research found for this topic."})
    
    retriever = CreateVector(papers)

    prompts =ChatPromptTemplate.from_template(
        '''
            You are an intelligent AI assistant specialized in agriculture and agricultural research. Your task is to help students, researchers, and scientists by answering their questions based on the provided context. 

            Carefully analyze the context below and provide a clear, detailed, and accurate response. Make sure your answer:

                1. Directly addresses the user’s query.
                2. Explains concepts in a simple, understandable way when needed.
                3. Uses examples from the context if applicable.
                4. Remains professional and informative.
                5. If some context and input is not related to Agriculture just return Sorry I am not able to help you..
            Context:
            {context}

            Question:
            {input}

        '''
        )
    try:
        documentChain = create_stuff_documents_chain(prompt=prompts,llm=llm)
        retrieverChain = create_retrieval_chain(retriever,documentChain)

        response = retrieverChain.invoke({"input":problem_statement})
        answer = response.get("answer", "No answer found.")
        return jsonify({"response": answer})
    except Exception as e:
        print("Error:", e)
        return jsonify({"response":"Result not found"})


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)