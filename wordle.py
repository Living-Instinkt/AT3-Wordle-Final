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
debug_test_case = 3
debug_user_guess = "tests"
debug_target_word = "tests"


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


# TODO: Read File Into Word List Function
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
    if debug_state and debug_test_case != 0:
        return ""

    return input("\nGuess a word: ").strip().lower()

def user_word_matches_target(user_guess: str, target_word: str) -> bool:
    return False

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
def debug_mode(state: bool,
               test_case: int = 0,
               user_guess: str = None,
               target_word: str = None):
    """Debugs game functions
    Arguments:
    ---------
    :param(bool) state: True if debug mode is on, False otherwise
    :param(int) test_case: test case number (default: 0)
    :param(str) user_guess: user guess string (default: None)
    :param(str) target_word: target word string (default: None)"""

    # If game debug_state setting is set to 'True'
    if state:

        match test_case:
            case 0:

                # Check if user guess is None or empty
                if user_guess is None or not user_guess:
                    user_guess = get_user_guess()

                # Check is user guess is None or empty
                if target_word is None or not target_word:
                    target_word = random.choice(read_words_into_list(all_words_path))

                # Checks if the user guess doesn't contain numbers, same length as word of the day and is in all_words.txt
                if is_user_guess_valid(user_guess, target_word):
                    print(f"Guess:  {user_guess}\nTarget: {target_word}")
                    print(str(score_guess(user_guess, target_word)))
                else:
                    debug_mode(True, test_case, user_guess, target_word)

            case 1:
                # Assignment test case 1
                user_guess = "world"
                target_word = "train"
                score = score_guess(user_guess, target_word)
                print(f"\nUser Word: {user_guess}          | Target Word: {target_word}")
                print(f"Score: {score}    | Expected: {[0] * len(target_word)}")
            case 2:
                # Assignment test case 2
                user_guess = "hello"
                target_word = "hello"
                score = score_guess(user_guess, target_word)
                print(f"\nUser Word: {user_guess}          | Target Word: {target_word}")
                print(f"Score: {score}    | Expected: {[2] * len(target_word)}")
            case 3:
                # Assignment test case 3
                user_guess = "world"
                target_word = "hello"
                score = score_guess(user_guess, target_word)
                print(f"\nUser Word: {user_guess}          | Target Word: {target_word}")
                print(f"Score: {score}    | Expected: {[0,1,0,2,0]}")


#TODO: Main Program
def main():
    debug_mode(debug_state, debug_test_case, debug_user_guess, debug_target_word)


if __name__ == "__main__":
    main()
