# ui.py

# Starter code for assignment 2 in ICS 32 Programming with Software Libraries in Python

# Alex Reyes Aranda
# areyesar@uci.edu
# STUDENT ID

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
    # input: diectory, list of sub commands, extra input
    # output: string of paths
    output = []
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


def command_C_admin(directory: Path, subs, filename):
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

# INPUT PARSING FUNCTIONS

def parse_input_general(o_input:str):
    # input: String o_input
    # output: List tuples matching sub with sub input

    # O dir -usr Reese -pwd 4321
    # C dir -n myjournal
    
    # Walkthrough:
    # input: -usr Reese R -pwd 4321
    # usr, Reese R, pwd, 4321
    # usrReeseRpwd4321
    # usr, Reese, R pwd 4321
    # _, Reese R, _ 4321
    # _ 
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

        subs = list(map(lambda d: d[0], tup_list)) # working
        extra_input = list(map(lambda s: s[1], tup_list))
        extra_input = list(filter(lambda s: s != "", extra_input))[0]
        parsed_list = [parsing_list[0], parsing_list[1], subs, extra_input]

    elif True in in_allowed_o:
        parsed_list = parse_input_general(user_input)
    else:
        parsed_list = parse_input_general(user_input)[:-1]
        pass # do whatever else
    return parsed_list


def loadDSU(dsu_path: Path):
    profile_to_load = Profile(dsu_path)
    profile_to_load.load_profile(dsu_path)
    print("DSU file loaded.")
    print(profile_to_load.username, profile_to_load.password, profile_to_load.bio)
    return profile_to_load
    

def save_note(note: str, p: Path):
    # check if storage file exists, if not create it.
    
    # open and write user note to file
    f = p.open('a')
    f.write(note + '\n')
    f.close()


def edit_by_command(tup:tuple, userprofile: Profile):
    # load the saved information onto a list
    # assume the file is loaded
    # input: One tuple at a time
    sub = tup[0]
    new = tup[1]
    if sub == "-usr":
        # edit the username part of the loaded list
        userprofile.username = new
        print("username edited to: ", new)
    elif sub == "-pwd":
        # edit the password part of the loaded list
        userprofile.password = new
        print("password edited to: ", new)
    elif sub == "-bio":
        # edit the bio part of the loaded list
        userprofile.bio = new
        print("bio edited to: ", new)
    elif sub == "-addpost":
        # add a post to dsu file
        post = Post(new)
        userprofile.add_post(post)
        # userprofile.add_post()
        pass
    elif sub == "-delpost": 
        # deete a file from dsu file based on index
        try:
            index = int(new)
            userprofile.del_post(index)
        except:
            print("Delete post not completed.")
            pass


def editDSU(tup_list: list, DSU_path: Path, userprofile: Profile):
    # can editDSU only if the file is loaded by C or O command -> i.e the file exists
    # either one command at a time or multiple
    for tup in tup_list:
        # run the edit command
        edit_by_command(tup, userprofile)
    userprofile.save_profile(DSU_path)
    print("Username: ", userprofile.username, " Password: ", userprofile.password," Bio: ", userprofile.bio, " Posts: ", userprofile._posts)
    

    # input: Path DSU
    # output: Str message of updated things

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
        output += str(userprofile.get_posts()[sub_input].get_entry()) + "\n"
    elif sub == "-posts":
        for i in range(len(userprofile.get_posts())):
            output += str(i) + ": " + str(userprofile.get_posts()[i].get_entry()) + "\n"
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
