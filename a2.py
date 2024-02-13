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
    print("You are now in admin mode: Refer to the README for instructions.")

    usr_input = input()
    # parsed_input = parse_inputs(usr_input)
    parsed_input = parse_input_general(usr_input)
    print(f"Most general: {parsed_input}")





    command_input = parsed_input[0] # str

    while command_input != "Q":

        directory_input = parsed_input[1] 
        # subs = parsed_input[2]
        # extra = parsed_input[3]

        tup_list = parsed_input[2]
        directory_path = Path(directory_input)

        if command_input == "L":
            # print(command_L(directory_path, subs, extra))
            print(command_L_new(directory_path, tup_list))
        # elif command_input == "C":
        #     print(command_C_admin(directory_path, subs, extra))
        # elif command_input == "D":
        #     command_D(directory_path)
        # elif command_input == "R":
        #     print(command_R(directory_path))

        usr_input = input()
        # parsed_input = parse_inputs(usr_input)
        parsed_input = parse_input_general(usr_input)
        command_input = parsed_input[0]
    return "Q"
    

def user():
    # refactor code into list of tuples

    usr_input = print_user_options() # beginning options

    parsed_user_input = parse_inputs(usr_input)
    if usr_input == "admin":
        command_input = admin()
    else:
        command_input = parsed_user_input[0]


    user_profile = Profile(username=None, password=None)
    profile_loaded = False


    while command_input != "Q":
        if command_input == "C":
            directory_input = parsed_user_input[1] 
            directory_input = Path(directory_input)
            subs, extra = parsed_user_input[2:] # may be wrong
            command_c = command_C(directory_input, subs, extra)
            user_profile.username = command_c[1]
            user_profile.password = command_c[2]
            user_profile.bio = command_c[3]
            profile_loaded = True # potential error(s)
            # C /Users/alexra/Documents/UCI_WINTER_2023/ICS_32/test_folder -n myjournal1

            # profile is created -> edit or print
            nested_usr_input = print_user_options_2() 
            n_parsed_input = parse_inputs(nested_usr_input)
            command_input = n_parsed_input[0]

            if command_input == "E": # edit information once DSU file opened
                # remove the directory form input only leave part with subs and sub inputs

                # C /Users/alexra/Documents/UCI_WINTER_2023/ICS_32/test_folder -n myjournal
                # O /Users/alexra/Documents/UCI_WINTER_2023/ICS_32/test_folder/myjournal.dsu
                # E -usr Reese -pwd thisisnewpassword
                # print(command_input, directory_input, subs, extra)

                tup_list = n_parsed_input[2]
                print(f"This is parsed: {n_parsed_input}")
                if profile_loaded:
                    directory_input = str(directory_input)
                    directory_input += "/"+extra +".dsu"
                    print(f"This is directory: {directory_input}")
                    directory_input = Path(directory_input)

        
                    editDSU(tup_list, directory_input, user_profile)
                else:
                    print("There is no profile loaded, please run C or O command.")

            
            elif command_input == "P":
                # print requested contents
                tup_list = n_parsed_input[2]
                if profile_loaded:
                    print(command_P(tup_list, user_profile))
                else:
                    print("There is no profile loaded, please run C or O command.")

        elif command_input == "O": # other route, if loaded
            try:
                directory_input = parsed_user_input[1]
                directory_input = Path(directory_input)
                user_profile = loadDSU(directory_input)
                profile_loaded = True
            except:
                print("Something went wrong. Profile not loaded.")


            # profile is loaded -> edit or print

            usr_input = print_user_options_2()
            n_parsed_input = parse_inputs(usr_input)
            command_input = n_parsed_input[0]
            if command_input == "E": # edit information once DSU file opened
                # remove the directory form input only leave part with subs and sub inputs

                # C /Users/alexra/Documents/UCI_WINTER_2023/ICS_32/test_folder -n myjournal
                # O /Users/alexra/Documents/UCI_WINTER_2023/ICS_32/test_folder/myjournal.dsu
                # E -usr Reese -pwd thisisnewpassword
                # print(command_input, directory_input, subs, extra)
                tup_list = n_parsed_input[2]
                if profile_loaded:
                    editDSU(tup_list, directory_input, user_profile)
                else:
                    print("There is no profile loaded, please run C or O command.")
            elif command_input == "P":
                # print requested contents
                tup_list = n_parsed_input[2]
                if profile_loaded:
                    print(command_P(tup_list, user_profile))
                else:
                    print("There is no profile loaded, please run C or O command.")

        usr_input = print_user_options() # beginning options
        parsed_user_input = parse_inputs(usr_input)
    
        if usr_input == "admin":
            command_input = admin()
        else:
            command_input = parsed_user_input[0]

        user_profile = Profile(username=None, password=None)
        profile_loaded = False
        # C /Users/alexra/Documents/UCI_WINTER_2023/ICS_32/test_folder -n myjournal

def main():
    # did not have time to implement the multiple commands input
    user()


    # print("Enter 'admin' or 'user'.\n")
    # usr_input = input().lower()

    # if usr_input == "admin":
    #     admin() # run admin command
    # elif usr_input == "user":
    #     user()
    #     # run other command
        

if __name__ == "__main__":
    main()
