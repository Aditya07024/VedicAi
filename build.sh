#!/bin/bash

# Install system dependencies for swisseph
apt-get update
apt-get install -y build-essential

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt
