#Python image
FROM python:3.10-slim

# Set working directory in container
WORKDIR /app

ENV PYTHONPATH /app

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# List the contents of the /app directory
RUN ls /app

# Expose a port 
EXPOSE 8000

CMD ["python", "api.py"]