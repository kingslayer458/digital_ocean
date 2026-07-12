pipeline {

    agent {
        docker {
            image 'python:3.12'
            reuseNode true
        }
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/kingslayer458/digital_ocean.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python -m venv venv
                    . venv/bin/activate

                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run DigitalOcean vms Extractor') {
            steps {
                withCredentials([
                    string(credentialsId: 'digitalocean-token',
                           variable: 'DIGITAL_OCEAN_TOKEN')]) {
                    sh '''
                        . venv/bin/activate
                        python -u get_vms.py
                    '''
                }
            }
        }

        stage('Archive JSON') {
            steps {
                archiveArtifacts artifacts: 'vm_data_digital_ocean.json', fingerprint: true
            }
        }
    }

    post {
        success {
            echo 'DigitalOcean VMs collected successfully.'
        }

        failure {
            echo 'VM collection failed.'
        }

        always {
            cleanWs()
        }
    }
}