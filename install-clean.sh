#!/bin/bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
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