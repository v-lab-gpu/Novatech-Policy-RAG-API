import os
import uuid
import logging
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import chromadb


load_dotenv()
Groq_api_key=os.getenv("GROQ_API_KEY")


logging.basicConfig(level=logging.INFO,format="%(asctime)s | %(message)s")
logger=logging.getLogger(__name__)



class ChatRequest(BaseModel):
    question:str

class ChatResponse(BaseModel):
    answer:str
    sources: list[str]
    request_id: str

client=OpenAI(api_key=Groq_api_key, base_url="https://api.groq.com/openai/v1")
chroma_client=chromadb.Client()



def load_and_index_docs():
    data_folder = "F:\Resume\AIML\Test\data"

    try:
        chroma_client.delete_collection('docs')
    except:
        pass

    collection=chroma_client.create_collection(name="docs")

    all_chunks=[]
    all_ids=[]
    all_metadatas=[]
    chunk_id=0

    for filename in os.listdir(data_folder):
        if not filename.endswith(".txt"):
            continue

        filepath=os.path.join(data_folder,filename)
        with open(filepath,"r") as f:
            text=f.read()
        #Chunk by paragraph 
        paragraphs=text.strip().split("\n\n")
        for para in paragraphs:
            para = para.strip()
            if len(para)<50:
                continue
            if para.startswith("===="):
                continue

            all_chunks.append(para)
            all_ids.append(f"chunk_{chunk_id}")
            all_metadatas.append({"source": filename})
            chunk_id +=1
    
    collection.add(documents=all_chunks, ids=all_ids, metadatas=all_metadatas)
    logger.info(f"Indexed{chunk_id} chunks from {data_folder}")
    return collection

collection =  load_and_index_docs()  


def ask_rag(question):
    results=collection.query(query_texts=[question], n_results=3)
    chunks = results['documents'][0]
    sources=[m["source"] for m in results["metadatas"][0]]


    #Build Prompt
    context ="\n\n".join(chunks)
    messages=[
        {
            "role": "system",
            "content": (
                "You are a helpful company assistant. Answer questions using ONLY "
                "the provided context. If the context doesn't contain the answer, "
                "say 'I don't have enough information to answer this.' Be concise."
            )
        },
        {
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {question}"
        }
    ]

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages,
        temperature=0.2
    )
    return response.choices[0].message.content, list(set(sources))



app = FastAPI(title="NovaTech RAG Chatbot", version="1.0")

@app.get("/")
def home():
    return{"status": "running","message":"NovaTech RAG Chatbot is live!"}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    request_id=str(uuid.uuid4())[:8]

    logger.info(f"[{request_id}] Question: {request.question}")

    answer,sources=ask_rag(request.question)

    logger.info(f"[{request_id}] Sources: {sources}")

    return ChatResponse(answer=answer,sources=sources,request_id=request_id)






