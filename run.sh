#!/bin/bash

# Command to activate the virtual environment
command_to_execute="source venv/bin/activate"

# AppleScript command to execute the command in a new Terminal window
osascript -e "tell application \"Terminal\" to do script \"$command_to_execute\""
