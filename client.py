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

def list_templates():
    templates_dir = "templates"
    templates = []
    for f in os.scandir(templates_dir):
        if f.is_file():
            with open(f.path, "r") as template_file:
                template_content = template_file.readline().strip() # Read only the first line
                templates.append((template_content, f.name))
    return templates

def read_template(template_name):
    template_path = os.path.join("templates", template_name)
    with open(template_path, "r") as template_file:
        template_content = template_file.readlines() # Read lines instead of reading the whole content
    # Strip the first line from the context
    return '\n'.join(template_content[1:]) if template_content else ''

def send_chat_message(message_content, api_key):
    client = Groq(api_key=api_key)     
    try:
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
    api_key = read_api_key()     
    if not api_key:
        raise GroqClientError("API key not found in config.txt. Please make sure the file exists and contains the API key.")     
    st.set_page_config(layout="wide")     
    templates = list_templates()
    selected_template = st.selectbox("Select a template:", [t[0] for t in templates], key="selected_template")
    if selected_template is not None:          
        selected_template_name = [t[1] for t in templates if t[0] == selected_template][0]
        user_input = st.text_area("Enter your message here:", key="user_input")     
        if user_input:          
            try:
                template_content = read_template(selected_template_name)
                response = send_chat_message(template_content + "\n" + user_input, api_key)
                st.write("Response:")
                st.write(response)
            except GroqClientError as e:
                st.error(f"Error: {e.message}") 
    else:
        st.warning("Please select a template before sending your message.")

if __name__ == "__main__":
    main()