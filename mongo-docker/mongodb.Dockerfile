FROM mongo:latest

# Set environment variables with strings (not recommended for production)
ENV MONGO_INITDB_ROOT_USERNAME='nadav'
ENV MONGO_INITDB_ROOT_PASSWORD='your_strong_password'

# Define the volume path for data persistence
VOLUME /data/db

CMD ["mongod", "--auth"]  
