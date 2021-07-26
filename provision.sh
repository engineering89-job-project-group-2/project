#!/usr/bin/env python3

sudo apt update -y
sudo apt install nginx

cd /etc/nginx/sites-available
sudo rm -rf default
sudo echo "server{
        listen 80;
        server_name _;
        location / {
        proxy_pass http://192.168.10.100:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
        }
}" >> default
sudo nginx -t
sudo systemctl reload nginx

cd
sudo apt update -y
sudo apt install python3-pip -y
pip3 --version

cd project
# use `pip3 freeze > requirements.txt` to make req.text
# python3 -m pip install -r requirements.txt
pip3 install flask
pip3 install flask_wtf
pip3 install pandas
pip3 install passlib
pip3 install lxml

sudo chmod +x main.py
python3 main.py