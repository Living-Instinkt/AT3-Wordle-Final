# JPL_ICTPRG302_Project_2025_S2
#
# Author: Josh Plank
# Student ID: 20154551
#
# Course Cert IV: Programming
# Lecturer: Para O'Kelly
import ast
import datetime
import os
import random
import statistics
import sys

# Name: Josh Plank | Student Number: 20154551 | Date: 17/11/25
# Variables and Constants
# -------------------------------
# -------=| File Paths |=--------
# -------------------------------
all_words_path = "all_words.txt"
target_words_path = "target_words.txt"
stats_path = "stats.txt"
game_history_path = "game_history.txt"

# -------------------------------
# --------=| Settings |=---------
# -------------------------------
# Hidden word length (allows for different difficulty games in a further expansion)
word_length = 5
game_attempts = 6

# -------------------------------
# -------=| Formatting |=--------
# -------------------------------
# Horizontal rules
xxl_hr = "─" * 112 + "\n"
sm_hr = "\n " + "─" * 60 + "\n"
correct_symbol = "X"
wrong_symbol = "-"
wrongly_placed_symbol = "?"

# -------------------------------
# -------=| Debugging |=---------
# -------------------------------
# debug_state - Allowing us to manually turn on/off debugging
# debug_test_case - Run test cases easily (default: 0 | Guess: Will ask you to input a word | Target: Will pick a random word from target_words.txt)
# debug_user_guess - Hard coded User guess word
# debug_target_word - Hard coded target word
# debug_file_path - File path for word lists
# debug_number_of_guesses - sets the debug amount of guesses; used for looping through the game 'x' amounts of times
debug_state = False
debug_test_case = 12
debug_user_guess = ""
debug_target_word = None
debug_file_path = ""
debug_number_of_guesses = 5


# Name: Josh Plank | Student Number: 20154551 | Date: 17/11/25
# Application Functions
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

# ----------------------------------------
# ------------=| Prints |=----------------
# -----------------------------------------
def print_welcome_message():
    """Prints the welcome message to console"""

    print(f"{xxl_hr}"
          "|                                       Welcome to AT3 - Word-all 2.0!                                          |\n"
          "|                                              Hope you enjoy!                                                  |\n"
          "|                                             (Created by Josh)                                                 |\n"
          f"{xxl_hr}")

# Prints game instructions
def print_instructions():
    """Prints the game instructions to console"""

    print(f"{xxl_hr}"
          f"|                                                How to Play                                                    |\n"
          f"{xxl_hr}"
          "|    Each day we randomly select a word and you have to guess it!                                               |\n"
          "|    The randomly selected word is blanked out however still displays the correct amount of letters.            |\n"
          "|    You must type in a word that you think might be hidden.                                                    |\n"
          f"{xxl_hr}"
          f"|    If you guess the correct letter and it's in the correct position '{correct_symbol}' will be displayed under the letter.   |\n"
          f"|    If you guess a letter that is in the hidden word however in the wrong spot an '{wrongly_placed_symbol}' under the letter.        |\n"
          f"|    If you guess a letter that is not in the hidden word, a '{wrong_symbol}' will be displayed under the letter.            |\n"
          f"|    You must guess the word in {game_attempts} attempts.                                                                     |\n"
          f"{xxl_hr}"
          "|                                          * Good luck and have fun! *                                          |\n"
          "|                          (Type 'help' at any time to view these instructions again)                           |\n"
          f"{xxl_hr}")

# Asks user to input a word and cleans for capital letters and white spaces
def get_user_guess(target_word: str, cheat_mode: bool = False) -> str:
    """Gets the users input and cleans it

    Returns:
    -------
    :returns: The cleaned user input
    """

    if cheat_mode:
        input_str = f"({target_word}) Guess a word: "
    else:
        input_str = "Guess a word: "

    return input(input_str).strip().lower()

# Para okayed this at 2025-11-17 20:21
def random_target_word() -> str:
    return random.choice(read_words_into_list(target_words_path))

def display_score(score: list[int], user_guess: str):
    output_marks = []

    for letter in score:
        if letter == 0:
            output_marks.append(wrong_symbol)
        elif letter == 1:
            output_marks.append(wrongly_placed_symbol)
        elif letter == 2:
            output_marks.append(correct_symbol)

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

# Check if player has won, print congratulations if they have, give them misery if they lost
def player_has_won(win_condition: bool, attempts: int, users_guessed_words: list[str],  target: str, player_name: str):
    """Function called to check if a player has won
    Arguments:
    ---------
    :param win_condition: True if player has won, False otherwise
    :param attempts: Number of attempts to play
    :param users_guessed_words: List of words the player has guessed already
    :param target: The word of the day
    :param player_name: The players name"""

    # Dynamically space the end pipe of guessed words line depending on how many words in the sentence
    guessed_words_str = f"| Guessed words: {", ".join(users_guessed_words)}"
    if len(guessed_words_str) < 60:
        str_filler = " " * (61 - len(guessed_words_str))
        guessed_words_str = f"| Guessed words: {", ".join(users_guessed_words)}{str_filler}|"

    # If the player has won, print congratulations and close terminal.
    if win_condition:
        print(f"{sm_hr}"
              f"|                     Congratulations!                       |"
              f"{sm_hr}"
              f"|                You guessed the hidden word!                |\n"
              f"| Attempts: {attempts}/{game_attempts}                                              |\n"
              f"{guessed_words_str}"
              f"{sm_hr}")
        save_game_log(player_name, target, users_guessed_words, True)
        update_stat_file()
        sys.exit(0)

    # If the player runs out of attempts, print misery message and shame them. Close terminal.
    if attempts <= 0:
        print(f"{sm_hr}"
              f"|                   Boo! You lost! Shame!                    |"
              f"{sm_hr}"
              f"|                The hidden word was: {target}                  |\n"
              f"| Attempts: {attempts}/{game_attempts}                                              |\n"
              f"{guessed_words_str}"
              f"{sm_hr}")
        save_game_log(player_name, target, users_guessed_words, False)
        update_stat_file()
        sys.exit(0)

# Gets the players name and welcomes them
def get_players_name() -> str:
    """Function called to get the players name and welcomes them"""
    user_name = input("Please enter your name: ")

    if user_name.strip() == "":
        user_name = "Playa"

    print(f"Welcome, {user_name}\n")
    return user_name

# Asks the user if they need instructions or not and starts teh game
def prompt_instructions():
    """Function called to check if a player has required instructions and starts the game"""

    user_response = input("Do you need instructions on how to play? (y/n): ").lower().strip()

    if user_response not in ("y", "n"):
        print("Invalid input, please only enter 'y' or 'n'")
        prompt_instructions()

    if user_response == "y":
        print_instructions()

    if user_response == "n":
        print("\nVery well then, good luck!\n(Psst! You can type 'help' at any time to see the instructions.)")

# Please note: parameter only here as integrated into debug test case 9 (Defaulted to 'None' so without that test case affecting it will act as normal)
def play_game(target_word: str = None):

    print_welcome_message()

    # Get players name and say welcome to them
    player_name = get_players_name()

    # Ask player if they want instructions
    prompt_instructions()

    # Initialise game
    attempts = game_attempts
    users_guessed_words = []
    user_cheat_mode = False

    # Check if target word is set (debug test case 9)
    if not target_word:
        # Get random target word
        target_word = random_target_word()

    # Loop through number of attempts until attempts run out
    while attempts > 0:

        # Print attempt number
        print(f"\nGuess number: {attempts}/{game_attempts}")

        # Get the users guess
        user_guess = get_user_guess(target_word, user_cheat_mode)

        if user_guess == "help":
            print_instructions()
            continue

        if user_guess == "cheatmode":
            if user_cheat_mode:
                print("\nCheat mode deactivated!\n")
                user_cheat_mode = False
            else:
                print("\nCheat mode activated!\n")
                user_cheat_mode = True
            continue

        # Check if users guess is valid
        if is_user_guess_valid(user_guess, target_word):

            # Print the guess word with appropriate relating symbols
            display_score(score_guess(user_guess, target_word), user_guess)

            # Add the users guess to our guessed words list
            users_guessed_words.append(user_guess.capitalize())

            # Format the guessed words list into a string, each word separated by a comma
            guessed_words_str = ", ".join(users_guessed_words)

            if user_guess == target_word:
                player_has_won(True, attempts, users_guessed_words, target_word, player_name)
            else:
                # Reduce the guess attempt by 1
                attempts -= 1
                player_has_won(False, attempts, users_guessed_words, target_word, player_name)
                print(f"Your current guesses: {guessed_words_str}\n---------------------")

        # If not a valid word, continue loop; user_guess word error handling is done in is_user_guess_valid()
        else:
            continue

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
                    user_guess = get_user_guess(target_word)

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
            # Prints 5 random words
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
                    user_guess = get_user_guess(target_word)

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
                    print("\nNo anagrams found.")

            # Cheat mode! Displays the hidden word at the top of the console
            case 9:
                target_word = random_target_word()
                print(f"\n Target word: {target_word}\n")
                play_game(target_word)

            # Test case to further test debugging of statistics implementation
            case 10:
                target_word = random_target_word()
                guessed_words = ["steam", "steam", "steam", "steam"]
                save_game_log("1", target_word, guessed_words, True)
                update_stat_file()

            # Test case just to try break things (statistics implementation)
            case 11:
                print(f"{get_average_score([])}")
                read_game_history()

            # Test case to bypass all inputs using static variables (used for testing statistics implementation)
            case 12:
                player_has_won(True, 1, ["steam"], "steam", "Playa")

def get_average_score(user_guess_attempts: list[int]) -> float | None:
    """Takes in a list[int] of the total number of game attempts and
    returns the mean/average attempts or None if there is no data.

    Param:
         - user_guess_attempts (list[int]): List of past game attempts

    Return:
        - average attempts or None (float)
    """
    if user_guess_attempts:
        return statistics.mean(user_guess_attempts)

    return None


# https://www.geeksforgeeks.org/python/how-to-read-dictionary-from-file-in-python/
def read_game_history() -> dict | None:
    """Reads game history from 'game_history.txt' path and returns it as a dict.

    Return:
        dict | None: dictionary containing.
        - 'player_name' (str): name of the player
        - 'number_of_guesses' (int): number of guesses
        - 'number_of_games' (int): number of games
    """

    # Initialise variables
    player_names = []
    number_of_guesses = []
    number_of_games = 0

    # Try open 'game_history.txt' as read only
    try:
        with open(game_history_path, "r") as file:
            for line in file:

                # If the line starts with a '{', use eval to attempt to put data into a dictionary.
                if line.startswith("{"):
                    stat_dict = ast.literal_eval(line)

                    # Populate player_names and number_of_guesses lists
                    player_names.append(stat_dict["player_name"])
                    number_of_guesses.append(len(stat_dict["player_guesses"]))

                    # Increment number of games by 1
                    number_of_games += 1

            return {"player_names": player_names, "number_of_guesses": number_of_guesses, "number_of_games": number_of_games}

    except FileNotFoundError:
        print(f"Error: '{game_history_path}' not found")
        return None

    except Exception as e:
        print(f"Error: {e}")
        return None


def update_stat_file():
    """
    Update the stats file cherry-picking data from game_history.txt using read_game_history().
    """

    # Get the cherry-picked data from read_game_history()
    stats = read_game_history()

    # If 'stats' is populated, try writing stats to file.
    if stats:
        try:

            # Control for if we somehow end up with an empty 'avg_attempts'
            user_number_of_guesses = stats.get("number_of_guesses") or []
            avg_attempts = get_average_score(user_number_of_guesses)

            if avg_attempts is not None :
                avg_attempts_str = f"{avg_attempts:.2f}"
            else:
                avg_attempts_str = "N/A"

            # Write stats to file
            with open(stats_path, "w+") as file:
                heading = "------------=| Game Stats |=------------\n"
                file.write(
                    f"{heading}"
                    f"Player names: {'; '.join(stats.get('player_names'))}\n"
                    f"Number of Games: {str(stats.get('number_of_games'))}\n"
                    f"Average Attempts: {avg_attempts_str}"
                    )

        except Exception as e:
            print(f"Error: {e}")
    else:
        print("No stats found.")


def save_game_log(player_name: str, target_word: str, player_guesses:list[str], win_condition: bool = False):
    """
    Save game log to game_history.txt.

    Args:
        - player_name (str): name of the player
        - target_word (str): target word the user was trying to guess
        - player_guesses (list[str]): list of previously guessed words
        - win_condition (bool): if True, the game was won, False the player lost
    """

    # Get current time
    time = datetime.datetime.now()

    # Populate dictionary
    stat_dict = {
        "time_stamp": time.strftime("%I:%M:%S(%p) - %d/%m/%y"),
        "player_name": player_name,
        "target_word": target_word,
        "player_guesses": player_guesses,
        "win_condition": win_condition
    }

    try:
        with open(game_history_path, "a+") as file:

            # https://labex.io/tutorials/python-how-to-read-the-contents-of-a-python-file-and-check-if-it-is-empty-395093
            # Check if file is empty, if it is, append the header
            if os.path.getsize(game_history_path) == 0:
                file.write("------------=| Game History |=------------\n")

            # Append/write stat dictionary to file
            file.write(f"{stat_dict}\n")

    except Exception as e:
        print(e)

def main():
    if debug_state:
        debug_mode(debug_state, debug_test_case, debug_user_guess, debug_target_word, debug_file_path, debug_number_of_guesses)
    else:
        play_game()


if __name__ == "__main__":
    main()