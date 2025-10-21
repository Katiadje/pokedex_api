# Étape 1 : choisir une image Python légère
FROM python:3.12-slim

# Étape 2 : définir le répertoire de travail
WORKDIR /code

# Étape 3 : installer les dépendances système minimales
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Étape 4 : copier requirements.txt et installer
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Étape 5 : copier le reste du projet
COPY . .

# Étape 6 : variables d’environnement par défaut
ENV PYTHONUNBUFFERED=1 \
    REDIS_HOST=redis \
    REDIS_PORT=6379

# Étape 7 : commande par défaut (sera surchargée par docker-compose)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
