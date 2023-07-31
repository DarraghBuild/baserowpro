#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

# User input
echo "Welcome to the single instance Baserow deployment"
echo ""
echo "We will need sudo access so the next question is for you to give us superuser access"
echo "Please enter your sudo password now:"
sudo echo ""
echo "Thanks!"
echo "Change BASEROW_PUBLIC_URL to your domain name or http://YOUR_SERVERS_IP"
echo "if you want to access Baserow remotely."
echo ""
echo "⚠️  Please enter valid BASEROW_PUBLIC_URL ⚠️"
printf "%s" "Enter URL: " 
read url

if [[  $url != http?(s)://* ]];
then
	echo ""
    echo "$url IS NOT valid"   
	echo ""     
else
	echo ""
    echo "$url IS valid"
	echo ""
fi

curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Linux post-install
	sudo usermod -aG docker $USER
	sudo su - $USER -c exit;
	sudo systemctl enable docker
	sudo chmod 666 /var/run/docker.sock
# Change BASEROW_PUBLIC_URL to your domain name or http://YOUR_SERVERS_IP if you want
# to access Baserow remotely.
# This command will run Baserow with it's data stored in the new baserow_data docker 
# volume.
	docker run -e BASEROW_PUBLIC_URL=$url \
	--name baserow \
	-d \
	--restart unless-stopped \
	-v baserow_data:/baserow/data \
	-p 80:80 \
	-p 443:443 \
	baserow/baserow:1.18.0

echo "We will need to wait few minutes for things to settle down and migrations to finish"
echo ""
echo "⏳ Waiting for Baserow web to boot (this will take a few minutes)"
while [[ "$(curl -s -o /dev/null -I -w "%{http_code}" "$url"/api/_health/)" != "200" ]]; do sleep 5; done
echo "⌛️ Baserow looks up!"
echo ""
echo "🎉🎉🎉  Done! 🎉🎉🎉"