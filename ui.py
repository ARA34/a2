# ui.py

# Starter code for assignment 2 in ICS 32 Programming with Software Libraries in Python

# Alex Reyes Aranda
# areyesar@uci.edu
# 69754988

from pathlib import Path
from Profile import *


def recur_dir(directory: Path):
    # input: directory
    # output: list of paths
    paths = []
    for path in directory.iterdir():
        if path.is_file():
            paths.append(path)

    dirs = []
    for path in directory.iterdir():
        if path.is_dir():
            dirs.append(path)
    for path in dirs:
        paths.append(path)
        paths.extend(recur_dir(path))
    return paths 


def paths_to_strs(path_list:list):
    # input: list of paths
    # output: string of path directories
    output = ""
    for path in path_list:
        output += str(path) + "\n"

    return output.strip()


def command_L(directory: Path, subs: list, extra_input: str):
    # CURRENTLY NOT BEING USED [OLD]
    output = ""
    iter_paths = []

    allowed_ext = [".dsu", ".py",".txt"]
    for path in directory.iterdir():
        iter_paths.append(path)

    if len(subs) == 0 and extra_input == "":
        output = paths_to_strs(iter_paths)
    elif "-r" in subs:
        # it r time
        output = recur_dir(directory)
        if "-f" in subs:
            # r  + f
            output = list(filter(lambda p: p.is_file(), output))
            output = paths_to_strs(output)
        elif "-e" in subs:
            # r + e
            if "."+extra_input in allowed_ext:
                output = list(filter(lambda p: p.suffix == "." + extra_input, output))
                output = paths_to_strs(output)
            else:
                output = "ERROR"
        elif "-s" in subs:
            # r + s
            if extra_input != "":
                output = list(filter(lambda p: p.name == extra_input, output))
                output = paths_to_strs(output)
            else:
                output = "ERROR"
        else:
            output = paths_to_strs(output)
    elif "-f" in subs:
        # f
        if extra_input == "":
            output = list(filter(lambda p: p.is_file(), iter_paths))
            output = paths_to_strs(output)
        else:
            output = "ERROR"
    elif "-e" in subs:
        # e
        if "." + extra_input in allowed_ext:
            output = list(filter(lambda p: p.suffix == "." + extra_input, iter_paths))
            output = paths_to_strs(output)
        else:
            output = "ERROR"
    elif "-s" in subs:
        # s
        if extra_input != "":
            output = list(filter(lambda p: p.name == extra_input, iter_paths))
            output = paths_to_strs(output)
        else:
            output = "ERROR"
    else:
        output = "ERROR"
    return output


def command_L_new(directory:Path, list_tups:list):
    #output: string converted from list of paths
    output = []
    for tup in list_tups:
        output = small_L(tup, directory, output)

    return paths_to_strs(output)
    

def get_iter_paths(dir:Path) -> list:
    # input: Path directory
    # output: list of paths
    output = []
    for path in dir.iterdir():
        output.append(path)
    return output


def small_L(tup, dir:Path, p_list:list) -> list:
    # input: tup and directory_path
    # output: list of paths
    output = []
    # -r, -f, -e, -s
    sub = tup[0]
    new = tup[1]
    allowed_ext = [".dsu", ".py", ".txt"]

    if len(p_list) == 0:
        p_list = get_iter_paths(dir) 
        if sub == "-r":
            output = recur_dir(dir)
        elif sub == "":
            output = p_list
        elif sub == "-f":
            output = list(filter(lambda p: p.is_file(), p_list))
        elif sub == "-e":
            if "." + new in allowed_ext:
                output = list(filter(lambda p: p.suffix == "." + new, p_list))
            else:
                print("Not the right extension")
        elif sub == "-s":
            output = list(filter(lambda p: p.name == new, p_list))
        else:
            print("ERROR - First iteration")
    else:
        if sub == "-f":
            output = list(filter(lambda p: p.is_file(), p_list))
        elif sub == "-e":
            if "." + new in allowed_ext:
                output = list(filter(lambda p: p.suffix == "." + new, p_list))
            else:
                print("Not the right extension")
        elif sub == "-s":
            output = list(filter(lambda p: p.name == new, p_list))
        else:
            print("ERROR - Later iteration")
    return output


def command_C_admin(directory: Path, tup_list:list):
    subs = tup_list[0][0]
    filename = tup_list[0][1]
    output = ""
    if "-n" in subs:
        filename_dsu = filename + ".dsu"
        file = directory/filename_dsu
        file.touch()
        output = str(file)
    else:
        output = "ERROR"
    return output


def command_C(directory: Path, subs, filename):

    output = ""
    if "-n" in subs:
        filename_dsu = filename + ".dsu"
        file = directory/filename_dsu
        file.touch()
        output = str(file)

        username = input("Username: \n")
        userpass = input("Pasword: \n")
        userbio = input("Bio: \n")

        user = Profile(username=username,password=userpass) # missing dsuserver input
        user.bio = userbio
        user.save_profile(file) # takes the file directory as input
    else:
        output = "ERROR"
    return output, username, userpass, userbio


def command_D(file_dir: Path):
    if file_dir.exists() and file_dir.suffix == ".dsu":
        str_file = str(file_dir)
        file_dir.unlink()
        print(str_file + " DELETED")
    else:
        print("ERROR")


def command_R(file_dir: Path):
    contents = ""
    if file_dir.suffix != ".dsu":
        contents = "ERROR"
    elif len(file_dir.read_text()) != 0:
        contents = file_dir.read_text().strip()
    else:
        contents = "EMPTY"
    return contents


def parse_input_general(o_input:str):
    # input: String o_input
    # output: List tuples matching sub with sub input
    parsed_list = []
    command_letter = o_input[0]
    o_input = o_input[2:]
    dir_input = o_input.split("-")[0]
    dir_input = "".join(dir_input).strip()

    allowed_subs = ["-usr", "-pwd", "-bio", "-addpost", "-delpost", "-r","-f","-s","-e","-n", "-posts", "-post", "-all"]
    allowed_subs_stripped = list(map(lambda d: d[1:], allowed_subs)) # commands without "-"

    subs = list(filter(lambda i: i in allowed_subs, o_input.split())) # getting all the commands

    input_split = o_input.split("-")[1:]
    input_split = "".join(input_split).split()
    for i in range(len(input_split)):
        if input_split[i] in allowed_subs_stripped:
            input_split[i] = "_"

    input_split = " ".join(input_split)
    input_split = input_split.split("_")[1:]
    input_split = list(map(lambda d:d.strip(), input_split))

    tpl_list = list(map(lambda x,y: (x,y), subs, input_split))
    parsed_list = [command_letter, dir_input, tpl_list]
    return parsed_list


def parse_inputs(user_input:str):
    allowed_general = ["-r","-f","-s","-e","-n"]
    allowed_o = ["-usr", "-pwd", "-bio", "-addpost", "-delpost", "-posts", "-post", "-all"]

    in_general = list(map(lambda d: d in user_input, allowed_general))
    in_allowed_o = list(map(lambda d: d in user_input, allowed_o))
    parsed_list = [] # what to be returned
    
    if True in in_general:
        # converst to old format --> can be refactored but not enough time
        parsing_list = parse_input_general(user_input)
        tup_list = parsing_list[2]

        subs = list(map(lambda d: d[0], tup_list))
        try:
            extra_input = list(map(lambda s: s[1], tup_list))
            extra_input = list(filter(lambda s: s != "", extra_input))[0]
        except:
            extra_input = ""
        parsed_list = [parsing_list[0], parsing_list[1], subs, extra_input]

    elif True in in_allowed_o:
        parsed_list = parse_input_general(user_input)
    else:
        parsed_list = parse_input_general(user_input)[:-1]
    return parsed_list


def loadDSU(dsu_path: Path):
    profile_to_load = Profile(dsu_path)
    profile_to_load.load_profile(dsu_path)
    print("DSU file loaded.")
    print(profile_to_load.username, profile_to_load.password, profile_to_load.bio)
    return profile_to_load
    

def edit_by_command(tup:tuple, userprofile: Profile):
    # load the saved information onto a list
    # assume the file is loaded
    # input: One tuple at a time
    sub = tup[0]
    new = tup[1]
    if sub == "-usr":
        # edit the username part of the loaded list
        userprofile.username = new
        print("username edited to: ", new,"\n")
    elif sub == "-pwd":
        # edit the password part of the loaded list
        userprofile.password = new
        print("password edited to: ", new, "\n")
    elif sub == "-bio":
        # edit the bio part of the loaded list
        userprofile.bio = new
        print("bio edited to: ", new,"\n")
    elif sub == "-addpost":
        # add a post to dsu file
        post = Post(new)
        userprofile.add_post(post)
        # userprofile.add_post()
    elif sub == "-delpost": 
        # deete a file from dsu file based on index
        try:
            index = int(new)
            userprofile.del_post(index)
        except:
            print("Delete post not completed.")


def editDSU(tup_list: list, DSU_path: Path, userprofile: Profile):
    # can editDSU only if the file is loaded by C or O command -> i.e the file exists
    # either one command at a time or multiple
    for tup in tup_list:
        edit_by_command(tup, userprofile)
    userprofile.save_profile(DSU_path)
    print("Username: ", userprofile.username, " Password: ", userprofile.password," Bio: ", userprofile.bio, " Posts: ", userprofile._posts)


def get_user_info(tup: tuple, userprofile: Profile):
    output = ""
    sub = tup[0]
    try:
        sub_input = int(tup[1])
    except:
        pass

    all_commands = ["-usr", "-pwd", "-bio", "-posts"]

    if sub == "-usr":
        output += "Username: " + userprofile.username + "\n"
    elif sub == "-pwd":
        output += "Password " + userprofile.password + "\n"
    elif sub == "-bio":
        output += "Bio: " + userprofile.bio + "\n"
    elif sub == "-post":
        if len(userprofile.get_posts()) != 0:
            output += str(userprofile.get_posts()[sub_input].get_entry()) + "\n"
        else:
            output += "No Posts."
    elif sub == "-posts":
        if len(userprofile.get_posts()) != 0:
            for i in range(len(userprofile.get_posts())):
                output += str(i) + ": " + str(userprofile.get_posts()[i].get_entry()) + "\n"
        else:
            output += "No Posts."
    elif sub == "-all":
        for cmd in all_commands:
            output += get_user_info((cmd,""),userprofile)
    return output


def command_P(tup_list: list, userprofile: Profile):
    # input: String P + commands
    # output: string with requested information
    output = ""
    for tup in tup_list:
        output += get_user_info(tup, userprofile)
    return output


def print_user_options():
    # input: various strs
    # output: long str to parse
    output_str = ""
    cmd_letter = str(input("Welcome! Do you want to create or load a DSU file (type 'C' to create or 'O' to load): \n")) # can also enter admin
    output_str += cmd_letter + " "
    if cmd_letter.strip() == "admin":
       return "admin"
    elif cmd_letter == "C":
        dir_input = str(input("Great! What is the name of the directory you want to create in:\n"))
        output_str += dir_input + " "
        sub_input = input("Please enter '-n' in order to specify your filename:\n")
        output_str += sub_input + " "
        filename = input("What is the name of the file you would like to create:\n")
        output_str += filename

    elif cmd_letter == "O":
        dir_input = str(input("Great! What is the name of the file you want to load?\n"))
        output_str += dir_input + " "
    elif cmd_letter == "Q":
        output_str += "Q"
    else:
        print("invalid statement, please try again.")

    return output_str


def print_user_options_2():
    print("You have created or loaded a file!\n")
    output_str = ""
    cmd_letter = input("Do you want to edit or print contents of a file (type 'E' to edit or 'P' to print contents):\n")
    output_str += cmd_letter + " "
    sub_menu_inputs = ""
    if cmd_letter == "E":
        print_edit_cmds() # for editing
        sub_menu_inputs += take_sub_inputs()
    elif cmd_letter == "P":
        print_cmds() # for printing
        sub_menu_inputs += take_sub_inputs()

    output_str += sub_menu_inputs[:-1]
    return output_str


def take_sub_inputs():
    sub_menu_inputs = ""
    sub_input = input("Enter a sub input ('Q' for escape sub input menu):\n")
    while sub_input != "Q":
        sub_menu_inputs += sub_input + " "
        sub_menu_input = input("Addtional Input:")
        sub_menu_inputs += sub_menu_input + " "
        sub_input = input("Enter a sub input ('Q' for escape sub input menu):\n")
    return sub_menu_inputs


def print_edit_cmds():
    print("Now you will be entering edit commands and their respective inputs (for no input enter return):")
    print("'-usr' - Edit username.")
    print("'-pwd' - Edit password.")
    print("'-bio' - Edit bio.")
    print("'-addpost' - Add a post.")
    print("'-delpost' - Delete a post.")


def print_cmds():
    print("Now you will be entering print commands and their respective inputs (for no input enter return):")
    print("'-usr' - Print username.")
    print("'-pwd' - Print password.")
    print("'-bio' - Print bio.")
    print("'-post' - Print post based on ID.")
    print("'-posts' - Print all posts.")
    print("'-all' - Print all information.")

