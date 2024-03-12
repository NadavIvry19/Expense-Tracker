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
        // No longer using the 'localhost' since we'll be using a Docker network
        PROJECT_ID = '55376310'
        GITLAB_URL = 'https://gitlab.com'
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Application Docker image') {
            steps {
                script {
                    // Build the Docker image using the Dockerfile at the root of the repository
                    dockerImage = docker.build("my-final-project-web:latest", "--no-cache .")
                }
            }
        }

        stage('Build Test Docker image and Run Tests') {
            steps {
                script {
                    // Create a custom Docker network
                    sh 'docker network create expense-tracker-net'
                    
                    // Build the Docker test image
                    def testDockerImage = docker.build("my-final-project-app-tests:${BUILD_NUMBER}", "-f Dockerfile.test .")
                    
                    // Start MongoDB container on the custom network
                    sh 'docker run -d --name mongodb-test --network expense-tracker-net mongo:latest'
                    
                    // Wait for MongoDB to fully start
                    sh 'sleep 10'
                    
                    // Run the test container on the custom network, ensure the MONGO_URI environment variable
                    // is set within the container to use the MongoDB container's hostname
                    sh 'docker run --name expense-tracker-test-container --network expense-tracker-net -e MONGO_URI=mongodb://mongo:27017/expenses_tracker my-final-project-app-tests:${BUILD_NUMBER}'
                }
            }
        }

        stage('Push Docker image') {
            when {
                branch 'main'
            }
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'nadav-docker-hub') {
                        dockerImage.push("${env.BRANCH_NAME}-${env.BUILD_NUMBER}")
                        dockerImage.push("latest")
                    }
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
                    withCredentials([string(credentialsId: 'nadav-gitlab', variable: 'GITLAB_API_TOKEN')]) {
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
            // Cleanup MongoDB container, the test container, and the custom network
            // to ensure no conflicts on subsequent runs
            sh 'docker rm -f mongodb-test'
            sh 'docker rm -f expense-tracker-test-container'
            sh 'docker network rm expense-tracker-net'
            cleanWs()
        }
    }
}
