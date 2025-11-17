# JPL_ICTPRG302_Project_2025_S2
#
# Author: Josh Plank
# Student ID: 20154551
#
# Course Cert IV: Programming
# Lecturer: Para O'Kelly

# TODO: Add Import statements (if needed)
import random

# Name: Josh Plank | Student Number: 20154551 | Date: 17/11/25
# Variables and Constants
# TODO: Define Constants
# -------------------------------
# -------=| File Paths |=--------
# -------------------------------
all_words_path = "all_words.txt"
target_words_path = "target_words.txt"

# -------------------------------
# --------=| Settings |=---------
# -------------------------------
# Hidden word length (allows for different difficulty games in a further expansion)
word_length = 5

# -------------------------------
# -------=| Debugging |=---------
# -------------------------------
# debug_state - Allowing us to manually turn on/off debugging
# debug_test_case - Run test cases easily (default: 0 | Guess: Will ask you to input a word | Target: Will pick a random word from target_words.txt)
# debug_user_guess - Hard coded User guess word
# debug_target_word - Hard coded target word
debug_state = True
debug_test_case = 8
debug_user_guess = ""
debug_target_word = None
debug_file_path = ""
debug_number_of_guesses = 5


# TODO: Define Variables

# Name: Josh Plank | Student Number: 20154551 | Date: 17/11/25
# Application Functions
# TODO: Score Guess Function
def score_guess(user_guess: str, target: str) -> list[int]:
    """
    Scores the state of the guess vs target word and returns a list of letter scores
    Arguments:
    ---------
    :param(str) user_guess: user guess string
    :param(str) target: target guess string

    Returns:
    -------
    :return(list[int]): list of letter scores: [0] letter not in word, [1] letter in word but wrong position, [2] letter in correct position

    Examples:
    --------
    score_guess("tests", "tests") - Returns: [2,2,2,2,2]
    score_guess("world", "hello") - Returns: [0,1,0,2,0]
    """

    # Initialise the output list with all 0's
    output = [0] * len(target)
    remaining_letters = []

    if user_guess == target:
        output = [2] * len(target)
        return output

    for letter in range(len(target)):
        if user_guess[letter] == target[letter]:
            output[letter] = 2
        # else if letters don't match, add remaining letters to a remaining_letters_list
        else:
            remaining_letters.append(target[letter])

    # Loop through target word again
    for letter in range(len(target)):

        # skip/continue over letters that are already in the right place ([2])
        if output[letter] == 2:
            continue

        # check if user_input letter is in remaining_letter_list
        if user_guess[letter] in remaining_letters:

            # Change output[letter] to [1] (in word but wrong place)
            output[letter] = 1

            # Remove letter from remaining_letter_list
            remaining_letters.remove(user_guess[letter])

    # Return
    return output

# Name: Josh Plank | Student Number: 20154551 | Date: 17/11/25
def read_words_into_list(file_path: str) -> list[str] | None:
    """Opens a file and reads each line into a list
    Arguments:
    ---------
    :param(str) file_path: path to file with words

    Returns:
    -------
    :return(list[str]): cleaned list of words matching game word_length setting"""

    # Try open given filepath and read lines
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()

            # Clean & verify words for whitespaces, capitals and ensure we only pick words from file path that match our given word length setting
            cleaned_word_list = [word.strip().lower() for word in lines if len(word.strip()) == word_length]

            if len(cleaned_word_list) == 0:
                print(f"Error: No {word_length}-letter words found in file.")
                return None

            # Return a cleaned list of verified words
            return cleaned_word_list

    # Print file not found error
    except FileNotFoundError:
        print(f"Error: {file_path} not found")
        return None

    # Print all other generic errors
    except Exception as error:
        print(f"Error: {error}")
        return None


# TODO: Display Greeting Function
def show_greeting():
    print("Welcome")


# TODO: Display Instructions Function
def show_instructions():
    print("Instructions")


# TODO: Any Optional Additional Functions
# Asks user to input a word and cleans for capital letters and white spaces
def get_user_guess() -> str:
    """Gets the users input and cleans it

    Returns:
    -------
    :returns: The cleaned user input
    """
    return input("Guess a word: ").strip().lower()

# Para okayed this at 2025-11-17 20:21
def random_target_word() -> str:
    return random.choice(read_words_into_list(target_words_path))

def display_score(score: list[int], user_guess: str):
    output_marks = []

    for letter in score:
        if letter == 0:
            output_marks.append("-")
        if letter == 1:
            output_marks.append("?")
        if letter == 2:
            output_marks.append("X")

    print(f"{" ".join(user_guess)}\n{" ".join(output_marks)}\n")

# Verifies if the users guess is valid, returns False if contains anything other than letters, is not in all_words.txt or incorrect length or True for everything else.
def is_user_guess_valid(user_input: str, word_of_the_day: str) -> bool:
    """Validates the users input.
    Arguments:
    ---------
    :param user_input: The user input
    :param word_of_the_day: The word of the day

    Returns:
    -------
    :return boolean: True if user input valid, False otherwise"""

    # If the users input is not the same length as the word of the day
    if len(user_input) != len(word_of_the_day):
        print(f"Error: Enter a {len(word_of_the_day)}-letter word")
        return False

    # If the user input contains anything other than letters
    if not user_input.isalpha():
        print("Error: Words must only contain letters.")
        return False

    # If the users guess is not in all_words.txt (Could probably just use this check and omit the other 2 checks above)
    if user_input not in read_words_into_list(all_words_path):
        print(f"Error: {user_input} is not in guessable words.")
        return False

    # Otherwise return True
    return True


# TODO: Play Game Function

#TODO: Testing Function
# Name: Josh Plank | Student Number: 20154551 | Date: 17/11/25
def debug_mode(state: bool,
               test_case: int = 0,
               user_guess: str = None,
               target_word: str = None,
               file_path: str = None,
               number_of_guesses: int = None):
    """Debugs game functions
    Arguments:
    ---------
    :param(bool) state: True if debug mode is on, False otherwise
    :param(int) test_case: test case number (default: 0)
    :param(str) user_guess: user guess string (default: None)
    :param(str) target_word: target word string (default: None)
    :param(str) file_path: path to file with words"""

    # If game debug_state setting is set to 'True'
    if state:

        match test_case:
            # Test case that allows static user_guess and target_word or dynamic; Single iteration
            case 0:

                # Check if user guess is None or empty
                if not user_guess:
                    user_guess = get_user_guess()

                # Check is user guess is None or empty
                if not target_word:
                    target_word = random.choice(read_words_into_list(all_words_path))

                # Checks if the user guess doesn't contain numbers, same length as word of the day and is in all_words.txt
                if is_user_guess_valid(user_guess, target_word):
                    print(f"Guess:  {user_guess}\nTarget: {target_word}")
                    print(str(score_guess(user_guess, target_word)))
                else:
                    debug_mode(True, test_case, user_guess, target_word)

            # Assessment test case 1
            case 1:
                user_guess = "world"
                target_word = "stack"
                score = score_guess(user_guess, target_word)
                print(f"\nUser Word: {user_guess}          | Target Word: {target_word}")
                print(f"Score: {score}    | Expected: {[0] * len(target_word)}")

            # Assessment test case 2
            case 2:
                user_guess = "hello"
                target_word = "hello"
                score = score_guess(user_guess, target_word)
                print(f"\nUser Word: {user_guess}          | Target Word: {target_word}")
                print(f"Score: {score}    | Expected: {[2] * len(target_word)}")

            # Assessment test case 3
            case 3:
                user_guess = "world"
                target_word = "hello"
                score = score_guess(user_guess, target_word)
                print(f"\nUser Word: {user_guess}          | Target Word: {target_word}")
                print(f"Score: {score}    | Expected: {[0,1,0,2,0]}")

            # Assessment debug test case 4
            case 4:
                print("\nFirst 5 words from all_words.txt")
                print(f"Found:    {read_words_into_list(all_words_path)[:5]}\nExpected: ['aahed', 'aalii', 'aargh', 'aarti', 'abaca']")

            # Assessment debug test case 5
            case 5:
                print("\nLast 5 words from target_words.txt")
                print(f"Found:    {read_words_into_list(target_words_path)[-5:]}\nExpected: ['young', 'youth', 'zebra', 'zesty', 'zonal']")
            case 6:
                for i in range(5):
                    print(random_target_word())

            # Runs through game play {number_of_guesses} amount of times; No win conditions
            case 7:

                # Check if target_word is None or empty; Gets a target word if it is
                if not target_word:
                    target_word = random_target_word()

                # If number of guesses not specified; Set number of guesses to 5
                if not number_of_guesses:
                    number_of_guesses = 5

                # Print the target word to assist with debugging
                print(target_word)

                # Sets number of attempts user has to guess the word
                attempts = number_of_guesses

                # Loop through number of attempts until attempts run out
                while attempts > 0:

                    # Print attempt number
                    print(f"\nGuess number: {attempts}/{number_of_guesses}")

                    # Get the users guess
                    user_guess = get_user_guess()

                    # Check if users guess is valid
                    if is_user_guess_valid(user_guess, target_word):

                        # Print target word with letter spacing
                        print(f"{" ".join(target_word)}")

                        # Print the guess word with appropriate relating symbols
                        display_score(score_guess(user_guess, target_word), user_guess)

                        # Reduce the guess attempt by 1
                        attempts -= 1

                    # If not a valid word, continue loop; user_guess word error handling is done in is_user_guess_valid()
                    else:
                        continue

            # Checks target_word for anagrams in all_words.txt; Runs all anagrams through display_score (Good for testing display_score functionality)
            case 8:

                # Check if target_word is None or empty; Gets a target word if it is
                if not target_word:
                    target_word = random_target_word()

                # Get all words from all_words.txt
                all_words = read_words_into_list(all_words_path)

                # Sort target_word
                sorted_target = sorted(target_word)

                # Find anagrams (same letters in any order); Exclude target_word
                anagrams = [word for word in all_words if sorted(word) == sorted_target and word != target_word]

                # If there are anagrams, loop through them all and test each one with display_score()
                if len(anagrams) > 0:
                    for anagram in anagrams:

                        # Print target word with letter spacing
                        print(f"{" ".join(target_word)}")

                        # Feed anagrams through display_score()
                        display_score(score_guess(anagram, target_word), anagram)
                else:
                    print("\nNo anagrams")

#TODO: Main Program
def main():
    debug_mode(debug_state, debug_test_case, debug_user_guess, debug_target_word, debug_file_path, debug_number_of_guesses)


if __name__ == "__main__":
    main()
