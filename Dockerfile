ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim AS base

# Install system dependencies and compilers
RUN apt-get update && apt-get install -y \
    curl make xz-utils perl fontconfig git \
    libpq-dev wget gcc g++ build-essential && \
    apt-get clean

# Set working directory
WORKDIR /app

# Copy Pipenv files and install dependencies
COPY Pipfile Pipfile.lock /app/
RUN pip install --no-cache-dir pipenv && \
    pipenv install --deploy --ignore-pipfile

# Copy the rest of your FastAPI project
COPY . /app

# Expose FastAPI port
EXPOSE 8000

# Start the FastAPI server using Pipenv
CMD ["pipenv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]