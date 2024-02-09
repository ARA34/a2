# a2.py

# Starter code for assignment 2 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Alex Reyes Aranda
# areyesar@uci.edu
# STUDENT ID

# TODO:
# implement admin mode - still kinda iffy idk how they want us to integrate this...
# Stylecheck Profile.py
# Finish editDSU function
# refactor the admin function to include the new type of parsed inputs

from pathlib import Path
from ui import *


def admin():

    usr_input = input()
    command_input, directory_input, subs, extra = parse_input_general(usr_input)
    directory_input = Path(directory_input)

    while command_input != "Q":
        if len(usr_input) == 1:
            print("ERROR")
        directory_path = Path(directory_input)
        if command_input == "L":
            print(command_L(directory_path, subs, extra))
        elif command_input == "C":
            print(command_C_admin(directory_path, subs, extra))
        elif command_input == "D":
            command_D(directory_path)
        elif command_input == "R":
            print(command_R(directory_path))

        usr_input = input()
        command_input, directory_input, subs, extra = parse_input_general(usr_input)
    

def user():
    # refactor code into list of tuples
    usr_input = input()
    parsed_user_input = parse_inputs(usr_input)
    command_input = parsed_user_input[0]
    directory_input = parsed_user_input[1] 

    directory_input = Path(directory_input)
    user_profile = Profile(username=None, password=None)
    profile_loaded = False


    while command_input != "Q":
        if len(usr_input) == 1:
            print("ERROR")
        elif command_input == "C":
            subs, extra = parsed_user_input[2:] # may be wrong
            command_c = command_C(directory_input, subs, extra)
            user_profile.username = command_c[1]
            user_profile.password = command_c[2]
            user_profile.bio = command_c[3]
            profile_loaded = True # potential error(s)
            print(command_input, directory_input, subs, extra)
            # C /Users/alexra/Documents/UCI_WINTER_2023/ICS_32/test_folder -n myjournal1
        elif command_input == "O":
            try:
                user_profile = loadDSU(directory_input)
                profile_loaded = True
            except:
                print("Something went wrong. Profile not loaded.")
                return

        elif command_input == "E": # edit information once DSU file opened
            # remove the directory form input only leave part with subs and sub inputs

            # O /Users/alexra/Documents/UCI_WINTER_2023/ICS_32/test_folder/myjournal.dsu
            # E /Users/alexra/Documents/UCI_WINTER_2023/ICS_32/test_folder/myjournal.dsu -usr Reese -pwd thisisnewpassword
            # print(command_input, directory_input, subs, extra)
            tup_list = parsed_user_input[2]
            if profile_loaded:
                editDSU(tup_list, user_profile)
            else:
                print("There is no profile loaded, please run C or O command.")
                return

        usr_input = input()
        parsed_user_input = parse_inputs(usr_input)
        command_input = parsed_user_input[0]
        directory_input = parsed_user_input[1] 
        # C /Users/alexra/Documents/UCI_WINTER_2023/ICS_32/test_folder -n myjournal

def main():
    # did not have time to implement the multiple commands input
    print("Enter 'admin' or 'user'.\n")
    usr_input = input().lower()

    if usr_input == "admin":
        admin() # run admin command
    elif usr_input == "user":
        user()
        # run other command
        

if __name__ == "__main__":
    main()
