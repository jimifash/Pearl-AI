from client_process import get_response
from game import synonym_game



def main():
    print("Welcome to the English Learning Chatbot!")
    print("Type 'exit' to end the conversation.\n")

    choice = input("Would you like to play a game or just chat? \nType 'game' to play \nType 'chat' to just chat: ").strip().lower()

    if choice == 'game':
        synonym_game()

    elif choice == 'chat':
        print("\nYou are now in chat mode! Type 'exit' to end the chat.\n")
        print("\nI am Pearl your personal AI english tutor")
        print("Please be specific with questions to enable me respond accordingly")
        while True:
            user_input = input("You: ").strip()

            if user_input.lower() == 'exit':
                print("Goodbye!")
                break

            # Get response from the bot
            bot_response = get_response(user_input)
            print(f"Bot: {bot_response.content}")

    else:
        print("Invalid choice. Please restart and type 'game' or 'chat'.")

if __name__ == "__main__":
    main()