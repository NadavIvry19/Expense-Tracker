pipeline {
    agent {
        kubernetes {
            label 'ez-joy-friends'
            idleMinutes 5
            yamlFile 'build-pod.yaml'
            defaultContainer 'ez-docker-helm-build'
        }
    }

    environment {
        GITLAB_CREDS = 'nadav-gitlab'
        MONGODB_URI = 'mongodb://mongo:27017/expense_tracker'
        PROJECT_ID = '55376310'
        GITLAB_URL = 'https://gitlab.com'
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker image') {
            steps {
                script {
                    // Build Docker image using Dockerfile in the root directory
                    docker.build("my-custom-image", "--no-cache .")
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    sh 'docker-compose -f docker-compose.yaml up -d'
                    sh 'docker-compose -f docker-compose.yaml run test pytest'
                    sh 'docker-compose -f docker-compose.yaml down'
                }
            }
        }

        stage('Push Docker image') {
            when {
                branch 'main'
            }
            steps {
                script {
                    def dockerHub = docker.registry('https://registry.hub.docker.com', 'nadav-docker-hub')
                    def customImage = docker.image('my-custom-image:latest')
                    customImage.push('latest')
                }
            }
        }

        stage('Create Merge Request') {
            when {
                not {
                    branch 'main'
                }
            }
            steps {
                script {
                    withCredentials([string(credentialsId: 'dary-gitlab-api', variable: 'GITLAB_API_TOKEN')]) {
                        def response = sh(script: """
                        curl -s -o response.json -w "%{http_code}" --header "PRIVATE-TOKEN: ${GITLAB_API_TOKEN}" -X POST "${GITLAB_URL}/api/v4/projects/${PROJECT_ID}/merge_requests" \
                        --form "source_branch=${env.BRANCH_NAME}" \
                        --form "target_branch=main" \
                        --form "title=MR from ${env.BRANCH_NAME} into main" \
                        --form "remove_source_branch=true"
                        """, returnStdout: true).trim()
                        if (response.startsWith("20")) {
                            echo "Merge request created successfully."
                        } else {
                            echo "Failed to create merge request. Response Code: ${response}"
                            def jsonResponse = readJSON file: 'response.json'
                            echo "Error message: ${jsonResponse.message}"
                            error "Merge request creation failed."
                        }
                    }
                }
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}
