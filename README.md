# 🌍 Pokédex Weather API + DevOps Observability (Dev & Prod)

Une API développée avec **FastAPI** combinant un **Pokédex** et la météo en temps réel via **OpenWeather**.  
Chaque Pokémon peut avoir une **faiblesse météo** selon son type et les conditions climatiques actuelles de sa ville.

Cette version intègre une **stack DevOps complète** avec des environnements **DEV** et **PROD**, une surveillance via **Prometheus**, **Grafana** et des **exporters** (Redis + PostgreSQL).

---

## 🚀 Fonctionnalités principales
- 📌 CRUD complet sur les Pokémon (ajout, modification, suppression, lecture)
- 🌦️ Détermination automatique de la **faiblesse météo**
  - 🔥 Feu → faible s’il pleut ☔
  - 💧 Eau → faible s’il neige ❄️
  - ⚡ Électrique → faible en cas d’orage ⛈️
  - 🐾 Normal → aucune faiblesse météo
- ⚡ Cache météo intelligent avec **Redis**
- 🐘 Persistance des données avec **PostgreSQL**
- 📊 Monitoring complet via **Prometheus** et **Grafana**

---

## ⚙️ Architecture & profils Docker

### 🧱 Images Docker Hub
| Environnement | Image Docker Hub | Port exposé | Description |
|----------------|------------------|--------------|--------------|
| 🧑‍💻 Dev | `katiadje/pokedex_api:dev` | `8000` | Contient le hot reload et les volumes montés |
| 🚀 Prod | `katiadje/pokedex_api:latest` | `8080` | Image optimisée pour la production (utilisateur non-root) |

---

## 🐳 Dockerfile multi-étapes
Le `Dockerfile` contient deux profils distincts :

```dockerfile
# Étape DEV
FROM base AS dev
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Étape PROD
FROM base AS prod
COPY . .
RUN useradd -m pokedexuser
USER pokedexuser
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## ⚙️ Docker Compose (Stack complète)

Le `docker-compose.yml` permet de lancer la stack complète :

- `api_dev` → mode développement avec reload
- `api_prod` → mode production sécurisé
- `postgres` → base de données PostgreSQL
- `redis` → cache
- `redis_exporter` + `postgres_exporter` → monitoring
- `prometheus` + `grafana` → observabilité

```bash
docker compose up --build
```

📍 Accès aux services :
- API Dev : [http://localhost:8000](http://localhost:8000)
- API Prod : [http://localhost:8080](http://localhost:8080)
- Prometheus : [http://localhost:9090](http://localhost:9090)
- Grafana : [http://localhost:3000](http://localhost:3000)

---

## 🧠 Prometheus + Grafana

### Prometheus
Collecte automatiquement les métriques depuis :
- `/metrics` de l’API FastAPI
- Redis Exporter (`9121`)
- PostgreSQL Exporter (`9187`)

Fichier config : `prometheus.yml`

### Grafana
Accès : [http://localhost:3000](http://localhost:3000)  
Login par défaut :
```
admin / admin
```

Ajouter une Data Source → Prometheus  
URL : `http://prometheus:9090`

Importer le dashboard FastAPI (ID **4701**).

---

## 🧩 Commandes Docker Hub

### 🔹 Construire les images
```bash
# Build Dev
docker build -t katiadje/pokedex_api:dev --target dev .

# Build Prod
docker build -t katiadje/pokedex_api:latest --target prod .
```

### 🔹 Pousser les images
```bash
docker push katiadje/pokedex_api:dev
docker push katiadje/pokedex_api:latest
```

### 🔹 Récupérer une image depuis Docker Hub
```bash
docker pull katiadje/pokedex_api:latest
```

---

## 🧪 Environnement local (optionnel)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## 📊 Technologies utilisées
- [FastAPI](https://fastapi.tiangolo.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Redis](https://redis.io/)
- [OpenWeather API](https://openweathermap.org/api)
- [Prometheus](https://prometheus.io/)
- [Grafana](https://grafana.com/)
- [Docker Compose](https://docs.docker.com/compose/)

---

## 👩‍💻 Auteur
Projet développé par **Katia** dans le cadre du Master *M2 Développement & Data *
*
