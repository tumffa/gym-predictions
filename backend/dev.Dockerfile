FROM python:3.10

# Set the working directory
WORKDIR /app

# Poetry configuration files
COPY pyproject.toml poetry.lock* ./

# Install Poetry and dependencies
RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy the source code
COPY ./ ./

ENV FLASK_APP=src/main:app
ENV FLASK_ENV=development

# Expose the Flask backend port
EXPOSE 3000

# Run Flask with live reloading
CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0", "--port=3000"]