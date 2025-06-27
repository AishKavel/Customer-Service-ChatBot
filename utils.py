from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, Tool, AgentType
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()
groq_api_key = "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"
assert groq_api_key, "GROQ_API_KEY must be set."

# Initialize embeddings and database
embeddings_model_name = os.getenv("EMBEDDINGS_MODEL_NAME", "all-MiniLM-L6-v2")
persist_directory = os.getenv("PERSIST_DIRECTORY", "db")
embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
retriever = db.as_retriever(search_kwargs={"k": 5})

# Initialize LLM
llm = ChatGroq(model_name="mixtral-8x7b-32768", groq_api_key=groq_api_key)
memory = ConversationBufferMemory()


# Define tools
def extract_related_context(docs):
    related_context = ""
    for doc in docs:
        related_context += f"\n> {doc.metadata['source']}:\n{doc.page_content}\n"
    return related_context

# def generate_related_questions(parent_question, related_context):
#     query = f"""What are related questions for '{parent_question}' and make sure it will be one based on:\n{related_context}. and generate based on related context quickly."""
#     try:
#         return llm.invoke(query)
#     except Exception as e:
#         print(f"Error generating related questions: {e}")
#         return "Error generating related questions."

def generate_rag_response(query):
    try:
        start_time = time.time()
        answer = agent.invoke({"input": query})
        end_time = time.time()
        print(f"RAG QA completed in {end_time - start_time:.2f}s")
        return answer
    except Exception as e:
        print(f"Error: {e}")
        return "Error generating response."

tools = [
    Tool(name="Retriever", func=retriever.get_relevant_documents, description="Fetch relevant documents from the database but don't go deeper just get the basic information and give response quickly."),
    Tool(name="FinalAnswerGenerator", func=generate_rag_response, description="Generate final answer from retriever which is then passed to RAG for final answer generation quickly dont take time and make it interactive."),
]

agent = initialize_agent(tools, llm=llm, agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, memory=memory, verbose=True)