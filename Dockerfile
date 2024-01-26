FROM python:3.10-slim

# Set working directory in the container
WORKDIR /app

# Install poetry
RUN pip install --no-cache-dir poetry

# Copy poetry lock files
COPY pyproject.toml ../poetry.lock ./

# Install dependencies
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi --no-root

COPY . /app
# Copy the application files to the container


# Run the application
CMD ["uvicorn", "streaming.app:app", "--host", "0.0.0.0"]