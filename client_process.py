#Import libraries
from langchain_groq import ChatGroq
import chromadb
from sentence_transformers import SentenceTransformer
from pdf_embed import collection
from dotenv import load_dotenv
import uuid
import os




load_dotenv()

# Initialize the ChatGroq client

#Chat

client = ChatGroq(
    model='llama3-8b-8192',
    groq_api_key= os.getenv("GROQ_API_KEY"),  # replace with your actual API key
    temperature=0
)

client2 = chromadb.PersistentClient()


#ID generator to store data in the vector database
response_ext = ["Hi Jimi. I would be you English buddy"]
user_ext = ["My name is Jimi"]

def generate_id(prefix):
    """Generate a unique ID using a prefix."""
    return f"{prefix}_{uuid.uuid4().hex}"  # Generates a random unique ID


#Getting pdf collection and storing it in a Variable called Collection
collection = collection




#Creating collection for chat history
collection2 = client2.get_or_create_collection(name = "history")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def store(user_input, bot_response):


    """Stores Chat history in Chromadb"""
    documents =[user_input, bot_response] #Stores user input and bot_response in  document
    embedding2 = model.encode(documents)
    ids = [generate_id(user_input), generate_id(bot_response)]


    #stores the documents in the Chat history collection 
    collection2.add(
        documents =documents,
        ids =ids,
        embeddings = embedding2
    )




def Retrieve(query):
    """Retrieves chat history from Chromadb"""
    query_embedding = model.encode(query)
    results = collection2.query(query_embeddings = query_embedding, n_results = 1)

    if results["documents"]:
            #print(results)  # Optional: See the full response structure
            # Return the first matching document
            return results["documents"][0]
    else:
        return None



def Retrieve_pdf(query):
  """Retrieve pdf contents and return results"""
  embed = model.encode(query)
  results = collection.query(query_embeddings = embed, n_results = 3)

  if results["documents"]:
    return results["documents"][0]
  else:
      return None





def get_response(user_input):
    """Generate bot response and use ChromaDB for context if available."""
    # Try to retrieve a relevant past conversation from the database
    relevant_response = Retrieve(user_input)
    relevant_response2 = Retrieve_pdf(user_input)
    #print(relevant_response2)

    if relevant_response:
        messages = [
            ("system", f"You are Pearl, a friendly and engaging English tutor who corrects grammatical errors and help improve english of its students. Do not introduce yourself again. Ensure to correct mistakes. Simply continue the conversation based on the user's input. Correct mistakes in grammar, lexis, and sentence structure when necessary. Keep the conversation flowing naturally while offering the corrections. The user’s previous response is there to maintain the flow, but do not repeat it. Use insights from previous messages to guide the conversation and provide relevant corrections. If the user says 'explain' without specifying what to explain, use {relevant_response} to provide an answer."),
            ("human", f"User: {user_input}\n Previous response: {relevant_response}")
        ]
    else:
        messages = [
            ("system", f"Your name is Pearl. You a friendly and engaging English tutor. Correct mistakes when necessary, and keep the conversation flowing naturally.  Start the conversation by introducing yourself but avoid introducing yourself more than once."),
            ("human", f"User: {user_input}")
        ]


    try:
      response = client.invoke(messages)
    #stores chat history
      store(user_input, str(response))

      return response
    except Exception as e:
        return f"Error: {str(e)}"
