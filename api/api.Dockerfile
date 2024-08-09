# Use the official Python image as the base image
FROM python:3.10-slim


# Set the working directory inside the container
WORKDIR /code

# Copy the pyproject.toml files to the working directory
COPY pyproject.toml /code/

# Install poetry
RUN pip install poetry

# Install project dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Copy the rest of the application code to the working directory
COPY . /code/app

# Expose the port on which the FastAPI application will run
EXPOSE 8000

# Run the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]