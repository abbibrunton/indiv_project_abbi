cd ..
#checking if docker is already installed
if [ -x "$(command -v docker)" ]; then
	echo 'docker already installed'
else
    echo 'docker not already installed. installing...'
    curl https://get.docker.com | sudo bash
fi

#checking if docker-compose is already installed
if [ -x "$(command -v docker-compose)" ]; then
	echo 'docker-compose already installed'
else
    echo 'docker-compose not already installed. installing...'
    sudo curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi
#deleting network
docker network rm indiv_project_abbi_default
#running docker-compose
sudo docker-compose up -d
