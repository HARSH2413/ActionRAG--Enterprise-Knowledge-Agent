import os
import time
from langchain_groq import ChatGroq
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
import config

def load_vector_db():
    embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    if os.path.exists(config.VECTOR_DB_PATH):
        return FAISS.load_local(config.VECTOR_DB_PATH, embeddings, allow_dangerous_deserialization=True)
    return None

def ask_question(query: str, chat_history: list, api_key: str, use_smart_model: bool = False):
    db = load_vector_db()
    if not db:
        return "Database is empty.", [], 0.0

    model_name = config.LLM_SMART if use_smart_model else config.LLM_FAST
    llm = ChatGroq(groq_api_key=api_key, model_name=model_name)
    
    # 1. Contextualize Question Prompt (Rephrasing for history)
    contextualize_q_system_prompt = """Given a chat history and the latest user question 
    which might reference context in the chat history, formulate a standalone question 
    which can be understood without the chat history. Do NOT answer the question, 
    just reformulate it if needed and otherwise return it as is."""
    
    contextualize_q_prompt = ChatPromptTemplate.from_messages([
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])
    
    # 2. Answer Question Prompt (STRICT ENTERPRISE MODE)
    # This prevents the AI from answering questions about Google, Football, etc.
    qa_system_prompt = """You are a strict Enterprise Analyst. 
    Use the following pieces of retrieved context to answer the question.
    
    CRITICAL RULES:
    1. You must answer ONLY using the information present in the Context.
    2. If the user asks about a topic that is NOT in the Context (e.g., "Google", "Facebook", general knowledge), 
       you MUST say: "I cannot find information about this topic in the uploaded documents."
    3. Do NOT make up answers. Do NOT use your internal training data.
    4. CITATION IS REQUIRED: For every fact, explicitly mention the Source (filename).
    
    Context: {context}"""
    
    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])

    # 3. Document Formatting (To show Filenames in Context)
    document_prompt = PromptTemplate(
        input_variables=["page_content", "source"],
        template="Source: {source}\nContent: {page_content}"
    )

    # 4. Chain Construction
    retriever = db.as_retriever(search_kwargs={"k": config.RETRIEVAL_SEARCH_K})
    
    history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)
    
    question_answer_chain = create_stuff_documents_chain(
        llm, 
        qa_prompt,
        document_prompt=document_prompt,
        document_variable_name="context"
    )
    
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    # 5. Execute
    start = time.time()
    response = rag_chain.invoke({"input": query, "chat_history": chat_history})
    end = time.time()

    return response["answer"], response["context"], (end - start)