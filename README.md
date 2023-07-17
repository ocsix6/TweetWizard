# TweetWizard
TweetWizard is an automation tool designed to facilitate interaction with publications on the Twitter social network. This tool allows the simultaneous management of multiple accounts, which can be used to simulate a botnet. This functionality can facilitate the generation of opinion trends on this social network.

This tool has been developed exclusively for educational or research purposes, therefore the author of this tool is not responsible for any improper use that may be made of it.

## Notes
As with all web automation tools, TweetWizard relies on the code structure of the Twitter website for its operation. This means that any changes made by Twitter to its code may affect the proper functioning of the tool until the necessary adaptations are made.

Sometimes, websites make minor modifications, such as changing the names of classes or modifying the XPath of certain elements, in order to make web automation or *web scraping* tasks more difficult.

## Instructions
In order to make use of the developed tool, the following requirements are necessary.
1. Create the file `config/keys.ini`, based on the [example file](config/keys_example.ini) `config/keys_example.ini` provided.
2. In the [configuration file](config/config.ini) `config/config.ini`, the number of `max_threads` can be modified as needed. This parameter determines the maximum number of threads to be used in the tool to perform Twitter interaction tasks.
3. Create the file `data/input/tw_accounts.csv` from the [example file](data/input/tw_accounts_example.csv) `data/input/tw_accounts_example.csv` provided. This file should contain the list of Twitter accounts you want to interact with, in the format specified in the example.

Once the necessary files have been prepared and the settings have been adjusted, the next step is to install the project dependencies. These dependencies are specified in the [requirements.txt](requirements.txt) file provided. It is recommended to use a virtual environment management tool, such as Poetry, to perform the installation of the dependencies.

It is important to note that the tool has been developed using **Python version 3.9**. Therefore, it is strongly recommended to use this same version to ensure compatibility and correct operation of the program. Using a different version of Python may cause incompatibility problems and errors in the execution of the tool.

Once the dependencies have been installed, the tool can be run using the `python main.py` command. This will start the execution of the program.