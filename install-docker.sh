#!/bin/bash

# Comprehensive script to install Docker, Docker Compose, and set up the MLRChecker application

echo "Starting Docker and Docker Compose installation..."

# Check if script is run as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run this script with sudo or as root"
  exit 1
fi

# Install Docker using the convenience script
echo "Installing Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
rm get-docker.sh

# Check if Docker was installed successfully
if ! command -v docker &> /dev/null; then
    echo "Docker installation failed. Please check for errors above."
    exit 1
fi

# Install Docker Compose
echo "Installing Docker Compose..."
COMPOSE_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep 'tag_name' | cut -d\" -f4)
curl -L "https://github.com/docker/compose/releases/download/${COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Check if Docker Compose was installed successfully
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose installation failed. Please check for errors above."
    exit 1
fi

# Add the current user to the docker group
echo "Adding current user to the docker group..."
usermod -aG docker $SUDO_USER || usermod -aG docker $USER

# Start and enable Docker service
echo "Starting and enabling Docker service..."
systemctl start docker
systemctl enable docker

# Print versions
echo "Installation completed successfully!"
echo "Docker version: $(docker --version)"
echo "Docker Compose version: $(docker-compose --version)"
echo ""
echo "IMPORTANT: You may need to log out and log back in for group changes to take effect."
echo "To verify the installation, run: docker run hello-world"

# =====================================================================
# Application Setup Section (from docker-setup.sh)
# =====================================================================

echo ""
echo "Setting up MLRChecker application..."

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    echo "Please enter your Google API key for Gemini:"
    read -r api_key
    echo "GOOGLE_API_KEY=\"$api_key\"" > .env
    echo "ANALYSER_A2A_HOST=\"0.0.0.0\"" >> .env
    echo "ANALYSER_A2A_PORT=8003" >> .env
    echo ".env file created successfully."
else
    echo ".env file already exists. Using existing configuration."
fi

# Create directories for volumes
echo "Creating directories for volumes..."
mkdir -p static temp
chmod 777 static temp

# Build and start the Docker container
echo "Building and starting the Docker container..."
docker-compose up -d

# Check if the container is running
if [ "$(docker ps -q -f name=mlrchecker)" ]; then
    echo "MLRChecker is now running at http://localhost:8003"
    echo "To check the logs, run: docker-compose logs -f"
    echo "To stop the container, run: docker-compose down"
else
    echo "Failed to start the container. Please check the logs with: docker-compose logs"
    exit 1
fi
