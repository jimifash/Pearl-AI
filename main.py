import streamlit as st
from client_process import get_response
from game import synonym_game  
from translate_input import trans_text 


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
        #Initialize preferred language
        lang = st.text_input("Enter your preferred language (e.g., 'fr' for French):")
        if not lang:
            st.warning("Please enter a valid language code.")


        st.write(f"""\n{trans_text("You are now in chat mode! Type 'exit' to end the chat.", lang)}""")
        st.write(f'{trans_text("I am Pearl, your personal AI English tutor! Please be specific with questions to enable me to respond accordingly.", lang)}')
        
        user_input = st.text_input(trans_text("You:", lang), "")
        
        if user_input.lower() == 'exit':
            st.write("Goodbye!")
            st.session_state.chat_history = []  # Clear chat history when exit
        elif user_input:
            bot_response = get_response(user_input, lang)  # Your chatbot logic here


    # Only display the most recent user input and bot response
    for message in st.session_state.chat_history:
        st.write(message)

if __name__ == "__main__":
    main()

