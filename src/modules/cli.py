from modules.logger import logger
from rich import print as rprint
from rich.table import Table
from rich.columns import Columns
from rich.panel import Panel
import modules.chatgpt as chatgpt
import random
import re


def init_screen():
    rprint('''[bold green]
888888 Yb        dP 888888 888888 888888 Yb        dP 88 8888P    db    88""Yb 8888b.  
  88    Yb  db  dP  88__   88__     88    Yb  db  dP  88   dP    dPYb   88__dP  8I  Yb 
  88     YbdPYbdP   88""   88""     88     YbdPYbdP   88  dP    dP__Yb  88"Yb   8I  dY 
  88      YP  YP    888888 888888   88      YP  YP    88 d8888 dP""""Yb 88  Yb 8888Y"       
    [/bold green]''')

def options_table():
    options = [["0", "exit", "Exit program"],
        ["1", "info", "Show/Hide info"],
        ["2", "users", "Select users"],
        ["3", "login", "Log in of all selected users and logout of all unselected users with sessions opened"],
        ["4", "logout", "Log out all users"], 
        ["5", "like", "Like selected tweet"],
        ["6", "retweet", "Retweet selected tweet"],
        ["7", "like_rt", "Like and retweet selected tweet"],
        ["8", "comment", "Comment selected tweet"]]
        
    table = Table("ID", "Command", "Description")
    for option in options:
        table.add_row(option[0], option[1], option[2])
    rprint(table)

def executing_msg():
    rprint("[bold blue]Executing the selected option...[/bold blue]")

def exit_msg():
    rprint("[bold red]Exiting...[/bold red]")

def select_random_users(list_of_users):
    max_users = len(list_of_users)
    rprint(f"[bold blue]How many random users do you want to use? (Max: {max_users})[/bold blue]")

    num = input("Number: ")
    if not num.isdigit():
        rprint("[bold red]Error: You must enter a number.[/bold red]")
        return select_random_users(list_of_users)
    elif int(num) > max_users:
        rprint(f"[bold red]Error: The number of users you entered is greater than the number of users available. The maximum number of users available is {max_users}.[/bold red]")
        return select_random_users(list_of_users)
    elif int(num) < 1:
        rprint("[bold red]Error: You must enter a number greater than 0.[/bold red]")
        return select_random_users(list_of_users)
    print("You selected: " + str(num) + " random users")
    # Select N random users between 0 and max_users
    random_users = random.sample(range(0, max_users), int(num))
    selected_users = [list_of_users[i] for i in random_users]
    return selected_users

def select_users(list_of_users):
    rprint("[bold blue]List of users:[/bold blue]")
    table = Table("ID", "User")
    table.add_row("0", "Random users")
    for i in range(len(list_of_users)):
        table.add_row(str(i+1), list_of_users[i])
    rprint(table)
    rprint("[bold blue]Select the users to be used...[/bold blue]")
    rprint("[bold blue]Enter the ID of the users separated by commas. Example: 1,2,3. If you want to use random users, enter 0. [/bold blue]")
    users = input("Selection: ")

    # Check if the user entered more than one number
    if "," not in users:
        if not users.isdigit():
            rprint("[bold red]Error: You must enter numbers separated by commas.[/bold red]")
            return select_users(list_of_users)
        if int(users) > len(list_of_users):
            rprint("[bold red]Error: You entered a number greater than the number of users available.[/bold red]")
            return select_users(list_of_users)
        if -1 < int(users) < 1:
            print("You selected: Random")
            list_of_users = select_random_users(list_of_users)
            return list_of_users
    
    users = users.split(',')
    for i in users:
        if not i.isdigit():
            rprint("[bold red]Error: You must enter numbers separated by commas.[/bold red]")
            return select_users(list_of_users)
        if int(i) > len(list_of_users):
            rprint("[bold red]Error: You entered a number greater than the number of users available.[/bold red]")
            return select_users(list_of_users)
        if int(i) < 1:
            rprint("[bold red]Error: You can not select random and specific users.[/bold red]")
            return select_users(list_of_users)

    users = [int(i)-1 for i in users]
    selected_users = [list_of_users[i] for i in users]
    print("You selected: " + ", ".join(selected_users))
    return selected_users

def print_selected_users_status(users_list):
    rprint("[bold blue]Selected users:[/bold blue]")
    users_panel = [Panel(user, expand=False) for user in users_list]
    rprint(Columns(users_panel))

def select_option(extra_info, users_color):
    print("\n")
    if extra_info:
        print_selected_users_status(users_color)
    rprint("\n[bold blue]Select one of the following options (By id or command):[/bold blue]")
    options_table()
    option = input("Option: ")
    
    return option

def ask_url():
    rprint("[bold blue]Enter the URL of the tweet you want to interact with:[/bold blue]")
    url = input("URL: ")
    # check if url is a valid twitter status url
    url_pattern = re.compile(r'https://twitter.com/(\w+)/status/(\d+)')
    if url_pattern.match(url):
        return url
    rprint("[bold red]Error: You must enter a valid URL.[/bold red]")
    return ask_url()

def ask_comment():
    rprint("[bold blue]Select an option:[/bold blue]")
    table = Table("ID", "Option")
    table.add_row("0", "Back to menu")
    table.add_row("1", "Manual comment")
    table.add_row("2", "Genearte comment with ChatGPT")
    rprint(table)
    comment_type = input("Selection: ")
    if not comment_type.isdigit():
        rprint("[bold red]Error: You must enter the ID of the selected option.[/bold red]")
        return ask_comment()
    elif 0 > int(comment_type) or int(comment_type) > 2:
        rprint("[bold red]Error: You entered an invalid option ID.[/bold red]")
        return ask_comment()
    elif int(comment_type) == 0:
        return None
    elif int(comment_type) == 1:
        rprint("[bold blue]Enter the comment:[/bold blue]")
        comment = input("Comment: ")
        return comment
    elif int(comment_type) == 2:
        comment = generate_comment_cgpt()
        if comment != None:
            return comment
        else:
            return None
    else:
        rprint("[bold red]Error: You entered an invalid option ID.[/bold red]")
        return ask_comment()

def generate_comment_cgpt():
    rprint("[bold blue]Enter the statement for chatgpt to generate the comment:[/bold blue]")
    sentence = input("Input: ")
    try:
        comment = chatgpt.gen_tw_comment(sentence)
    except:
        rprint("[bold red]Error: ChatGPT could not generate the comment. Try with manual comment.[/bold red]")
        logger.error("ChatGPT could not generate the comment.")
        return ask_comment()
    exit = False
    while not exit:
        rprint(f"[bold blue]The comment generated by ChatGPT is: {comment}.\nDo you want to use that comment?:[/bold blue]")
        table = Table("ID", "Option")
        table.add_row("0", "No, go back to the menu")
        table.add_row("1", "No, generate another comment")
        table.add_row("2", "Yes, use that comment")
        rprint(table)
        option = input("Selection: ")
        if not option.isdigit():
            rprint("[bold red]Error: You must enter the ID of the selected option.[/bold red]")
        elif 0 > int(option) or int(option) > 2:
            rprint("[bold red]Error: You entered an invalid option ID.[/bold red]")
        elif int(option) == 0:
            return None
        elif int(option) == 1:
            return generate_comment_cgpt()
        elif int(option) == 2:
            return comment
        else:
            rprint("[bold red]Error: You entered an invalid option ID.[/bold red]")

    return None