# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Run the WSGI server (Gunicorn)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
