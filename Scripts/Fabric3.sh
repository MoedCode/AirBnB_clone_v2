#!/usr/bin/env bash

# Uninstall previous Fabric version
pip3 uninstall Fabric

# Install required dependencies
sudo apt-get update
sudo apt-get install -y libffi-dev libssl-dev build-essential python3.4-dev libpython3-dev

# Install additional Python packages
pip3 install pyparsing appdirs setuptools==40.1.0 cryptography==2.8 bcrypt==3.1.7 PyNaCl==1.3.0

# Install Fabric for Python 3 - version 1.14.post1
pip3 install Fabric3==1.14.post1

