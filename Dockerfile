# Use a lightweight Python image
FROM python:3.11-slim

# Set environment vars
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy app files
COPY . .

# Expose Flask port
EXPOSE 5000

# Run Flask app
CMD ["flask", "--app", "app", "--debug", "run", "--host=0.0.0.0"]
