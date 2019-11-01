cd ..
#checking if docker is already installed
if [ -x "$(command -v docker)" ]; then
	echo 'docker already installed'
else
    echo 'docker not already installed. installing...'
    curl https://get.docker.com | sudo bash
fi
#checking if the project is already running
if sudo docker ps -a | grep "indiv"; then
	sudo docker rm -f indiv
fi

#building and running the application
sudo docker build -t indiv-project:latest .
sudo docker run -d -p 5000:5000 --name indiv indiv-project
