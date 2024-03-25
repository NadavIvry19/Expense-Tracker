FROM mongo:latest

# Optional: Set environment variables for authentication (replace with your strong password)
ENV MONGO_INITDB_ROOT_USERNAME='mongoadmin'
ENV MONGO_INITDB_ROOT_PASSWORD='your_strong_password'
