# Base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create app directory
WORKDIR /app

# Copy server code and database
COPY server.py database.json /app/

# Expose the server port
EXPOSE 8888

# Run the server
CMD ["python", "server.py"]