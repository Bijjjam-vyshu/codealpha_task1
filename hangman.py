"""
Hangman - a beginner-friendly terminal game.
Runs with plain Python 3, no external libraries needed.
"""

import random

# ---------------------------------------------------------------------------
# 1. WORD BANK - categories with words (30+ words in total)
# ---------------------------------------------------------------------------
WORDS = {
    "Animals": [
        "elephant", "giraffe", "kangaroo", "dolphin", "penguin",
        "leopard", "squirrel", "crocodile", "butterfly", "hedgehog",
    ],
    "Fruits": [
        "banana", "pineapple", "strawberry", "watermelon", "mango",
        "blueberry", "pomegranate", "apricot", "coconut", "raspberry",
    ],
    "Countries": [
        "india", "brazil", "canada", "germany", "australia",
        "japan", "norway", "mexico", "portugal", "thailand",
    ],
    "Technology": [
        "python", "keyboard", "database", "algorithm", "internet",
        "compiler", "network", "software", "processor", "encryption",
    ],
}

MAX_WRONG = 6  # maximum number of incorrect guesses allowed

# ---------------------------------------------------------------------------
# 2. HANGMAN ASCII STAGES - index = number of wrong guesses so far
# ---------------------------------------------------------------------------
HANGMAN_PICS = [
    """
     +---+
     |   |
         |
         |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
         |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
     |   |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
    /|   |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
    /|\\  |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
    /|\\  |
    /    |
         |
    =========""",
    """
     +---+
     |   |
     O   |
    /|\\  |
    / \\  |
         |
    =========""",
]


def choose_category():
    """Show the categories and let the player pick one by number."""
    categories = list(WORDS.keys())
    print("\nChoose a category:")
    for index, name in enumerate(categories, start=1):
        print(f"  {index}. {name}")

    while True:
        choice = input("Enter category number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(categories):
            return categories[int(choice) - 1]
        print("Invalid choice. Please enter a number from the list.")


def pick_word(category):
    """Return a random word from the chosen category."""
    return random.choice(WORDS[category])


def display_word(secret, guessed):
    """Build the masked word, e.g. 'p y _ h o _'."""
    return " ".join(letter if letter in guessed else "_" for letter in secret)


def get_guess(guessed):
    """Ask for a single new letter, rejecting invalid or repeated input."""
    while True:
        guess = input("Guess a letter: ").strip().lower()
        if len(guess) != 1:
            print("Please enter exactly one character.")
        elif not guess.isalpha():
            print("Letters only - no numbers or symbols.")
        elif guess in guessed:
            print(f"You already guessed '{guess}'. Try another letter.")
        else:
            return guess


def play_round(category):
    """Play one full game. Returns True if the player wins."""
    secret = pick_word(category)
    guessed = set()      # every letter the player has tried
    wrong = 0            # number of incorrect guesses

    while True:
        print(HANGMAN_PICS[wrong])
        print(f"Category: {category}")
        print("Word: ", display_word(secret, guessed))
        print("Guessed letters:", " ".join(sorted(guessed)) or "(none)")
        print(f"Attempts remaining: {MAX_WRONG - wrong}")

        guess = get_guess(guessed)
        guessed.add(guess)

        if guess in secret:
            print(f"Good guess! '{guess}' is in the word.")
        else:
            wrong += 1
            print(f"Sorry, '{guess}' is not in the word.")

        # Win check: every letter of the secret word has been guessed
        if all(letter in guessed for letter in secret):
            print(HANGMAN_PICS[wrong])
            print(f"\nThe word was: {secret.upper()}")
            print("You Win! (+10 points)\n")
            return True

        # Lose check: no attempts left
        if wrong == MAX_WRONG:
            print(HANGMAN_PICS[wrong])
            print(f"\nGame Over! The word was: {secret.upper()} (+0 points)\n")
            return False


def play_again():
    """Ask the player if they want another round."""
    while True:
        answer = input("Play again? (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please answer with 'y' or 'n'.")


def main():
    """Game loop: category -> round -> score -> replay."""
    print("=" * 40)
    print("        WELCOME TO HANGMAN")
    print("=" * 40)

    score = 0
    while True:
        category = choose_category()
        if play_round(category):
            score += 10  # +10 for a win, 0 for a loss
        print(f"Total score: {score}")

        if not play_again():
            break

    print(f"\nThanks for playing! Final score: {score}")


if __name__ == "__main__":
    main()
