#!/bin/bash

# Istallation update & upgrade

sudo apt-get update

# Install dependencies using pip
pip3 install -r requirements.txt

# Inform the user about successful installation
echo "Installation completed successfully."