"""
Hangman Quest - console version.
Pure Python 3. No external libraries, no graphics, no audio.

Sections:
  1. LEVELS        - 500 words with categories, ordered easy (short) to hard (long)
  2. ART           - ASCII gallows stages + a small ASCII picture clue per category
  3. Game helpers  - masking the word, validating input, hints
  4. play_level    - one level of play
  5. main          - level progression, difficulty menu, score, saving progress
"""

import json
import os
import random

# ---------------------------------------------------------------- 1. LEVELS
# (word, category) - sorted by length so the game gets harder as you progress.
LEVELS = [
    ("ant", "Animals"), ("api", "Technology"), ("app", "Technology"), ("bag", "Everyday"),
    ("bat", "Animals"), ("bay", "Nature"), ("bed", "Everyday"), ("bee", "Animals"),
    ("bit", "Technology"), ("box", "Everyday"), ("bud", "Nature"), ("cap", "Everyday"),
    ("cat", "Animals"), ("cow", "Animals"), ("cup", "Everyday"), ("dew", "Nature"),
    ("dog", "Animals"), ("elk", "Animals"), ("elm", "Nature"), ("fan", "Everyday"),
    ("fig", "Fruits"), ("fog", "Nature"), ("fox", "Animals"), ("hat", "Everyday"),
    ("hen", "Animals"), ("ice", "Nature"), ("ivy", "Nature"), ("jar", "Everyday"),
    ("key", "Everyday"), ("log", "Nature"), ("mud", "Nature"), ("mug", "Everyday"),
    ("oak", "Nature"), ("owl", "Animals"), ("pan", "Everyday"), ("pen", "Everyday"),
    ("pig", "Animals"), ("pot", "Everyday"), ("ram", "Animals"), ("rug", "Everyday"),
    ("sea", "Nature"), ("ski", "Sports"), ("sky", "Nature"), ("sun", "Nature"),
    ("web", "Technology"), ("yak", "Animals"), ("bear", "Animals"), ("belt", "Everyday"),
    ("book", "Everyday"), ("bowl", "Everyday"), ("byte", "Technology"), ("cake", "Food"),
    ("cave", "Nature"), ("chad", "Countries"), ("chip", "Technology"), ("code", "Technology"),
    ("coin", "Everyday"), ("comb", "Everyday"), ("crab", "Animals"), ("crow", "Animals"),
    ("cuba", "Countries"), ("data", "Technology"), ("date", "Fruits"), ("deer", "Animals"),
    ("desk", "Everyday"), ("disk", "Technology"), ("door", "Everyday"), ("drum", "Music"),
    ("duck", "Animals"), ("dune", "Nature"), ("fawn", "Animals"), ("fern", "Nature"),
    ("fiji", "Countries"), ("file", "Technology"), ("fork", "Everyday"), ("frog", "Animals"),
    ("goal", "Sports"), ("goat", "Animals"), ("golf", "Sports"), ("gulf", "Nature"),
    ("hail", "Nature"), ("harp", "Music"), ("hawk", "Animals"), ("hill", "Nature"),
    ("host", "Technology"), ("iran", "Countries"), ("iraq", "Countries"), ("judo", "Sports"),
    ("kiwi", "Fruits"), ("lake", "Nature"), ("lamp", "Everyday"), ("laos", "Countries"),
    ("leaf", "Nature"), ("lime", "Fruits"), ("link", "Technology"), ("lion", "Animals"),
    ("lynx", "Animals"), ("mali", "Countries"), ("mist", "Nature"), ("mole", "Animals"),
    ("moon", "Nature"), ("moss", "Nature"), ("mule", "Animals"), ("node", "Technology"),
    ("oman", "Countries"), ("palm", "Nature"), ("peak", "Nature"), ("pear", "Fruits"),
    ("peru", "Countries"), ("pine", "Nature"), ("plum", "Fruits"), ("port", "Technology"),
    ("puma", "Animals"), ("race", "Sports"), ("rain", "Nature"), ("reef", "Nature"),
    ("rice", "Food"), ("ring", "Everyday"), ("rock", "Nature"), ("root", "Nature"),
    ("rope", "Everyday"), ("sand", "Nature"), ("seal", "Animals"), ("seed", "Nature"),
    ("shoe", "Everyday"), ("sink", "Everyday"), ("snow", "Nature"), ("sock", "Everyday"),
    ("sofa", "Everyday"), ("soil", "Nature"), ("soup", "Food"), ("star", "Nature"),
    ("surf", "Sports"), ("swan", "Animals"), ("swim", "Sports"), ("taco", "Food"),
    ("toad", "Animals"), ("togo", "Countries"), ("tree", "Nature"), ("user", "Technology"),
    ("wave", "Nature"), ("wifi", "Technology"), ("wind", "Nature"), ("wolf", "Animals"),
    ("yoga", "Sports"), ("apple", "Fruits"), ("array", "Technology"), ("banjo", "Music"),
    ("beach", "Nature"), ("berry", "Fruits"), ("bison", "Animals"), ("bread", "Food"),
    ("brush", "Everyday"), ("cache", "Technology"), ("camel", "Animals"), ("cello", "Music"),
    ("chair", "Everyday"), ("chile", "Countries"), ("china", "Countries"), ("cliff", "Nature"),
    ("clock", "Everyday"), ("cloud", "Technology"), ("coral", "Nature"), ("creek", "Nature"),
    ("debug", "Technology"), ("delta", "Nature"), ("eagle", "Animals"), ("egypt", "Countries"),
    ("email", "Technology"), ("field", "Nature"), ("finch", "Animals"), ("flute", "Music"),
    ("frost", "Nature"), ("gecko", "Animals"), ("ghana", "Countries"), ("glass", "Everyday"),
    ("grass", "Nature"), ("guava", "Fruits"), ("haiti", "Countries"), ("heron", "Animals"),
    ("honey", "Food"), ("horse", "Animals"), ("hyena", "Animals"), ("india", "Countries"),
    ("input", "Technology"), ("italy", "Countries"), ("japan", "Countries"), ("jeans", "Everyday"),
    ("kenya", "Countries"), ("knife", "Everyday"), ("koala", "Animals"), ("lemon", "Fruits"),
    ("libya", "Countries"), ("llama", "Animals"), ("malta", "Countries"), ("mango", "Fruits"),
    ("marsh", "Nature"), ("melon", "Fruits"), ("moose", "Animals"), ("mouse", "Animals"),
    ("nepal", "Countries"), ("ocean", "Nature"), ("olive", "Fruits"), ("otter", "Animals"),
    ("panda", "Animals"), ("pasta", "Food"), ("peach", "Fruits"), ("phone", "Everyday"),
    ("piano", "Music"), ("pixel", "Technology"), ("plate", "Everyday"), ("purse", "Everyday"),
    ("qatar", "Countries"), ("query", "Technology"), ("raven", "Animals"), ("rhino", "Animals"),
    ("ridge", "Nature"), ("river", "Nature"), ("robot", "Technology"), ("route", "Technology"),
    ("rugby", "Sports"), ("salad", "Food"), ("shark", "Animals"), ("sheep", "Animals"),
    ("shirt", "Everyday"), ("shore", "Nature"), ("sloth", "Animals"), ("snake", "Animals"),
    ("spain", "Countries"), ("spoon", "Everyday"), ("stone", "Nature"), ("storm", "Nature"),
    ("sudan", "Countries"), ("swamp", "Nature"), ("syria", "Countries"), ("table", "Everyday"),
    ("tiger", "Animals"), ("towel", "Everyday"), ("viper", "Animals"), ("watch", "Everyday"),
    ("whale", "Animals"), ("yemen", "Countries"), ("zebra", "Animals"), ("angola", "Countries"),
    ("badger", "Animals"), ("banana", "Fruits"), ("basket", "Everyday"), ("beaver", "Animals"),
    ("binary", "Technology"), ("boxing", "Sports"), ("brazil", "Countries"), ("buffer", "Technology"),
    ("butter", "Food"), ("canada", "Countries"), ("candle", "Everyday"), ("canyon", "Nature"),
    ("carpet", "Everyday"), ("cheese", "Food"), ("cherry", "Fruits"), ("chorus", "Music"),
    ("cipher", "Technology"), ("client", "Technology"), ("cookie", "Food"), ("cougar", "Animals"),
    ("cursor", "Technology"), ("daemon", "Technology"), ("desert", "Nature"), ("device", "Technology"),
    ("domain", "Technology"), ("donkey", "Animals"), ("durian", "Fruits"), ("falcon", "Animals"),
    ("ferret", "Animals"), ("forest", "Nature"), ("france", "Countries"), ("grapes", "Fruits"),
    ("greece", "Countries"), ("guinea", "Countries"), ("guitar", "Music"), ("hockey", "Sports"),
    ("iguana", "Animals"), ("island", "Nature"), ("israel", "Countries"), ("jaguar", "Animals"),
    ("jordan", "Countries"), ("jungle", "Nature"), ("karate", "Sports"), ("kernel", "Technology"),
    ("laptop", "Technology"), ("lizard", "Animals"), ("lychee", "Fruits"), ("meadow", "Nature"),
    ("melody", "Music"), ("memory", "Technology"), ("mexico", "Countries"), ("mirror", "Everyday"),
    ("module", "Technology"), ("monkey", "Animals"), ("muffin", "Food"), ("noodle", "Food"),
    ("norway", "Countries"), ("orange", "Fruits"), ("packet", "Technology"), ("panama", "Countries"),
    ("papaya", "Fruits"), ("parrot", "Animals"), ("pepper", "Food"), ("pillow", "Everyday"),
    ("plugin", "Technology"), ("poland", "Countries"), ("quince", "Fruits"), ("rabbit", "Animals"),
    ("rhythm", "Music"), ("router", "Technology"), ("russia", "Countries"), ("rwanda", "Countries"),
    ("salmon", "Animals"), ("screen", "Technology"), ("script", "Technology"), ("serbia", "Countries"),
    ("server", "Technology"), ("soccer", "Sports"), ("socket", "Technology"), ("spider", "Animals"),
    ("sweden", "Countries"), ("syntax", "Technology"), ("tablet", "Technology"), ("tennis", "Sports"),
    ("tundra", "Nature"), ("turkey", "Countries"), ("turtle", "Animals"), ("uganda", "Countries"),
    ("valley", "Nature"), ("violin", "Music"), ("waffle", "Food"), ("walrus", "Animals"),
    ("weasel", "Animals"), ("widget", "Technology"), ("window", "Everyday"), ("zambia", "Countries"),
    ("apricot", "Fruits"), ("archery", "Sports"), ("armenia", "Countries"), ("austria", "Countries"),
    ("avocado", "Fruits"), ("backend", "Technology"), ("belgium", "Countries"), ("bicycle", "Everyday"),
    ("blanket", "Everyday"), ("blossom", "Nature"), ("bolivia", "Countries"), ("bowling", "Sports"),
    ("browser", "Technology"), ("buffalo", "Animals"), ("cheetah", "Animals"), ("cluster", "Technology"),
    ("coconut", "Fruits"), ("compile", "Technology"), ("concert", "Music"), ("console", "Technology"),
    ("cricket", "Sports"), ("currant", "Fruits"), ("cycling", "Sports"), ("denmark", "Countries"),
    ("desktop", "Technology"), ("dolphin", "Animals"), ("ecuador", "Countries"), ("encrypt", "Technology"),
    ("finland", "Countries"), ("gateway", "Technology"), ("georgia", "Countries"), ("germany", "Countries"),
    ("giraffe", "Animals"), ("glacier", "Nature"), ("gorilla", "Animals"), ("hamster", "Animals"),
    ("hosting", "Technology"), ("hungary", "Countries"), ("iceberg", "Nature"), ("iceland", "Countries"),
    ("ireland", "Countries"), ("leopard", "Animals"), ("library", "Technology"), ("monitor", "Technology"),
    ("morocco", "Countries"), ("network", "Technology"), ("nigeria", "Countries"), ("octopus", "Animals"),
    ("ostrich", "Animals"), ("pancake", "Food"), ("peacock", "Animals"), ("pelican", "Animals"),
    ("penguin", "Animals"), ("prairie", "Nature"), ("process", "Technology"), ("program", "Technology"),
    ("raccoon", "Animals"), ("rainbow", "Nature"), ("romania", "Countries"), ("running", "Sports"),
    ("runtime", "Technology"), ("skating", "Sports"), ("somalia", "Countries"), ("storage", "Technology"),
    ("sunrise", "Nature"), ("thunder", "Nature"), ("trumpet", "Music"), ("ukraine", "Countries"),
    ("vietnam", "Countries"), ("volcano", "Nature"), ("antelope", "Animals"), ("backpack", "Everyday"),
    ("baseball", "Sports"), ("clarinet", "Music"), ("colombia", "Countries"), ("computer", "Technology"),
    ("database", "Technology"), ("elephant", "Animals"), ("envelope", "Everyday"), ("firewall", "Technology"),
    ("flamingo", "Animals"), ("football", "Sports"), ("hardware", "Technology"), ("hedgehog", "Animals"),
    ("internet", "Technology"), ("kangaroo", "Animals"), ("keyboard", "Technology"), ("malaysia", "Countries"),
    ("mandarin", "Fruits"), ("marathon", "Sports"), ("mountain", "Nature"), ("omelette", "Food"),
    ("pakistan", "Countries"), ("paraguay", "Countries"), ("password", "Technology"), ("plantain", "Fruits"),
    ("portugal", "Countries"), ("protocol", "Technology"), ("sandwich", "Food"), ("savannah", "Nature"),
    ("scissors", "Everyday"), ("software", "Technology"), ("squirrel", "Animals"), ("srilanka", "Countries"),
    ("suitcase", "Everyday"), ("swimming", "Sports"), ("terminal", "Technology"), ("thailand", "Countries"),
    ("umbrella", "Everyday"), ("variable", "Technology"), ("woodland", "Nature"), ("accordion", "Music"),
    ("algorithm", "Technology"), ("alligator", "Animals"), ("argentina", "Countries"), ("australia", "Countries"),
    ("badminton", "Sports"), ("bandwidth", "Technology"), ("blueberry", "Fruits"), ("bluetooth", "Technology"),
    ("butterfly", "Animals"), ("chameleon", "Animals"), ("chocolate", "Food"), ("cranberry", "Fruits"),
    ("crocodile", "Animals"), ("framework", "Technology"), ("furniture", "Everyday"), ("indonesia", "Countries"),
    ("interface", "Technology"), ("mainframe", "Technology"), ("nectarine", "Fruits"), ("orchestra", "Music"),
    ("persimmon", "Fruits"), ("porcupine", "Animals"), ("processor", "Technology"), ("raspberry", "Fruits"),
    ("saxophone", "Music"), ("spaghetti", "Food"), ("tangerine", "Fruits"), ("telephone", "Everyday"),
    ("venezuela", "Countries"), ("waterfall", "Nature"), ("bangladesh", "Countries"), ("basketball", "Sports"),
    ("blackberry", "Fruits"), ("blockchain", "Technology"), ("chimpanzee", "Animals"), ("clementine", "Fruits"),
    ("encryption", "Technology"), ("filesystem", "Technology"), ("gooseberry", "Fruits"), ("gymnastics", "Sports"),
    ("javascript", "Technology"), ("kazakhstan", "Countries"), ("madagascar", "Countries"), ("mozambique", "Countries"),
    ("repository", "Technology"), ("rhinoceros", "Animals"), ("skateboard", "Sports"), ("strawberry", "Fruits"),
]

TOTAL_LEVELS = len(LEVELS)
SAVE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hangman_save.json")

MAX_LIVES = 6  # never more than 6 incorrect guesses

DIFFICULTIES = [
    ("Classic", 6, "The traditional hangman"),
    ("Steady", 5, "One strike tighter"),
    ("Hard", 4, "Every letter counts"),
    ("Brutal", 3, "Three strikes, that's it"),
    ("Insane", 2, "For sharp guessers only"),
]

# ------------------------------------------------------------------- 2. ART
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

# A small ASCII "picture clue" for each category - the console stand-in for images.
CATEGORY_ART = {
    "Animals": r"""
      /\_/\
     ( o.o )   a living creature
      > ^ <
""",
    "Fruits": r"""
        ,--./
       /    \    something you eat,
       \    /    grown on a plant
        `--'
""",
    "Countries": r"""
       ___
      /   \___   a place on the world map
      \_______/
""",
    "Technology": r"""
      .------.
      |[][][]|   machines, code and gadgets
      '------'
""",
    "Nature": r"""
        /\
       /  \  /\   outdoors: land, sky, weather
      /    \/  \
""",
    "Everyday": r"""
       ______
      |      |   an ordinary household thing
      |______|
""",
    "Sports": r"""
        ___
       (o o)    games and competition
       /|_|\
""",
    "Music": r"""
       o
      /|      sound, songs, instruments
     d
""",
    "Food": r"""
       (====)
      (      )   something cooked or served
       `----'
""",
}


def picture_clue(category):
    """Return the ASCII picture clue for a category."""
    return CATEGORY_ART.get(category, "   (no picture clue for this category)\n")


# --------------------------------------------------------- 3. Game helpers
def display_word(secret, guessed):
    """Show the word with underscores for letters not yet guessed."""
    return " ".join(letter if letter in guessed else "_" for letter in secret)


def max_hints(secret):
    """Roughly one hint per three different letters, at least two."""
    return max(2, len(set(secret)) // 3)


def give_hint(secret, guessed):
    """Reveal one random unguessed letter (never the last remaining one)."""
    remaining = [l for l in set(secret) if l not in guessed]
    if len(remaining) <= 1:
        print("Only one letter left - that one is yours to find!")
        return None
    letter = random.choice(remaining)
    print("Hint: the word contains the letter '%s'." % letter)
    return letter


def get_guess(guessed, hints_left, secret, category):
    """Ask for one new letter, or a command. Returns a letter, 'hint' or 'clue'."""
    while True:
        raw = input("Guess a letter (or 'hint' / 'clue'): ").strip().lower()
        if raw in ("hint", "clue"):
            if raw == "hint" and hints_left <= 0:
                print("No hints left.")
                continue
            return raw
        if len(raw) != 1:
            print("Please enter exactly one character.")
        elif not raw.isalpha():
            print("Letters only - no numbers or symbols.")
        elif raw in guessed:
            print("You already guessed '%s'. Try another letter." % raw)
        else:
            return raw


def choose_difficulty(default_lives):
    """Difficulty menu shown before each level."""
    print("\nChoose your difficulty:")
    for i, (name, lives, blurb) in enumerate(DIFFICULTIES, start=1):
        print("  %d) %-8s %d lives - %s" % (i, name, lives, blurb))
    print("  c) custom (1-%d)" % MAX_LIVES)
    print("  Enter = keep %d lives" % default_lives)

    while True:
        answer = input("Your choice: ").strip().lower()
        if answer == "":
            return default_lives
        if answer == "c":
            value = input("How many wrong guesses (1-%d)? " % MAX_LIVES).strip()
            if value.isdigit() and 1 <= int(value) <= MAX_LIVES:
                return int(value)
            print("Please enter a number between 1 and %d." % MAX_LIVES)
            continue
        if answer.isdigit() and 1 <= int(answer) <= len(DIFFICULTIES):
            return DIFFICULTIES[int(answer) - 1][1]
        print("Please pick one of the options above.")


# ----------------------------------------------------------- 4. play_level
def play_level(index, lives):
    """Play one level. Returns (won, points)."""
    secret, category = LEVELS[index]
    guessed = set()
    wrong = 0
    hints_left = max_hints(secret)

    print("\n" + "=" * 40)
    print("LEVEL %d of %d  -  %s  -  %d letters" % (index + 1, TOTAL_LEVELS, category, len(secret)))
    print("=" * 40)
    print(picture_clue(category))  # picture clue is shown from the start

    while True:
        # The gallows drawing scales to the number of lives you chose.
        print(HANGMAN_PICS[int(round(wrong * 6.0 / lives))])
        print("Word: ", display_word(secret, guessed))
        print("Guessed letters:", " ".join(sorted(guessed)) or "(none)")
        print("Attempts remaining: %d | Hints left: %d" % (lives - wrong, hints_left))

        guess = get_guess(guessed, hints_left, secret, category)

        if guess == "clue":
            print(picture_clue(category))
            continue
        if guess == "hint":
            letter = give_hint(secret, guessed)
            if letter:
                hints_left -= 1
                guessed.add(letter)
        else:
            guessed.add(guess)
            if guess in secret:
                print("Good guess! '%s' is in the word." % guess)
            else:
                wrong += 1
                print("Sorry, '%s' is not in the word." % guess)

        if all(letter in guessed for letter in secret):
            points = 10 + max(0, MAX_LIVES - lives) * 2  # fewer lives = bigger bonus
            print("\nThe word was: %s" % secret.upper())
            print("You Win! (+%d points)" % points)
            return True, points

        if wrong >= lives:
            print(HANGMAN_PICS[6])
            print("\nGame Over! The word was: %s (+0 points)" % secret.upper())
            return False, 0


# ------------------------------------------------------------------ 5. main
def load_progress():
    """Read the saved level and score, if any."""
    try:
        with open(SAVE_FILE) as fh:
            data = json.load(fh)
        level = min(max(int(data.get("level", 0)), 0), TOTAL_LEVELS - 1)
        lives = min(max(int(data.get("lives", MAX_LIVES)), 1), MAX_LIVES)
        return level, int(data.get("score", 0)), lives
    except Exception:
        return 0, 0, MAX_LIVES


def save_progress(level, score, lives):
    """Store progress so the next session continues where you stopped."""
    try:
        with open(SAVE_FILE, "w") as fh:
            json.dump({"level": level, "score": score, "lives": lives}, fh)
    except Exception:
        pass  # saving is a nicety, never break the game over it


def ask_yes_no(question):
    while True:
        answer = input(question).strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please answer with 'y' or 'n'.")


def main():
    print("=" * 40)
    print("        WELCOME TO HANGMAN QUEST")
    print("     %d levels, easy to hard" % TOTAL_LEVELS)
    print("=" * 40)

    level, score, lives = load_progress()
    if level > 0 and ask_yes_no("Continue from level %d (score %d)? (y/n): " % (level + 1, score)):
        pass
    else:
        level, score = 0, 0

    while level < TOTAL_LEVELS:
        lives = choose_difficulty(lives)
        won, points = play_level(level, lives)
        score += points
        print("Total score: %d" % score)

        if won:
            level += 1
            save_progress(level, score, lives)
            if level >= TOTAL_LEVELS:
                break
            print("\nNext level starting automatically...")
            continue

        save_progress(level, score, lives)
        if not ask_yes_no("Try level %d again? (y/n): " % (level + 1)):
            if ask_yes_no("Skip to the next level? (y/n): "):
                level += 1
            else:
                break

    if level >= TOTAL_LEVELS:
        print("\nIncredible - you finished all %d levels!" % TOTAL_LEVELS)
    print("\nThanks for playing! Final score: %d" % score)


if __name__ == "__main__":
    main()
