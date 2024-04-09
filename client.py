import os
import configparser
import streamlit as st
from groq import Groq 

# Custom exception class for Groq API errors
class GroqClientError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def read_api_key():
    api_key = None
    config_file_path = "config.txt"     
    if os.path.exists(config_file_path):
        config = configparser.ConfigParser()
        config.read(config_file_path)        
        if 'API' in config and 'GROQ_API_KEY' in config['API']:
            api_key = config['API']['GROQ_API_KEY']     
    return api_key 

def send_chat_message(message_content, api_key):
    # Initialize the Groq client with the API key
    client = Groq(api_key=api_key)     
    try:
        # Send a chat completion request
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": message_content,
                }
            ],
            model="mixtral-8x7b-32768",
        )         
        if chat_completion.choices:
            return chat_completion.choices[0].message.content
        else:
            return "No response received from the chat completion."
    except Exception as e:
        raise GroqClientError(f"Groq API Error: {str(e)}") 

def main():
    # Read API key from config.txt
    api_key = read_api_key()     
    if not api_key:
        raise GroqClientError("API key not found in config.txt. Please make sure the file exists and contains the API key.")     
    # Set Streamlit layout to wide
    st.set_page_config(layout="wide")     
    user_input = st.text_area("Enter your message here:", key="user_input")     
    if user_input:          
        # Send user input to Groq API and display response
        try:
            response = send_chat_message(user_input, api_key)
            st.write("Response:")
            st.write(response)
        except GroqClientError as e:
            st.error(f"Error: {e.message}") 

if __name__ == "__main__":
    main()