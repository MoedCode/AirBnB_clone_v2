#!/usr/bin/env bash
# Bash script that sets up web servers for the deployment of web_static

# Update package lists and install Nginx
sudo apt-get update
sudo apt-get -y install nginx

# Allow Nginx through the firewall
sudo ufw allow 'Nginx HTTP'

# Create necessary directories for web_static deployment
sudo mkdir -p /data/web_static/releases/test/
sudo touch /data/web_static/releases/test/index.html

# Create a simple HTML content for testing
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create or update symbolic link to the latest deployment
sudo ln -s -f /data/web_static/releases/test/ /data/web_static/current

# Set ownership of the /data/ directory to the ubuntu user and group recursively
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to serve /data/web_static/current/ as /hbnb_static
nginx_config="/etc/nginx/sites-enabled/default"
sudo sed -i '/listen 80 default_server/a location /hbnb_static { alias /data/web_static/current/;}' "$nginx_config"

# Restart Nginx to apply changes
sudo service nginx restart

# Exit successfully
exit 0
