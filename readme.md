### intro
welcome to my app! this is a handy travel itinerary app for planning your next holiday. it has been developed using flask and html.

### prerequisites:
  sudo apt-get -y update
  
  sudo apt-get -y install python3
  
  sudo apt-get -y install python3-pip
  
if you want to run anything from the scripts folder, do the following:
  cd scripts
  
  chmod +x <SCRIPT NAME>
  
  ./<SCRIPT NAME>
  
## running the app

### local:
  if you want to run the app locally on your computer, run the local-install.sh script in the scripts folder.
  you can access the app by navigating to localhost:5000 in your web browser

### systemd:
  this app can be run using systemd. use the systemd-install.sh script provided in the scripts folder to do this.
  if you are using gcp to run the app, you can run it using http://<EXTERNAL IP>:5000

### docker:
  once you have cloned down the repository you can use the dockerfile to run the application.
  you can do this by using docker-install.sh. this will check if docker is already installed (and install it if not) and then check if the container has already been created (and delete it if it has). then it will build the docker container from the image provided and run the application.
  
  if you are using gcp to run the app, you can run it using http://EXTERNAL_IP:5000

### automation:
  
  a jenkinsfile has been provided which allows you to automate the deployment of the app
  you should set up the project as a pipeline and use a webhook to connect it to this repository
