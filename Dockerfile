# 1. Start with a clean, lightweight Linux system that already has Python
FROM python:3.11-slim

# 2. Create a folder inside the container called /app
WORKDIR /app

# 3. Copy our recipe book into the container
COPY requirements.txt .

# 4. Have Docker run the PIP INSTALL automatically inside the container
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy your dashboard code into the container (we will make this code next)
COPY dashboard.py .

# 6. Open the network port
EXPOSE 5000

# 7. Start the app
CMD ["python3", "dashboard.py"]
