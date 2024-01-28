#!/usr/bin/env bash
# install nginx

sudo apt-get update
sudo apt-get install nginx -y

sudo mkdir -p /data/
sudo mkdir -p /data/web_static/
sudo mkdir -p /data/web_static/releases/
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test
sudo touch /data/web_static/releases/test/index.html
echo "<html>
	<head>
	</head>
	<body>
		<p>Hello World!</p>
	</body>
</html>" | sudo tee  /data/web_static/releases/test/index.html

sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

sudo sed -i "/listen 80 default_server;/ a \\\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n" /etc/nginx/sites-available/default

sudo service nginx restart
