#!/usr/bin/env bash
# Write a Bash script that sets up your web servers for the deployment
sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y install nginx
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/


echo -e "Hello, Sarah" > index.html
sudo mv index.html /data/web_static/releases/test/
if [ -L /data/web_static/current ]; then
    sudo rm /data/web_static/current
fi
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

sudo chown -hR ubuntu:ubuntu /data/web_static/
if ! grep -q "location \/test" /etc/nginx/sites-available/default; then
    # Use a temporary file to store the new configuration
    tmpfile=$(mktemp)
    cat <<EOL > "$tmpfile"
        location /test/ {
            root /data/web_static/releases/;
        }
EOL
    # Use sed to insert the contents of the temporary file after the 'listen' line
    sudo sed -i "/    listen \[::\]:80 default_server;/r $tmpfile" /etc/nginx/sites-available/default
    # Remove the temporary file
    rm "$tmpfile"
fi

if ! grep -q "location \/hbnb_static" /etc/nginx/sites-available/default; then
sudo sed -i '38i\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default

fi
sudo service nginx restart
