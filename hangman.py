"""
Hangman - simple console game.
Plain Python 3, no external libraries, no graphics or audio.
"""

import random

# A small predefined list of 5 words
WORDS = ["python", "banana", "rocket", "guitar", "planet"]

MAX_WRONG = 6  # maximum number of incorrect guesses allowed

# ASCII hangman stages - index = number of wrong guesses so far
HANGMAN_PICS = [
    """
     +---+
     |   |
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
    =========""",
    """
     +---+
     |   |
     O   |
     |   |
         |
    =========""",
    """
     +---+
     |   |
     O   |
    /|   |
         |
    =========""",
    """
     +---+
     |   |
     O   |
    /|\\  |
         |
    =========""",
    """
     +---+
     |   |
     O   |
    /|\\  |
    /    |
    =========""",
    """
     +---+
     |   |
     O   |
    /|\\  |
    / \\  |
    =========""",
]


def display_word(secret, guessed):
    """Show the word with underscores for letters not yet guessed."""
    return " ".join(letter if letter in guessed else "_" for letter in secret)


def get_guess(guessed):
    """Ask for one new letter; reject invalid or repeated input."""
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


def play_round():
    """Play one game. Returns True if the player wins."""
    secret = random.choice(WORDS)  # pick a random word
    guessed = set()                # letters already tried
    wrong = 0                      # count of incorrect guesses

    while True:
        print(HANGMAN_PICS[wrong])
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

        # Win: every letter of the secret word has been guessed
        if all(letter in guessed for letter in secret):
            print(HANGMAN_PICS[wrong])
            print(f"\nThe word was: {secret.upper()}")
            print("You Win! (+10 points)\n")
            return True

        # Lose: no attempts left
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
    """Game loop with a running score."""
    print("=" * 32)
    print("      WELCOME TO HANGMAN")
    print("=" * 32)

    score = 0
    while True:
        if play_round():
            score += 10  # +10 for a win, 0 for a loss
        print(f"Total score: {score}")
        if not play_again():
            break

    print(f"\nThanks for playing! Final score: {score}")


if __name__ == "__main__":
    main()
