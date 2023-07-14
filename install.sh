#!/bin/bash
if [ -x "$(command -v docker)" ]; then
    #echo "Update docker"
	sudo apt-get update && sudo apt-get upgrade docker-ce
else
    sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
	curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
	sudo apt-key fingerprint 0EBFCD88
	sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
	sudo apt-get update
	sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y 
fi
# Linux post-install
	sudo usermod -aG docker $USER
	sudo su - $USER -c exit;
	sudo systemctl enable docker
	
# Change BASEROW_PUBLIC_URL to your domain name or http://YOUR_SERVERS_IP if you want
# to access Baserow remotely.
# This command will run Baserow with it's data stored in the new baserow_data docker 
# volume.

	docker run -e BASEROW_PUBLIC_URL=http://localhost \
	--name baserow \
	-d \
	--restart unless-stopped \
	-v baserow_data:/baserow/data \
	-p 80:80 \
	-p 443:443 \
	baserow/baserow:1.18.0
# Watch the logs for Baserow to come available by running:
	docker logs baserow
