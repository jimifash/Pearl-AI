#Import libraries
from langchain_groq import ChatGroq
import chromadb
from sentence_transformers import SentenceTransformer
from pdf_embed import collection
from dotenv import load_dotenv
import uuid
import os
import streamlit as st
from language_codes import LANGUAGES



load_dotenv()

# Initialize the ChatGroq client

#Chat

client = ChatGroq(
    model='llama3-8b-8192',
    groq_api_key= os.getenv("GROQ_API_KEY"),  # replace with your actual API key
    temperature=0
)

client2 = chromadb.PersistentClient(path=r'chat_history')


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


MAX_MEMORY_SIZE = 100 #limit for storage to prevent overload

def store(user_input, bot_response):
    """Store chat history and manage memory size."""
    documents = [user_input, bot_response]
    if not documents or not all(isinstance(doc, str) for doc in documents):  ## Error handling
        raise ValueError("Documents must be a non-empty list of strings.")
    embedding2 = model.encode(documents)
    ids = [generate_id(user_input), generate_id(bot_response)]

    # Remove oldest entries if the memory size exceeds the limit
    history = collection2.get()
    if history and 'ids' in history and len(history['ids']) >= MAX_MEMORY_SIZE:
        collection2.delete(ids=[history['ids'][0]]) # Remove the oldest record


    #stores the documents in the Chat history collection 
    collection2.add(
        documents =documents,
        ids =ids,
        embeddings = embedding2
    )




'''def Retrieve(query):
    """Retrieves chat history from Chromadb"""
    query_embedding = model.encode(query)
    results = collection2.query(query_embeddings = query_embedding, n_results = 1)

    if results["documents"]:
            #print(results)  # Optional: See the full response structure
            # Return the first matching document
            return results["documents"][0]
    else:
        return None'''





def Retrieve_pdf(query):
  """Retrieve pdf contents and return results"""
  embed = model.encode(query)
  results = collection.query(query_embeddings = embed, n_results = 3)

  if results["documents"]:
    return results["documents"][0]
  else:
      return None




def get_response(user_input, lang):
    """Generate bot response and use ChromaDB for context if available."""

    # Initialize chat history if not already present
    '''if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []'''

    # Optional: Retrieve past context or response from ChromaDB
    # relevant_response = Retrieve(user_input)  
    relevant_response2 = Retrieve_pdf(user_input)  # Example of retrieving from PDF

    # Build context from chat history if available
    if st.session_state.chat_history:
        MAX_MESSAGE_LENGTH = 500  # Limit each message length in context
        context = collection2.get()
        context = context[:MAX_MESSAGE_LENGTH] + "..." if len(context) >MAX_MESSAGE_LENGTH else context  # Limit total context size


        messages = [
            ("system", (
            "You are Pearl, a friendly and engaging {0} speaker and English tutor who speaks with the user in their preferred language, {0}."
            "You correct grammatical errors and help improve english of its students. Do not introduce yourself again. Always Ensure to correct mistakes"
            "Your goal is to help the user improve their English by responding in {0}, but always providing clear corrections and explanations in English. Use {2} to get relevant answers to english related questions. Don't be too critical unless it is a blunder"
            "Simply continue the conversation based on the user's input. Always Correct mistakes in grammar, lexis, and sentence structure when necessary using information from {2}. "
            "Do not refer to past mistakes unless they are made immediately. Use insights from previous messages to guide the conversation and provide relevant corrections."
            "When the user makes mistakes in English, gently correct them and explain the correction in {0}, so they understand why the change was made. "
            "Always encourage the user and keep the conversation flowing naturally, so they feel supported and confident in their learning."
            "If the user asks for explanations (like 'explain' or '¿puedes explicar?'), provide context and corrections in {0}, making sure they understand the English structure."
            "You use the history: {1}, to understand the flow of the conversation to keep it natural"
            "Remember to Correct mistakes."
            ).format(LANGUAGES.get(lang), context, relevant_response2)),
            ("human", f"User: {user_input}")


        ]
    else:
        messages = [
            ("system", (
               "You are Pearl, a friendly and engaging English tutor. "
                "Your task is to correct grammatical errors and help improve English fluency. "
                "If the user says something incorrect, gently correct it and provide an explanation."
            )),
            ("human", f"User: {user_input}")

        ]

    try:
        # Invoke the chatbot client
        response = client.invoke(messages)

        # Store chat history for context
        st.session_state.chat_history.append(f"You: {user_input}")
        st.session_state.chat_history.append(f"Pearl: {response.content}")


        # Optionally store the conversation externally
        store(user_input, str(response))

        return response
    except Exception as e:
        # Log the error and return a friendly error message
        import logging
        logging.error(f"Error invoking chatbot: {e}")
        return f"Sorry, I couldn't process your request due to an error: {str(e)}"
