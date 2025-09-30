# Use the official Python image as a base
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file and install dependencies
# The updated requirements.txt now pins Jinja2 to a version compatible with Flask 1.1.2
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY main.py .

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application using Gunicorn (secure and standard WSGI server)
# The application is started as 'app:app' (app.py module : Flask app instance name)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
