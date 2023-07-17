from modules.logger import logger
import modules.utils as utils
import modules.data_reader as data_reader
import modules.scraper as scraper
import modules.cli as cli
import concurrent.futures
import sys
import os


def main():
    # Get the number of cpus
    # n_cpus = os.cpu_count()
    
    # Log the start of the program
    logger.info('Program started')
    
    # Initialize global variables
    global selected_users, open_sessions, extra_info, config_max_threads    
    open_sessions = {}
    extra_info = True

    # Get project root library
    actual_path = utils.get_path(__file__)

    # Get the path of the configuration directory
    config_path = os.path.join(actual_path, '..', 'config')

    # Get the path of the input data directory
    input_path = os.path.join(actual_path, '..', 'data', 'input')

    # Read the configuration files
    global_config = data_reader.read_config(config_path+"/config.ini")

    # Read the twitter accounts
    tw_accounts = data_reader.load_csv(input_path+"/tw_accounts.csv")
    
    # First user is selected by default
    selected_users = [tw_accounts[0]["mail"]]

    # Get value of max_threads
    config_max_threads = global_config.getint('threads', 'max_threads')

    cli.init_screen()
    while True:
        prompt = cli.select_option(extra_info, get_users_color())

        if prompt == "0" or prompt == "exit":
            # Stop program execution
            exit = input("¿Are you sure you want to exit? [y/n]: ")
            if exit == "y":
                logger.info('Program finished')
                cli.exit_msg()
                sys.exit()
        
        elif prompt == "1" or prompt == "info":
            extra_info = not extra_info

        elif prompt == "2" or prompt == "users":
            mails_list = [i["mail"] for i in tw_accounts]
            selected_users = cli.select_users(mails_list)
        
        elif prompt == "3" or prompt == "login":
            # Log in of all selected users and logout of all unselected users
            cli.executing_msg()
            # Getting the new sessions to open
            sessions_to_open = [user for user in tw_accounts if user["mail"] in selected_users and user["mail"] not in open_sessions]
            # Getting the sessions to close
            sessions_to_close = [user for user in open_sessions if user not in selected_users]
            
            # Multi-threading
            with concurrent.futures.ThreadPoolExecutor(max_workers=config_max_threads) as executor:
                futures = []
                # Opening the new sessions
                for user in sessions_to_open:
                    future = executor.submit(scraper.Scraper, "https://twitter.com/i/flow/login", user["mail"], user["usr"], user["pwd"])
                    futures.append(future)

            # Closing the sessions to close
            for future, user in zip(futures, sessions_to_open):
                open_sessions[user["mail"]] = future.result()

            close_session_async(sessions_to_close)


        elif prompt == "4" or prompt == "logout":
            cli.executing_msg()
            sessions_to_close = [user for user in open_sessions]
            # Closing the sessions to close
            close_session_async(sessions_to_close)

        
        elif prompt == "5" or prompt == "like":
            url = cli.ask_url()
            cli.executing_msg()

            with concurrent.futures.ThreadPoolExecutor(max_workers=config_max_threads) as executor:
                futures = []
                for user in open_sessions:
                    future = executor.submit(open_sessions[user].like_tweet, url)
                    futures.append(future)
                for future in futures:
                    future.result()

        elif prompt == "6" or prompt == "retweet":
            url = cli.ask_url()
            cli.executing_msg()

            with concurrent.futures.ThreadPoolExecutor(max_workers=config_max_threads) as executor:
                futures = []
                for user in open_sessions:
                    future = executor.submit(open_sessions[user].retweet, url)
                    futures.append(future)
                for future in futures:
                    future.result()
        
        elif prompt == "7" or prompt == "like_rt":
            url = cli.ask_url()
            cli.executing_msg()

            with concurrent.futures.ThreadPoolExecutor(max_workers=config_max_threads) as executor:
                futures = []
                for user in open_sessions:
                    future = executor.submit(open_sessions[user].like_tweet, url)
                    futures.append(future)
                for future in futures:
                    future.result()
                futures = []
                for user in open_sessions:
                    future = executor.submit(open_sessions[user].retweet, url)
                    futures.append(future)
                for future in futures:
                    future.result()

        
        elif prompt == "8" or prompt == "comment":
            url = cli.ask_url()
            comment = cli.ask_comment()
            if comment != None:
                cli.executing_msg()

                with concurrent.futures.ThreadPoolExecutor(max_workers=config_max_threads) as executor:
                    futures = []
                    for user in open_sessions:
                        future = executor.submit(open_sessions[user].comment_tweet, url, comment)
                        futures.append(future)
                    for future in futures:
                        future.result()

        else:
            print("Invalid option, try again.")

def get_users_color():
    users_color = []
    for user in selected_users:
        if user in open_sessions:
            users_color.append(f"[green]{user}[/green]")
        else:
            users_color.append(f"[red]{user}[/red]")
    return users_color

def close_session(user):
    open_sessions[user].logout()
    open_sessions[user].close()
    del open_sessions[user]

def close_session_async(sessions_to_close):
    with concurrent.futures.ThreadPoolExecutor(max_workers=config_max_threads) as executor:
        futures = []
        for user in sessions_to_close:
            future = executor.submit(close_session, user)
            futures.append(future)
        for future in futures:
            future.result()

if __name__ == "__main__":
    main()