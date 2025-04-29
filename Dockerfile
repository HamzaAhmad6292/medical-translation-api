# Use official Python image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose FastAPI’s default port
EXPOSE 8080

# Run FastAPI with the correct import path
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
