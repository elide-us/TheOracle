FROM python:3.12

# Install FFmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Set up the FastAPI application
WORKDIR /app

# Copy everything, including startup.sh
COPY . /app

# Set virtual environment as the default Python environment
ARG PYTHON_ENV=/app/venv
ENV VIRTUAL_ENV=$PYTHON_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Create virtual environment and install dependencies
RUN python -m venv $VIRTUAL_ENV && \
    . $VIRTUAL_ENV/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Expose the FastAPI port
EXPOSE 8000

# Ensure startup.sh is executable
RUN chmod +x /app/startup.sh

# Run the startup shell script
CMD ["/bin/sh", "/app/startup.sh"]
