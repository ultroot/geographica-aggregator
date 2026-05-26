# Stage 1: Base Image & Environment
FROM python:3.12-slim

# Stage 2: Security & Environment Variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_USER=geographica_user

# Stage 3: System Dependencies & User Creation
RUN groupadd -r ${APP_USER} && useradd -r -g ${APP_USER} ${APP_USER} \
    && apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Stage 4: Working Directory
WORKDIR /app

# Stage 5: Dependency Installation (Caching Layer)
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel>=0.46.2 jaraco.context>=6.1.0 \
    && pip install --no-cache-dir -r requirements.txt

# Stage 6: Application Code
COPY . .

# Stage 7: Permissions & Security
RUN chown -R ${APP_USER}:${APP_USER} /app
USER ${APP_USER}

# Stage 8: Execution
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]