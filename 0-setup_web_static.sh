#!/bin/bash

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null
then
    sudo apt-get -y update
    sudo apt-get -y install nginx
fi

# Create necessary folders
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared

# Create a fake HTML file
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create or recreate symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership to the ubuntu user and group recursively
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
config_file="/etc/nginx/sites-available/default"
if grep -q "location /hbnb_static {" "$config_file"; then
    sed -i '/location \/hbnb_static {/!b;n;c\\talias /data/web_static/current/;' "$config_file"
else
    sed -i '/server {/a\\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}' "$config_file"
fi

# Restart Nginx
sudo service nginx restart

# Exit successfully
exit 0
