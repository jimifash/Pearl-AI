"# Pearl-AI" 
# Pearl: Your Personal English Tutor Chatbot

**Pearl** is an AI-powered chatbot designed to help users improve their English skills through natural, conversational interactions. Using advanced AI models and a memory system that recalls previous conversations, Pearl offers a personalized learning experience that adapts to your needs over time.

## Features

- **Engaging Conversations**: Pearl engages users in natural conversation, correcting grammar, improving sentence structure, and enhancing vocabulary.
- **Context-Aware**: Pearl remembers past interactions and integrates them into future conversations, making each exchange more personalized and relevant.
- **Grammar & Vocabulary Corrections**: The bot offers real-time feedback on grammar mistakes and helps users expand their vocabulary.
- **PDF Integration**: Pearl can extract useful information from PDF documents to answer questions and assist with learning.
- **Persistent Chat History**: The chatbot stores conversation history to maintain context and improve responses based on previous interactions.

## How It Works

1. **Chat History**: Pearl saves conversation data in a vector database (ChromaDB) to keep track of context. When a user asks a question, Pearl retrieves relevant previous exchanges to maintain continuity.
2. **Response Generation**: Using the LLaMA model (Llama3-8B), Pearl generates responses based on user input and past conversations, ensuring the chat feels more natural and coherent.
3. **PDF Querying**: The bot can access and process PDFs, allowing users to ask questions about specific content stored in the document.

## Installation

To get started with Pearl, you'll need to set up the environment and install the required dependencies.

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/pearl-chatbot.git
cd pearl-chatbot

## Install dependencies
pip install -r requirements.txt

## Setup environment Vaiables:
 Create a .env file in the project root directory and add your Groq API

 ## Run:
 streamlit run main.py


