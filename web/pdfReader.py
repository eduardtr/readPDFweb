from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate


import getpass
import os
#os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

rag_chain = {}
loaded_document = ""

def load_document(document):
    # Cargar fichero PDF
    if document == loaded_document:
        print("Document already loaded.")
        return
    loader = PyPDFLoader(document)
    docs = loader.load()

    #Cargamos el modelo CHATGPT
    llm = ChatOpenAI(model="gpt-3.5-turbo")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    vectorstore = InMemoryVectorStore.from_documents(
        documents=splits, embedding=OpenAIEmbeddings()
    )

    retriever = vectorstore.as_retriever()

    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the "
        "answer concise. Do not make up answers or use your own knowledge, focus on the text entered."
        "\n\n"
        "{context}"
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    global rag_chain
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

def ask_question(question):
    if rag_chain:
        return rag_chain.invoke({"input": question})
    else:
        print("Rag chain is null.")
        load_document("https://www.boe.es/doue/2016/119/L00001-00088.pdf")
        return rag_chain.invoke({"input": question})