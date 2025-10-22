# =====================================
# 🌍 Étape 1 : Base commune
# =====================================
FROM python:3.12-slim AS base

# Définir le répertoire de travail
WORKDIR /code

# Installer dépendances système minimales
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Copier requirements et installer les libs Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Variables d’environnement globales
ENV PYTHONUNBUFFERED=1 \
    REDIS_HOST=redis \
    REDIS_PORT=6379


# =====================================
# 👩‍💻 Étape 2 : Environnement DEV
# =====================================
FROM base AS dev

# Copier tout le code source (pour reload auto)
COPY . .

# Uvicorn avec rechargement automatique
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


# =====================================
# 🚀 Étape 3 : Environnement PROD
# =====================================
FROM base AS prod

# Copier uniquement le code nécessaire
COPY . .

# Créer un utilisateur non-root pour la sécurité
RUN useradd -m pokedexuser
USER pokedexuser

# Lancer sans reload pour la production
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
