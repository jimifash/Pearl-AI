import streamlit as st
from client_process import get_response  # Ensure you have this function available
from game import synonym_game  # Ensure this game function is available

def main():
    st.title("English Learning Chatbot")
    st.write("Welcome to the chatbot! Type 'exit' to end the conversation.")
    
    # Initialize chat history in session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # User chooses between chat or game
    choice = st.selectbox(
        "Would you like to play a game or just chat?", 
        ['game', 'chat']
    )

    # If user selects 'game'
    if choice == 'game':
        st.write("Let's play the synonym game!")
        synonym_game()  # Ensure the game is interactive and doesn't block the UI

    # If user selects 'chat'
    elif choice == 'chat':
        st.write("\nYou are now in chat mode! Type 'exit' to end the chat.")
        st.write("I am Pearl, your personal AI English tutor! Please be specific with questions to enable me to respond accordingly.")
        
        user_input = st.text_input("You:", "")
        
        if user_input.lower() == 'exit':
            st.write("Goodbye!")
            st.session_state.chat_history = []  # Clear chat history when exit
        elif user_input:
            # Append user input and bot response to chat history
            st.session_state.chat_history.append(f"You: {user_input}")
            bot_response = get_response(user_input)  # Your chatbot logic here
            st.session_state.chat_history.append(f"Bot: {bot_response.content}")
        
    # Display chat history
    for message in st.session_state.chat_history:
        st.write(message)

if __name__ == "__main__":
    main()
