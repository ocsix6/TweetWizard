import os
import modules.utils as utils
import modules.data_reader as data_reader
import openai

def read_api_key():
    actual_path = utils.get_path(__file__)

    # Get the path of the configuration directory
    config_path = os.path.join(actual_path, '..', '..', 'config')

    # Read the configuration file
    keys_config = data_reader.read_config(config_path+"/keys.ini")

    # Get the OpenAI API key
    openai_key = keys_config.get('keys', 'openai_api_key')

    return openai_key


def gen_tw_comment(input_text):
    
    # Set OpenAI API key
    openai.api_key = read_api_key()

    # Context of the agent
    context = {"role": "system", "content": "You are a very useful assistant, an expert in generating comments for the social network Twitter and making them appear to be written by humans."}
    messages = [context]

    # User input
    content = input_text

    messages.append({"role": "user", "content": content})

    # Generate response
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    # Get response message content
    response_content = response.choices[0].message.content

    return response_content