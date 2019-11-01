pipeline{
    agent any
    stages{ 
		stage('---Build_Image---'){
            steps{
                sh label: '', script:
		'''
		if [ ! "$(cat /etc/passwd | grep pythonadm)" ];
  		then sudo useradd -m -s /bin/bash pythonadm
		fi
		sudo docker build -t indiv-project:latest .
		'''
            }
        }
        stage('---Clean_Container---'){
            steps{
                sh label: '', script: 
                '''
                if [ "$(sudo docker ps -qa -f name=indiv)" ]; then
                        sudo docker rm -f indiv
                fi
                '''
            }
        }
        stage('---Build_Container---'){
            steps{
                sh "sudo docker run -d -p 5000:5000 --name indiv indiv-project"
            }
        }
    }
}
