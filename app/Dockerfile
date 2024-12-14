# Use Python as the base image
FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy the requirements and the application code
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port on which the app will run
EXPOSE 8888

# Set the entrypoint to run the application
CMD ["python", "app.py"]
