# Makefile for FastAPI project with Pipenv


# Define the Docker Compose service name for PostgreSQL
DB_SERVICE=db

# Start PostgreSQL
postgres-up:
	docker-compose up -d $(DB_SERVICE)

# Stop PostgreSQL (pause without deleting container)
postgres-down:
	docker-compose stop $(DB_SERVICE)

.PHONY: install run shell test lock clean

# Install all dependencies, including dev dependencies.
install:
	pipenv install --dev

# Run the FastAPI app using uvicorn.
# Adjust "main:app" to reflect your app's module and variable.
run:
	pipenv run uvicorn app.main:app --reload

# Open a shell with the virtual environment activated.
shell:
	pipenv shell

# Run tests using pytest.
test:
	pipenv run pytest

# Update the Pipfile.lock.
lock:
	pipenv lock

# Remove the virtual environment.
clean:
	pipenv --rm
