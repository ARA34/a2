# a2.py

# Starter code for assignment 2 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Alex Reyes Aranda
# areyesar@uci.edu
# STUDENT ID

# TODO:
# implement admin mode - still kinda iffy idk how they want us to integrate this...
# 

from pathlib import Path
from ui import *


def admin():

    usr_input = input()
    command_input, directory_input, subs, extra = parse_input(usr_input)

    while command_input != "Q":
        if len(usr_input) == 1:
            print("ERROR")
        directory_path = Path(directory_input)
        if command_input == "L":
            print(command_L(directory_path, subs, extra))
        elif command_input == "C":
            print(command_C(directory_path, subs, extra))
        elif command_input == "D":
            command_D(directory_path)
        elif command_input == "R":
            print(command_R(directory_path))

        usr_input = input()
        command_input, directory_input, subs, extra = parse_input(usr_input)
    

def user():
    pass

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
