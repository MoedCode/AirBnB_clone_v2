#!/bin/bash

# Create /data/ directory if it doesn't exist
mkdir data/

# Create /data/web_static/ directory if it doesn't exist
mkdir data/web_static/

# Create /data/web_static/releases/ directory if it doesn't exist
mkdir data/web_static/releases/

# Create /data/web_static/shared/ directory if it doesn't exist
mkdir data/web_static/shared/

# Create /data/web_static/releases/test/ directory if it doesn't exist
mkdir data/web_static/releases/test/

# Create a fake HTML file /data/web_static/releases/test/index.html
echo "<html><head><title>Test Page</title></head><body><h1>This is a test page</h1></body></html>" > /data/web_static/releases/test/index.html

mkdir data/
mkdir data/web_static/
mkdir data/web_static/releases/
mkdir data/web_static/shared/
mkdir data/web_static/releases/test/
