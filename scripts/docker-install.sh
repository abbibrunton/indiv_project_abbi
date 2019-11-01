cd ..
if [ -x "$(command -v docker)" ]; then
	echo 'docker already installed'
else
    echo 'docker not already installed. installing...'
    curl https://get.docker.com | sudo bash
fi

if sudo docker ps -a | grep "indiv"; then
	sudo docker rm -f indiv
fi


sudo docker build -t indiv-project:latest .
sudo docker run -d -p 5000:5000 --name indiv indiv-project
