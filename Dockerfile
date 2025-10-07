# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies (ffmpeg for pydub)
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Install uv
RUN pip install uv

# Copy the dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv export --no-dev | uv pip install --system -r -

# Copy the application code
COPY ./app ./app

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["fastapi", "run", "--host", "0.0.0.0", "--port", "8000"]
