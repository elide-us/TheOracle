# Use the official Python slim image
FROM python:3.10-slim

# Set working directory in the container
WORKDIR /app

# Copy project files into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r app/requirements.txt

# Expose a port (optional if using a Flask wrapper for health check)
# EXPOSE 8000

# Set the command to start the bot
CMD ["python", "bot.py"]
