# Lists to contain the coded words(this is the list the user will be modifying), clues(clues file), pairings(user entered) and decoded words
words_list = []
clues_list = []
pairings_list = []
solved_list = []

# List of symbols used in the coded words (Not including the clues given)
symbols = "0123456789!\"$&)-+:',./)"

# List of all the symbols used in the coded words (Including the clues given)
all_symbols = "0123456789!\"$%&*)-+:'#,./)"

"""
Function load_file

This function takes no arguments. First, the function accesses the global variables,
words_list, clues_list and solved_list, the word 'global' is used so that the
contents of the variables can be used by other functions. Next, I use the open
function to open the three files I need to open so that I can access the contents
of the files, then the .read() function is used to read the files as a string, I
then use .splitlines() to turn the string into a list where each elemetn is a new
line. Lastly I close the files.
"""
def load_files():
    # Declare that I'm using global variables to the content is stored globally
    global words_list
    global clues_list
    global solved_list

    # Open the files so I can use them
    file_words = open("words.txt")
    file_clues = open("clues.txt")
    file_solved = open("solved.txt")

    # Read files, split them by new line into a list, then store in global variable
    words_list = file_words.read().splitlines()
    clues_list = file_clues.read().splitlines()
    solved_list = file_solved.read().splitlines()

    # Close the files as I no longer need to use them
    file_words.close()
    file_clues.close()
    file_solved.close()

# Call the load_file function to load the files
load_files()

"""
Function aplpy_substitutions

This function substitutes the symbol pairings into the words_list. First, I use a
for loop to loop through the indexes of the words_list. Next I loop through the
pairings in the pairings_list, I then reassign the value of words_list[index]
(index is the word the loop is currently at) to its self, with the substitutions
made. This is done by using replace(). This replaces any occurrences of pairing[1]
with pairing[0], pairing[1] is the symbol and pairing[0] is the letter, this is
because the pairings are stored as letter:symbol.
"""
def apply_substitutions():
    # All pairings (default clues and user entered pairs)
    all_pairings = clues_list + pairings_list
    
    # Loop through the indexes of the words in the words_list
    for index in range(0, len(words_list)):    
        # Loop through each pairing in the pairings_list
        for pairing in all_pairings:
            # Reassign the element at the index with it's self with the replacements made
            words_list[index] = words_list[index].replace(pairing[1], pairing[0])

"""
Function add_pairing

This function handles the sections of code to do with adding a pairing to the list.
This function uses inputs to get user input from the user, i.e what symbol they
want to replace and with what letter. For loops are used to look through the
pairings_list to make sure the symbol or letter they have selected hasn't already
been paired. The function will return True if a pairing was added or it will
return False if no pairing was added.
"""
def add_pairing():
    # Access global pairings_list
    global pairings_list

    # Create two local variables to hold whether or not a symbol or letter exists
    symbol_exists = False
    letter_exists = False

    # All pairings (default clues and user entered pairs)
    all_pairings = clues_list + pairings_list
    
    # Ask the user what symbol they want to replace
    symbol = input("\nWhat symbol do you want to replace?\n> ")

    # Make sure the symbol entered is actually a symbol from the coded words
    while symbol == "" or len(symbol) > 1 or symbol not in symbols:
        symbol = input("Please enter a valid symbol! " + symbols)

    # Loop through the pairings list
    for pairing in all_pairings:
        # Check if the symbol entered is already paired
        if symbol == pairing[1]:
            symbol_exists = True
            
            # Tell the user symbol is already paired and tell them to return to menu
            print("\nYou have already paired this symbol with a letter!")
            option_continue = input("Press enter to return to the menu.")

            # Return False to exit the function and return to the main menu
            return False

    # The symbol is not already paired
    if symbol_exists == False:
        # Ask the user what letter they want to match with the symbol
        letter = input("What letter do you think symbol " + symbol + " represents?\n> ").upper()

        # Make sure the letter entered is a valid input and an actual letter
        while letter == "" or len(letter) > 1 or letter.isalpha() == False:
            letter = input("Please enter a valid letter!").upper()

        # Loop through the pairings_list
        for pairing in all_pairings:
            # Check if the letter entered is already paired
            if letter == pairing[0]:
                letter_exists = True

                # Tell the user letter is already paired and tell them to return to menu
                print("\nYou have already paired this letter with a symbol!")
                option_continue = input("Press enter to return to the menu.")

                # Return False to exit the function and return to the main menu
                return False
        
        # Else the letter isn't already paired
        if letter_exists == False:
            # Ask the user to confirm they want to add the pairing
            confirm = input("Are you sure you want to add the pairing " + letter + "=" + symbol + "? (Y/N)\n> ").upper()

            # Check the option selected at the menu is a valid option
            while confirm == "" or confirm not in "YN":
                confirm = input("Please enter a valid option! (Y/N)").upper()

            if confirm == "Y":
                # Yes was selected so concatenate the letter and symbol strings together and append to pairings_list
                pairings_list.append(letter + symbol)
                # Return True to exit function and return to menu
                return True
            elif confirm == "N":
                # No was selected, tell user and prompt to press enter to return to menu
                input("You have decided not to enter the pairing. Press enter to return to the menu.")
                return False

"""
Function delete_pairing

This function handles the deletion of pairings. The function first prints a list
of pairings to the user, presenting them as a numbered list. To do this I have
used a for loop and printed the index + 1 and then the pairing. I have done + 1
as list starts counting from 0 but I want my list to start from 1 so I have added
1 to this to do this. I then use the input function to ask for the pairing they
want to delete and store that in a variable. I then check to make sure they entered
a valid option. After this I asked the user to confirm the deletion. If they entered
Y then I use a reverse version of the apply substitutions function to substitute the
letters with the symbols (to revert the words list to how it was before the pairing
was added). I then use pairings_list.remove to remove the pairing from the list,
finally  a message is printed to the user to tell them they have deleted the pairing.
If N was entered, tell them they decided to not delete the pairing.
"""
def delete_pairing():
    # If the length of the pairings list is less than 1 (so 0) tell the user there are no pairings to be deleted
    if len(pairings_list) < 1:
        print("\nThere are no pairings to delete!")
        input("Press enter to return to the menu.")

        # Return False to exit this function
        return False
    
    # Print each pairing from the pairings_list
    print("\n\n\n-------------------- Pairings --------------------")
    for index in range(0, len(pairings_list)):
        print(str(index + 1) + ") " + pairings_list[index])

    # Ask the user to enter the number of the pairing they want to delete
    pairing_number = input("\nEnter the number of the pairing you want to delete\n> ")

    # Make sure the symbol entered is actually a symbol from the coded words
    while pairing_number == "" or pairing_number not in str([x + 1 for x in range(0, len(pairings_list))]):
        pairing_number = input("Please enter a valid option!")

    # Ask the user to confirm they want to delete the pairing
    confirm = input("\nAre you sure you want to delete the pairing " + pairings_list[index] + "? (Y/N)\n> ").upper()

    # Check the option selected at the menu is a valid option
    while confirm == "" or confirm not in "YN":
        confirm = input("Please enter a valid option!")

    # Create a variable which is the pairing it self to be removed, - 1 because lists start from 0, not 1 list the selection list
    pairing = pairings_list[int(pairing_number) - 1]

    if confirm == "Y":
        print("\n" * 20 + "--------------------------------------------------")
        # If Y, then loop through the indexes of the words in the words_list
        for i in range(0, len(words_list)):            
            # Reassign the element at the index with it's self with the replacements made
            words_list[i] = words_list[i].replace(pairing[0], pairing[1])

        # Remove the pairing from the pairings_list
        pairings_list.remove(pairing)

        # Print a message telling them they have deleted the pairing
        print("You have deleted the pairing " + pairing + ".")
        input("Press enter to return to the menu.")   
    elif confirm == "N":
        # If N, tell user they have decided to not enter pairing and press enter to return to menu
        print("You have decided not to delete the pairing " + pairing + ".")
        input("Press enter to return to the menu.")

"""
Function calculate_frequency

This function calculates the frequency of the remaining symbols in the coded words. First
a words_string is corrected which is the words_list in string format. Next two empty
lists are created to hold the frequency information and one for the nicely formatted
one. Next the function loops through each symbol in all_symbols and then checks if
the symbol is NOT in the frequency_raw list, if it isn't then add the frequency to
the frequency_raw list. To count the occurrences of the symbol I have used .count() to
count all the occurrences of the current symbol being looked at. Next some nice formatting
is applied and stored in frequency_table. Lastly the function returns the frequency_table
with some large spaces to make the table look nicely spaced.
"""
def calculate_frequency():
    # The words_list as a string
    words_string = "".join(words_list)

    # A list which will have the raw frequencies in them
    frequency_raw = []

    # A list which will have the nicely formatted table in it
    frequency_table = []

    # Loop through each symbol in the all_symbols list
    for symbol in all_symbols:
        # See if the symbol is not already in the frequency_raw list
        if symbol not in frequency_raw:
            # If it isn't already in the list, add it to the list
            frequency_raw.append("[" + symbol + ":" + str(words_string.count(symbol)) + "]")

    # Loop through the indexes in the frequency_raw list
    for index in range(0, len(frequency_raw)):
        # If we are index 0 then add a heading to the frequency table
        if index == 0:
            frequency_table.append("                Symbol:Frequency")
        # If the index divided by 5 is 0 then add a new line so only 5 frequencies are displayed per row
        if index % 5 == 0:
            frequency_table.append("\n")
        # Else add the frequency to the frequeny_table list
        else:
            frequency_table.append(frequency_raw[index])

    # Return the frequency table with a large space between the frequency brackets
    return "      ".join(frequency_table)

    print("\n" * 20 + "--------------------------------------------------")

"""
The main while loop.

This loop will always run as the condition set to run until is 'True' and True will always be equal
to true so will always end, the while loop will only end if the exit() command is called which
terminates the program. The while loop continually loops the substitution of pairings, the
displaying of of the words, clues, pairings and frequencies. It will also display the menu every
time the end of the loop is reached. This also handles the input from the user and calls the
necessary functions depending on what was selected.
"""
while True:
    # Call apply_substitutions
    apply_substitutions()

    # Print each word in the words_list
    print("------------ Words with substitutions ------------")
    for word in words_list:
        print(word)

    # Print each clue (already provided to user) pairing from the clues_list
    print("--------------------- Clues ----------------------")
    for clue in clues_list:
        print(clue)

    # Print each pairing (that the user has entered) from the pairings_list
    print("-------------------- Pairings --------------------")
    for pairing in pairings_list:
        print(pairing)

    # Print frequency of symbol occurrences
    print("------------------- Frequency --------------------")
    print(calculate_frequency())
    
    # Print a dashed line to make the spacing look nicer
    print("--------------------------------------------------\n")
    
    # Ask user what they want to do by presenting a menu
    option = input("What would you like to do?\n1) Add a pairing\n2) Delete a pairing\n3) Quit AQA Code Puzzle\n> ")

    # Check the option selected at the menu is a valid option
    while option == "" or option not in "123":
        option = input("Please enter a valid input! (1, 2 and 3)")

    if option == "1":
        # Option 1 was selected which is the add pairing option so call the add_pairing function
        return_status = add_pairing()

        # If return status is True, check the words_list with solved_list to see if they have completed the puzzle
        if return_status == True:
            # Apply substitutions to apply the pairing they just added
            apply_substitutions()

            # Check if words_list is the same as solved_list
            if words_list == solved_list:
                # If it is, display 20 new lines and a then "You Won!" message
                print("\n" * 20 + "--------------------------------------------------")
                print("You have cracked the puzzle!\n")
                print("--------------------------------------------------")

                # Ask the user what they would like to do now, play again or quit
                option = input("What would you like to do?\n1) Play Again\n2) Quit")

                # Check the option selected at the menu is a valid option
                while option == "" or option not in "12":
                    option = input("Please enter a valid input! (1 or 2)")

                # If they selected one, load the files again to reset the lists and then reset the pairings list by setting it to an empty list, then print 20 new lines
                if option == "1":
                    load_files()
                    pairings_list = []
                    print("\n" * 20)

                # If they selected two, then display a thank you message and then exit the program
                if option == "2":
                    input("Thank you for playing AQA Code Puzzle. Press enter to exit.")
                    exit()
            else:
                # Else the lists don't match so print a Not Solved message
                print("\n" * 10 + "----------------- Not Solved Yet -----------------" + "\n" * 5)
    elif option == "2":
        # Call the delete pairing function as number 2 was selected at the menu
        delete_pairing()
    elif option == "3":
        # Display a than you message to the user and then tell them to press enter to exit the game
        input("Thank you for playing AQA Code Puzzle! Press enter to exit.")
        exit()
