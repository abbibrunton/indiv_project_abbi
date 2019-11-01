pipeline{
    agent any
    stages{ 
		stage('---Build_Image---'){
            steps{
                sh "sudo docker build -t indiv-project:latest ."
		
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
