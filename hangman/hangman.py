# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string
import sys

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    with open(WORDLIST_FILENAME, 'r') as f:
        line = f.readline()         # line: string
    wordlist = line.split()     # wordlist: list of strings
    print(len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
WORDLIST = load_words()


def is_word_guessed(secret_word, letters_guessed):
    """
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    """
    for c in secret_word:
        if c not in letters_guessed:
            return False
    return True


def get_guessed_word(secret_word, letters_guessed):
    """
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    """
    guessed_word = ''
    for c in secret_word:
        if c in letters_guessed:
            guessed_word += c
        else:
            guessed_word += '_ '
    return guessed_word


def get_available_letters(letters_guessed):
    """
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    """
    available_letters = ''
    for c in string.ascii_lowercase:
        if c not in letters_guessed:
            available_letters += c
    return available_letters


def len_unique_letters(word):
    """ Returns the number of unique letters in 'word'."""
    unique_word = ''
    for c in word:
        if c not in unique_word:
            unique_word += c
    return len(unique_word)


def is_letter_valid(letter, letters_guessed):
    """Returns True if letter is a lowercase alphabet character, False otherwise."""
    return letter.isalpha() and letter.lower() not in letters_guessed


def match_with_gaps(my_word, other_word):
    """
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the
    corresponding letters of other_word, or the letter is the special symbol
    _ , and my_word and other_word are of the same length. False otherwise.
    """
    my_word = my_word.replace(' ', '') # remove all whitespace characters

    if len(my_word) != len(other_word):
        return False

    word_len = len(my_word)
    for i in range(word_len):
        if (my_word[i] != other_word[i]) and (my_word[i] != '_' or other_word[i] in my_word):
            return False
    return True


def show_possible_matches(my_word):
    """
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.
    """
    matches = []
    for word in WORDLIST:
        if match_with_gaps(my_word, word):
            matches.append(word)

    if not matches:
        return 'No matches found'
    return ' '.join(matches)


def hangman_with_hints(secret_word):
    """
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    Follows the other limitations detailed in the problem write-up.
    """
    print('Welcome to the game Hangman!')
    print('I am thinking of a word that is', len(secret_word), 'letters long.')

    guesses_remaining = 6
    warnings_remaining = 3
    letters_guessed = []

    print('You have', warnings_remaining, 'warnings left.')

    while not is_word_guessed(secret_word, letters_guessed) and guesses_remaining > 0:
        print('-' * 20)
        print('You have', guesses_remaining, 'guesses left.')
        print('Available letters:', get_available_letters(letters_guessed))
        letter = input('Please guess a letter: ')

        if letter == '*':
            print('Possible word matches are:')
            print(show_possible_matches(get_guessed_word(secret_word, letters_guessed)))
        elif is_letter_valid(letter, letters_guessed):
            letters_guessed.append(letter.lower())

            if letter in secret_word:
                print('Good guess:', get_guessed_word(secret_word, letters_guessed))
            else:
                print('Oops! That letter is not in my word:',
                      get_guessed_word(secret_word, letters_guessed))
                guesses_remaining -= 2 if letter in 'aeiou' else 1
        else:
            if not letter.isalpha(): # is a valid letter?
                print('Oops! That is not a valid letter.')
            elif letter.lower() in letters_guessed: # has the letter already been guessed?
                print('Oops! You\'ve already guessed that letter.')

            if warnings_remaining > 0:
                warnings_remaining -= 1
                print('You have', warnings_remaining, 'warnings left:',
                      get_guessed_word(secret_word, letters_guessed))
            else:
                print('You have no warnings left so you lose one guess:',
                      get_guessed_word(secret_word, letters_guessed))
                warnings_remaining = 3
                guesses_remaining -= 1

    print('-' * 20)
    if guesses_remaining > 0:
        total_score = guesses_remaining * len_unique_letters(secret_word)
        print('Congratulations, you won!')
        print('Your total score for this game is:', total_score)
    else:
        print('Sorry, you ran out of guesses. The word was', secret_word)


if __name__ == "__main__":
    try:
        secret_word = choose_word(WORDLIST)
        hangman_with_hints(secret_word)
    except KeyboardInterrupt:
        pass
    sys.exit(0)
