# Build the Docker image
docker build -t stock-prediction-app .

# Run the Docker container
docker run -p 8501:8501 stock-prediction-app
