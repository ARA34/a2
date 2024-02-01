# ui.py

# Starter code for assignment 2 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Alex Reyes Aranda
# areyesar@uci.edu
# STUDENT ID

from pathlib import Path
def parse_input(input:str):
    # L dir -r (3)
    # L dir (2)
    # C dir -n something (4) dir dir2 something 
    # L dir -r -e dsu (5)
    # L dir -r -f
    input_list = []

    command_letter = ""
    dir_input = ""

    allowed_subs = ["-r","-f","-s","-e","-n"]

    # command letter
    command_letter = input[0]

    remaining_str = input[2:]
    remaining_lst = remaining_str.split() # a list of subsections without the first letter

    subs = list(filter(lambda s: s in allowed_subs, remaining_lst))


    for i in range(len(remaining_lst)):
        try:
            check = remaining_lst[i] + " " + remaining_lst[i+1]
            if Path(check).exists():
                dir_input = check
                remaining_lst.remove(remaining_lst[i+1])
                remaining_lst.remove(remaining_lst[i])
            elif remaining_lst[i] in subs:
                remaining_lst.remove(remaining_lst[i])
            else:
                dir_input = remaining_lst[0]
                remaining_lst.remove(dir_input)
        except:
            for sub in remaining_lst:
                if sub in subs:
                    remaining_lst.remove(sub)

    remain = "".join(remaining_lst)
    if Path(remain).exists() and dir_input == "": # last edge case 
        dir_input = remain
        remain = ""
        
    # finalize
    input_list.append(command_letter)
    input_list.append(dir_input)
    input_list.append(subs)
    input_list.append(remain)      

    return input_list


        
