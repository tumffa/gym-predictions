FROM node:18 AS frontend

# Set working directory for frontend
WORKDIR /app/ui

# Copy frontend files
COPY ./src/ui/package.json ./src/ui/package-lock.json ./
RUN npm ci

# Build the Vite frontend
COPY ./src/ui ./
RUN npm run build

# Stage 2: Build the backend
FROM python:3.10

# Set the working directory
WORKDIR /app

# Poetry configuration files
COPY pyproject.toml poetry.lock* ./

# Install Poetry and dependencies
RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . .

# Copy built frontend from the frontend build stage
COPY --from=frontend /app/ui/build ./src/ui/build

# Expose the Flask backend port
EXPOSE 8080

# Run src/main.py
CMD ["poetry", "run", "python", "src/main.py"]