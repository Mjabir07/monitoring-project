# Use a lightweight official Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy our requirements and install them securely
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the actual python script
COPY ai-bridge.py .

# Expose the port the bridge listens on
EXPOSE 5001

# Run the script
CMD ["python3", "ai-bridge.py"]
