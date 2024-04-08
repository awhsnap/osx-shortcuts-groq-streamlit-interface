# Streamlit and Groq Workflow Basic
On OSX, using the shortcuts app and use shell to run.sh. It opens VSCode and source the enviornment. Finally open a web browser terminal pointing to streamlit groq interface.


## How-To Install
Clone the repo and virtualenv venv in your pwd. Source into the enviorment and pip install -r requirements.txt.

## Using Shortcuts on Mac M1 
Using the script below we can automate running our groq client and opening code. 

```
#!/bin/bash

sandbox_dir="sandbox"

osascript -e "tell application \"Terminal\" to do script \"cd '$sandbox_dir'; code . && source venv/bin/activate && streamlit run client.py && clear\""
```