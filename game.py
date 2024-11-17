#libraries
import random
from words import words

# Function to evaluate if the user's word is a synonym of the given word
def evaluate_synonym(word, user_word):
    user_word = user_word.lower()
    if user_word in words.get(word, []):
        return True
    return False

# Synonym game loop
def synonym_game():
    print("\nWelcome to the Synonym Game!")
    print("I'll give you a word, and you need to type a synonym for it.")
    print("Type 'exit' to stop playing the game.\n")

    while True:
        word = random.choice(list(words.keys()))
        print(f"What's a synonym for '{word}'?")
        user_word = input("You: ").strip().lower()

        if user_word == 'exit':
            print("Exiting the game. Thanks for playing!")
            break

        # Check if the user's word is a valid synonym
        if evaluate_synonym(word, user_word):
            print("Correct! Well done!")
        else:
            print(f"Oops! Some correct answers could be: {', '.join(words[word])}. Try again!")