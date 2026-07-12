pipeline {
    agent any

    stages {

       stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/kingslayer458/digital_ocean.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv

                    . venv/bin/activate

                    pip install --upgrade pip

                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run DigitalOcean vm extractor') {
            steps {

                withCredentials([
                    string(credentialsId: 'digitalocean-token',
                    variable: 'DIGITAL_OCEAN_TOKEN')])
                    {

                    sh '''
                        . venv/bin/activate

                        python3 -u get_vms.py
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
            echo 'DigitalOcean vms collected successfully.'
        }

        failure {
            echo 'vm collection failed.'
        }

        always {
            cleanWs()
        }
    }
}