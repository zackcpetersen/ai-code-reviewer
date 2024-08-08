FROM python:3.11-slim as base

# Base stage for shared environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8

# Install pipenv
RUN pip install --no-cache-dir pipenv

FROM base AS python-deps

# Install dependencies
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy

FROM base AS runtime

# Copy installed packages from python-deps stage
COPY --from=python-deps /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=python-deps /usr/local/bin /usr/local/bin

# Copy application code
WORKDIR /app
COPY . .

# Run the application
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
