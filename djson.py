#!/usr/bin/env python3
# coding: utf-8

import sys
import json
from time import gmtime, strftime
from os.path import exists
import os
import ast

found = 0
colors = []
std_filename = "./data.json"
options = ["help", "find", "add", "create", "key", "show", "delete", "edit", "editkey", "url"]
message = {"invalid": "Invalid arguments",
           "missing": "Missing arguments, type -help for more information",
           "ops": "Ops something went wrong",
           "notfound": "File {} not found",
           "exists": "File {} already exists!",
           "replace": "Would you like to replace, Y/N? ",
           "delete": "Would you like to delete key {}, Y/N? ",
           "save": "Save changes in key {}, Y/N? ",
           "deleteok": "Key {} deleted!",
           "nochange": "Aborted! Nothing was changed",
           "abort": "Data creation aborted",
           "success": "Successfully saved!"}


def display_help():
    print("\nusage: data -command [filename optional]\n")
    print("commands:\n")
    print("-h   |  -help        display these options")
    print("-a   |  -add         use to add new content into a json file")
    print("-f   |  -find        use to find a content in a json file")
    print("-s   |  -show        use to display all entries")
    print("-k   |  -key         use to find a content from its key in a json file")
    print("-e   |  -edit        use to edit a content from its key in a json file")
    print("-ek  |  -edit key    use to edit a key name if is not as auto increment schema")
    print("-d   |  -delete      use to delete a content from its key in a json file")
    print("-c   |  -create      use to create a new json schema and save in new file")
    print("-o   |  -open        use to open a url from a key, important attribute must be named 'site', 'website' or 'url'")
    print("%                    use the symbol % to substitute spaces in your query")
    print("")
    print("attribute names:\n")
    print("description")
    print("desc")
    print("observation")
    print("obs                  use these names for attribute to add a multi-line entry")
    print("url, site, website   use these names for attribute to add a link entry")
    print("")
    print("ATTENTION!           if no filename is described after options, the standard file name will be used\n"
          "                     standard filename 'data.json' will be created if doesn't exist\n")

def open_url(query, filename):
    if exists(filename):
        with open(filename, "r") as arquivo:
            data = json.loads(arquivo.read())
            if not search_key(data, query):
                print(Color.RED + "No results found for {} in {}".format(query, filename) + Color.END)
            else:
                print("-" * 17)
                print(Color.GREEN + "Found {} results".format(found) + Color.END)
                print("-" * 17)

                labels = ast.literal_eval(data["0"]["labels"])
                found_url = False
                for item in labels :
                    if item.lower() == "url" or \
                            item.lower() == "website" or \
                            item.lower() == "site":
                        found_url = True
                        url = data[query][item]
                        if os.name == 'posix' :
                            os.system("open " + str(url))
                        elif os.name == 'nt' :
                            os.system("start " + str(url))
                if not found_url:
                    print("Attribute URL not found, type -help to see more information")
    else:
        print(Color.RED + message["notfound"].format(filename) + Color.END)

def generate_colors(display):
    global colors
    colors = ["\x1b[0m"]
    for style in range(8):
        for fg in range(30, 38):
            s1 = ""
            for bg in range(40, 49):
                form = ';'.join([str(style), str(fg), str(bg)])
                colors.append("\x1b[" + str(style) + ";" + str(fg) + ";" + str(bg) + "m")
                s1 += "\x1b[%sm %s \x1b[0m" % (form, form)
    if display:
        c = 0
        for i in range(0, len(colors)):
            if (i % 9) == 0:
                print("")
            print(str(colors[i]) + "  {:04d}{}  ".format(c, str(colors[i])) + str(colors[0]), end="")
            c += 1


generate_colors(False)


class Color:
    PURPLE = colors[54]
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


def show(mdict, key):
    auto = mdict["0"]["auto"] == "True"
    global colors
    print("-"*17)
    if auto:
        print(Color.BOLD + "Entry code: " + Color.PURPLE + "#{:02d}".format(int(key)) + Color.END)
    else:
        print(Color.BOLD + "Entry code: " + Color.PURPLE + "{}".format(key) + Color.END)
    print("-"*17)

    for inner_key in mdict[key]:
        if len(mdict[key][inner_key]) == 0:
            print("{}{}: {}".format(Color.BOLD + inner_key.capitalize() + Color.END, "."*(7-len(inner_key)),
                                    Color.RED+"null"+Color.END))
        else:
            print("{}{}: {}".format(Color.BOLD + inner_key.capitalize() + Color.END, "."*(7-len(inner_key)),
                                    Color.DARKCYAN + mdict[key][inner_key] + Color.END))


def isJsonFile(jsonfilename):
    with open(jsonfilename, "r") as arquivo:
        try:
            json.load(arquivo)
            return True
        except ValueError:
            return False


def search(mdict, search_for):
    global found
    for key in mdict:
        for inner_key in mdict[key]:
            if search_for.upper() in mdict[key][inner_key].upper():
                found += 1
                show(mdict, key)
                break
    if found > 0:
        return True
    else:
        return False


def search_key(mdict, chave):
    global found
    mdict_keys = set(key.upper() for key in mdict)
    #if chave.upper() in mdict_keys:
    for key in mdict_keys:
        if chave.upper() in key:
            found += 1
            show(mdict, key.upper())
    if found > 0:
        return True
    else:
        return False


def find(query, filename):
    if exists(filename):
        if isJsonFile(filename):
            with open(filename, "r") as arquivo:
                if not search(json.loads(arquivo.read()), query):
                    print(Color.RED + "No results found for {} in {}".format(query, filename) + Color.END)
                else:
                    print("-" * 17)
                    print(Color.GREEN + "Found {} results".format(found) + Color.END)
                    print("-" * 17)
        else:
            print(Color.RED + "File {} not regonized".format(filename) + Color.END)
    else:
        print(Color.RED + message["notfound"].format(filename) + Color.END)


def find_key(query, filename):
    if exists(filename):
        if isJsonFile(filename):
            with open(filename, "r") as arquivo:
                if not search_key(json.loads(arquivo.read()), query):
                    print(Color.RED + "No results found for {} in {}".format(query, filename) + Color.END)
                else:
                    print("-" * 17)
                    print(Color.GREEN + "Found {} results".format(found) + Color.END)
                    print("-" * 17)
        else:
            print(Color.RED + "File {} not regonized".format(filename) + Color.END)
    else:
        print(Color.RED + message["notfound"].format(filename) + Color.END)


def edit_key_name(key, filename):
    if key != "0":
        if exists(filename):
            if isJsonFile(filename):
                with open(filename, "r") as arquivo:
                    if not search_key(json.loads(arquivo.read()), key):
                        print(Color.RED + "No results found for {} in {}".format(key, filename) + Color.END)
                    else:
                        print("-" * 17)
                        # Read last data saved
                        with open(filename, "r", encoding="utf-8") as arquivo:
                            data = json.loads(arquivo.read())

                        # ************* GET NEW KEY NAME ************* #
                        insert = True
                        while insert:
                            cd = input("Enter new key name: ")
                            if cd != "0" and cd != 0 and cd.replace(" ", "") != "":
                                if str(cd).upper() in data:
                                    show(data, cd)
                                    insert = input("Entry already exists, do you want to replace? Y/N ").upper() != "Y"
                                else:
                                    insert = False
                            else:
                                print("Invalid entry, try another key")
                        print("-" * 17)
                        # ************* CONFIRM CHANGES ************* #
                        if input(Color.YELLOW + message["save"].format(key) + Color.END).upper() == "Y":
                            auto = data["0"]["auto"] == "True"
                            if auto:
                                key = "{:02d}".format(int(key))
                                cd = "{:02d}".format(int(cd))
                            new_data = data[str(key)]
                            data.pop("{}".format(key))
                            data["{}".format(str(cd).upper())] = new_data
                            # Convert string into json object with indent
                            entry_json = json.dumps(data, indent=4, ensure_ascii=False)
                            # Save new data and close
                            with open(filename, "w", encoding="utf-8") as arquivo:
                                arquivo.write(entry_json)
                            print(message['success'].format(cd))
                        else:
                            print(message['nochange'])
                        print("-" * 17)
            else:
                print(Color.RED + "File {} not regonized".format(filename) + Color.END)
        else:
            print(Color.RED + message["notfound"].format(filename) + Color.END)
    else:
        print(Color.RED + message["invalid"].format(filename) + Color.END)


def edit_key(query, filename):
    if query != "0":
        if exists(filename):
            if isJsonFile(filename):
                with open(filename, "r") as arquivo:
                    if not search_key(json.loads(arquivo.read()), query):
                        print(Color.RED + "No results found for {} in {}".format(query, filename) + Color.END)
                    else:
                        print("-" * 17)
                        # ************* GET NEW VALUES ************* #
                        # Read last data saved
                        with open(filename, "r", encoding="utf-8") as arquivo :
                            data = json.loads(arquivo.read())

                        data_value = {}
                        labels = ast.literal_eval(data["0"]["labels"])
                        for item in labels :
                            # OPTION FOR MULTI-LINE LABEL
                            if item.lower() == "desc" or \
                                    item.lower() == "description" or \
                                    item.lower() == "observation" or \
                                    item.lower() == "obs" :
                                user_writing = []
                                print("{}: ".format(item).capitalize(), end="")
                                while True :
                                    line = input()
                                    if not line :
                                        break
                                    else :
                                        user_writing.append(line)
                                data_value[item] = '\n'.join(user_writing)
                            else :
                                data_value[item] = input("{}: ".format(item).capitalize())
                        data_value["date"] = "{}".format(strftime("%Y-%m-%d at %H:%M", gmtime()))
                        data[query] = data_value

                        # Register last update
                        data["0"]["updated"] = "{}".format(strftime("%Y-%m-%d at %H:%M", gmtime()))

                        # ************* CONFIRM CHANGES ************* #
                        if input(Color.YELLOW + message["save"].format(query) + Color.END).upper() == "Y":
                            old_content = {}
                            with open(filename, "r") as arquivo:
                                old_content = json.loads(arquivo.read())

                            # CHANGE ONLY NOT EMPTY ENTRIES
                            for item in labels:
                                if len(data[query][item]) == 0:
                                    # skip empty entry
                                    data[query][item] = old_content[query][item]

                            # Convert string into json object with indent
                            entry_json = json.dumps(data, indent=4, ensure_ascii=False)
                            
                            # Save new data and close
                            with open(filename, "w", encoding="utf-8") as arquivo :
                                arquivo.write(entry_json)
                            print(message['success'].format(query))
                        else:
                            print(message['nochange'])
                        print("-" * 17)
            else:
                print(Color.RED + "File {} not regonized".format(filename) + Color.END)
        else:
            print(Color.RED + message["notfound"].format(filename) + Color.END)
    else:
        print(Color.RED + message["invalid"].format(filename) + Color.END)


def delete_key(query, filename):
    if query != "0":
        if exists(filename):
            if isJsonFile(filename):
                with open(filename, "r") as arquivo:
                    if not search_key(json.loads(arquivo.read()), query):
                        print(Color.RED + "No results found for {} in {}".format(query, filename) + Color.END)
                    else:
                        print("-" * 17)
                        if input(Color.RED + message["delete"].format(query) + Color.END).upper() == "Y":
                            content = {}
                            with open(filename, "r") as arquivo:
                                content = json.loads(arquivo.read())
                            # delete query
                            content.pop(query)
                            # Convert string into json object with indent
                            entry_json = json.dumps(content, indent=4, ensure_ascii=False)
                            # Save new data and close
                            with open(filename, "w", encoding="utf-8") as arquivo:
                                arquivo.write(entry_json)
                            print(message['deleteok'].format(query))
                        else:
                            print(message['nochange'])
                        print("-" * 17)
            else:
                print(Color.RED + "File {} not regonized".format(filename) + Color.END)
        else:
            print(Color.RED + message["notfound"].format(filename) + Color.END)
    else:
        print(Color.RED + message["invalid"].format(filename) + Color.END)


def add(filename):
    # If filename doesn't exist it creates a empty one
    if not exists(filename):
        print("We didn't find a file with a dictionary, we must first create a schema")
        create(filename)

    if isJsonFile(filename):
        welcome = "Let's save some data at {}".format(filename)
        print(welcome)
        print("-" * len(welcome))

        # Read last data saved
        with open(filename, "r", encoding="utf-8") as arquivo:
            data = json.loads(arquivo.read())

        # Get last entry id and sum to generate an auto increment id
        auto = data["0"]["auto"] == "True"
        if auto:
            try:
                cd = int(sorted(data.keys())[-1]) + 1
            except:
                cd = 1
            print("Key: #{:02d}".format(cd))
        else:
            insert = True
            while insert:
                cd = input("Enter key value: ")
                if cd != "0" and cd != 0 and cd != "" :
                    if cd in data :
                        show(data, cd)
                        insert = input("Entry already exists, do you want to replace? Y/N ").upper() != "Y"
                    else :
                        insert = False
                else :
                    print("Invalid entry, try another key")
        data_value = {}
        labels = ast.literal_eval(data["0"]["labels"])
        for item in labels:
            # OPTION FOR MULTI-LINE LABEL
            if item.lower() == "desc" or \
            item.lower() == "description" or \
            item.lower() == "observation" or \
            item.lower() == "obs":
                user_writing = []
                print("{}: ".format(item).capitalize(), end="")
                while True :
                    line = input()
                    if not line:
                        break
                    else :
                        user_writing.append(line)
                data_value[item] = '\n'.join(user_writing)
            else:
                data_value[item] = input("{}: ".format(item).capitalize())
        data_value["date"] = "{}".format(strftime("%Y-%m-%d at %H:%M", gmtime()))
        if auto:
            data["{:02d}".format(cd)] = data_value
        else:
            data[str(cd).upper()] = data_value

        # Register last update
        data["0"]["updated"] = "{}".format(strftime("%Y-%m-%d at %H:%M", gmtime()))

        # Convert string into json object with indent
        entry_json = json.dumps(data, indent=4, ensure_ascii=False)

        # Save new data and close
        with open(filename, "w", encoding="utf-8") as arquivo:
            arquivo.write(entry_json)

        print(message["success"])
    else:
        print(Color.RED + "File {} not regonized".format(filename) + Color.END)


def check_create(filename):
    if exists(filename):
        print(Color.YELLOW + message["exists"].format(filename) + Color.END)
        if input(Color.RED + message["replace"] + Color.END).upper() == "Y":
            return True
        else:
            return False
    else:
        return True


def create(filename):
    if check_create(filename):
        op_dictionary = int(input("Type of dictionary:\n"
                                  "[1] -> Auto increment dictionary (Duplicate data will be saved)\n"
                                  "[2] -> Dictionary ordered by a string key (Duplicate data will be over written)\n"))
        if op_dictionary == 1:
            auto = True
        else:
            auto = False

        data_create = {"0": {}}
        print("Now let's create some labels for your dictionary\nTo finish leave label empty and press [Enter]")
        insert = True
        labels = []
        while insert:
            labels.append(input("Label nº{}: ".format(len(labels)+1)).lower())
            insert = not labels[-1] == ""
        labels.pop(-1)
        with open(filename, "w", encoding="utf-8") as arquivo:
            data_create["0"]["filename"] = "{}".format(filename)
            data_create["0"]["created"] = "{}".format(strftime("%Y-%m-%d at %H:%M", gmtime()))
            data_create["0"]["auto"] = "{}".format(auto)
            data_create["0"]["labels"] = "{}".format(labels)
            arquivo.write(json.dumps(data_create, indent=4))

        print("Total labels added {}".format(len(labels)))
        if auto:
            print("1:  {")
            for item in labels:
                print("    {}".format(item))
            print("    }")
        else:
            print("key:  {")
            for item in labels:
                print("    {}:".format(item).capitalize())
            print("    }")
        print(message["success"])
    else:
        print(message["abort"])


# Check for arguments passed
def check_args():
    if len(sys.argv) > 1:
        if sys.argv[1].upper() == "-H" or sys.argv[1].upper() == "-HELP" or sys.argv[1].upper() == "HELP":
            return [options[0], True]
        elif sys.argv[1].upper() == "-F" or sys.argv[1].upper() == "-FIND" or sys.argv[1].upper() == "FIND":
            if len(sys.argv) > 2:
                return [options[1], sys.argv]
            else:
                return [False, False]
        elif sys.argv[1].upper() == "-S" or sys.argv[1].upper() == "-SHOW" or sys.argv[1].upper() == "SHOW":
            if len(sys.argv) > 1:
                return [options[5], sys.argv]
            else:
                return [True, False]
        elif sys.argv[1].upper() == "-K" or sys.argv[1].upper() == "-KEY" or sys.argv[1].upper() == "KEY":
            if len(sys.argv) > 2:
                return [options[4], sys.argv]
            else:
                return [False, False]
        elif sys.argv[1].upper() == "-O" or sys.argv[1].upper() == "-OPEN" or sys.argv[1].upper() == "OPEN":
            if len(sys.argv) > 2:
                return [options[9], sys.argv]
            else:
                return [False, False]
        elif sys.argv[1].upper() == "-E" or sys.argv[1].upper() == "-EDIT" or sys.argv[1].upper() == "EDIT":
            if len(sys.argv) > 2:
                return [options[7], sys.argv]
            else:
                return [False, False]
        elif sys.argv[1].upper() == "-EK" or sys.argv[1].upper() == "-EDITKEY" or sys.argv[1].upper() == "EDITKEY":
            if len(sys.argv) > 2:
                return [options[8], sys.argv]
            else:
                return [False, False]
        elif sys.argv[1].upper() == "-D" or sys.argv[1].upper() == "-DELETE" or sys.argv[1].upper() == "DELETE":
            if len(sys.argv) > 2:
                return [options[6], sys.argv]
            else:
                return [False, False]
        elif sys.argv[1].upper() == "-A" or sys.argv[1].upper() == "-ADD" or sys.argv[1].upper() == "ADD":
            return [options[2], sys.argv]
        elif sys.argv[1].upper() == "-C" or sys.argv[1].upper() == "-CREATE" or sys.argv[1].upper() == "CREATE":
            return [options[3], sys.argv]
        else:
            return [True, False]
    else:
        return [False, False]


# Start procedures
def start(args):
    if args[0] and args[1]:
        # ******************** HELP ******************** #
        if args[0] == options[0]:
            display_help()
        # ******************** FIND ******************** #
        elif args[0] == options[1]:
            if len(args[1]) > 3:
                # Use a specific filename described
                filename = args[1][3]
            else:
                # Use standard filename
                filename = std_filename
            # Execute query
            query = args[1][2].replace("%", " ")
            find(query, filename)
        # ******************** SHOW ALL ******************** #
        elif args[0] == options[5]:
            if len(args[1]) > 2:
                # Use a specific filename described
                filename = args[1][2]
            else:
                # Use standard filename
                filename = std_filename
            # Execute query
            find("", filename)
        # ******************** FIND KEY ******************** #
        elif args[0] == options[4]:
            if len(args[1]) > 3:
                # Use a specific filename described
                filename = args[1][3]
            else:
                # Use standard filename
                filename = std_filename
            # Execute query
            query = args[1][2].replace("%", " ")
            find_key(query, filename)
        # ******************** OPEN ******************** #
        elif args[0] == options[9]:
            if len(args[1]) > 3:
                # Use a specific filename described
                filename = args[1][3]
            else:
                # Use standard filename
                filename = std_filename
            # Execute query
            query = args[1][2].replace("%", " ")
            open_url(query, filename)
        # ******************** EDIT ******************** #
        elif args[0] == options[7]:
            if len(args[1]) > 3:
                # Use a specific filename described
                filename = args[1][3]
            else:
                # Use standard filename
                filename = std_filename
            # Execute query
            query = args[1][2].replace("%", " ")
            edit_key(query, filename)
        # ******************** EDIT KEY NAME ******************** #
        elif args[0] == options[8]:
            if len(args[1]) > 3:
                # Use a specific filename described
                filename = args[1][3]
            else:
                # Use standard filename
                filename = std_filename
            # Execute query
            query = args[1][2].replace("%", " ").upper()
            edit_key_name(query, filename)
        # ******************** DELETE ******************** #
        elif args[0] == options[6]:
            if len(args[1]) > 3:
                # Use a specific filename described
                filename = args[1][3]
            else:
                # Use standard filename
                filename = std_filename
            # Execute query
            query = args[1][2].replace("%", " ").upper()
            delete_key(query, filename)
        # ******************** ADD ******************** #
        elif args[0] == options[2]:
            if len(args[1]) > 2:
                # Use a specific filename described
                filename = args[1][2]
            else:
                # Use standard filename
                filename = std_filename
            # Add new data to a json file
            add(filename)
        # ******************** CREATE ******************** #
        elif args[0] == options[3]:
            if len(args[1]) > 2:
                # Use a specific filename described
                filename = args[1][2]
            else:
                # Use standard filename
                filename = std_filename
            # Add new data to a json file
            create(filename)
        # ******************** END ******************** #
    elif args[0] and not args[1]:
        # Error 1
        print(message["invalid"])
    else:
        # Error 2
        print(message["missing"])


start(check_args())
