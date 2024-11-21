import random
import streamlit as st
from words import words

# Function to evaluate if the user's word is a synonym of the given word
def evaluate_synonym(word, user_word):
    user_word = user_word.lower()
    return user_word in words.get(word, [])

# Synonym game loop
def synonym_game():
    st.title("Synonym Game")
    st.write("I'll give you a word, and you need to type a synonym for it.")
    st.write("Type 'exit' to stop playing the game.\n")

    # Initialize session state variables
    if "score" not in st.session_state:
        st.session_state.score = 0  # Initialize score to 0
        st.session_state.current_word = random.choice(list(words.keys()))  # Pick the first random word
        st.session_state.game_over = False  # Track whether the game is over
        st.session_state.waiting_for_next = False  # To manage the "Next" button state

    # If the game is over, display the final score
    if st.session_state.game_over:
        st.write("❌ Game Over!")
        st.write(f"Your final score: **{st.session_state.score}**")
        if st.button("Restart"):
            # Reset session state to restart the game
            st.session_state.score = 0
            st.session_state.current_word = random.choice(list(words.keys()))
            st.session_state.game_over = False
            st.session_state.waiting_for_next = False
        return

    # Display the current word
    word = st.session_state.current_word

    if not st.session_state.waiting_for_next:
        st.write(f"What's a synonym for **{word}**?")
        # Input box for user answer
        user_word = st.text_input("Your answer: ", key="user_input")

        # Submit button to check the answer
        if st.button("Submit"):
            if user_word.lower() == "exit":
                st.write("You typed 'exit'. Thanks for playing!")
                st.write(f"Your final score: **{st.session_state.score}**")
                st.session_state.game_over = True
            elif evaluate_synonym(word, user_word):
                st.session_state.score += 1
                st.session_state.waiting_for_next = True  # Set the flag to show "Next" button
                st.success("✅ Correct! Click 'Next' to continue.")
            else:
                correct_answers = ", ".join(words[word])
                st.write(f"❌ Incorrect! A synonym could be: {correct_answers}.")
                st.session_state.game_over = True  # Mark the game as over
    else:
        # Show "Next" button to proceed to the next word
        next_word_button = st.button("Next")
        if next_word_button:
            st.session_state.current_word = random.choice(list(words.keys()))  # Pick the next random word
            st.session_state.waiting_for_next = False  # Reset for the next word

