# Specify the base image
FROM python:3.14-slim

# Set environment variables
# Prevents Python from writing .pyc files and enables unbuffered output for real-time logs.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
# Updates apt and installs necessary libraries for building Python and system dependencies.
RUN apt-get update && apt-get install -y \
    --no-install-recommends && \
    # Remove unnecessary files
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*   

# Install Node.js directly
# RUN curl -fsSL https://nodejs.org/dist/v22.2.0/node-v22.2.0-linux-x64.tar.xz | tar -xJ -C /usr/local --strip-components=1

# Copy the entire project (including frontend and backend)
COPY . /app/

# Set execute permissions for the entrypoint script
# RUN chmod +x /app/entrypoint.sh

# Install frontend dependencies and build
# WORKDIR /app/frontend
# RUN npm ci
# RUN npm run build

# Switch back to backend directory
# WORKDIR /app/backend

# Install pipenv
RUN pip install uv

# Copy nginx config
# COPY nginx.conf /etc/nginx/nginx.conf

# Install dependencies
RUN uv sync

# Activate the virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Expose the port the app runs on
EXPOSE 8000

# Set the entrypoint script
# ENTRYPOINT ["sh", "/app/entrypoint.sh"]

# Run the application 
CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["gunicorn", "babelpay.wsgi:application", "--bind", "0.0.0.0:8000"]


# Build the Docker image
# sudo docker build -t leet:test .

# Run the Docker container
# sudo docker run -p 8000:8000 --env-file example.env leet:test

# Run the Docker container in detached mode
# sudo docker run -d -p 8000:8000 --env-file example.env leet:test

# Stop the Docker container
# sudo docker stop <container_id>

# Run container with terminal access
# docker exec -it image_name sh
