if [ -x "$(command -v docker)" ]; then
    echo 'docker already installed'
else
    echo 'installing docker'
    curl https://get.docker.com | sudo bash
fi
