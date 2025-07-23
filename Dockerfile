# Use an official lightweight Python image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy your app files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create input and output folders inside container
RUN mkdir -p input output

# Run the script when the container starts
CMD ["python", "main.py"]
