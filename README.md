# 🌍 Pokédex Weather API + DevOps Observability

Une API développée avec **FastAPI** qui combine un **Pokédex** avec la météo en temps réel via **OpenWeather**.  
Chaque Pokémon peut avoir une **faiblesse météo** selon son type et les conditions climatiques de sa ville actuelle.

Cette version inclut désormais une **stack DevOps complète** avec **Prometheus**, **Grafana** et des **exporters** pour surveiller l’état de l’API, de Redis et de PostgreSQL.

---

## 🚀 Fonctionnalités
- 📌 CRUD complet sur les Pokémon (ajout, listing, modification, suppression).
- 🌦️ Vérification de la **faiblesse météo** d’un Pokémon selon :
  - 🔥 **Feu** → faible s’il pleut ☔
  - 💧 **Eau** → faible s’il neige ❄️
  - ⚡ **Électrique** → faible en cas d’orage ⛈️
  - 🐾 **Normal** → aucune faiblesse météo
- ⚡ Cache météo avec **Redis** pour optimiser les appels API.
- 📊 **Monitoring complet** (Prometheus + Grafana + Exporters).

---

## 📂 Structure du projet
```
pokedex_api/
 ├── app/
 │   ├── main.py          # Point d’entrée FastAPI (routes + instrumentation Prometheus)
 │   ├── database.py      # Connexion PostgreSQL (SQLAlchemy)
 │   ├── models.py        # Modèles SQLAlchemy (Pokemon)
 │   ├── schemas.py       # Schémas Pydantic (entrée/sortie)
 │   ├── deps.py          # Gestion du cache Redis
 │   ├── weather.py       # Intégration OpenWeather API
 │
 ├── prometheus.yml       # Configuration Prometheus
 ├── docker-compose.yml   # Stack complète (API + Redis + Postgres + Monitoring)
 ├── Dockerfile           # Image Docker de l’API
 ├── requirements.txt     # Dépendances Python
 ├── .env                 # Variables d’environnement
 ├── tests/               # Tests unitaires et d’intégration
 └── README.md
```

---

## ⚙️ Installation

### 1. Cloner le projet
```bash
git clone https://github.com/Katiadje/pokedex_api.git
cd pokedex_api
```

### 2. Créer un environnement virtuel
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate    # Windows PowerShell
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configurer les variables d’environnement (.env)
```
OPENWEATHER_API_KEY=ta_cle_api_openweather
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
POSTGRES_DB=pokedex
```

---

## ▶️ Lancer l’application

### 🔹 En local (Uvicorn)
```bash
uvicorn app.main:app --reload
```
API disponible sur : [http://127.0.0.1:8000](http://127.0.0.1:8000)

### 🔹 En mode conteneur (Docker Compose)
```bash
docker compose up --build
```
Les services suivants seront lancés :
- 🐍 API FastAPI (`localhost:8000`)
- 🧠 Redis cache (`localhost:6379`)
- 🐘 PostgreSQL (`localhost:5432`)
- 📈 Prometheus (`localhost:9090`)
- 📊 Grafana (`localhost:3000`)

---

## 📊 Observabilité (DevOps)

### 1️⃣ Prometheus
Prometheus collecte les métriques depuis :
- `/metrics` de l’API FastAPI  
- Redis Exporter (port `9121`)  
- Postgres Exporter (port `9187`)

Fichier de config : `prometheus.yml`

### 2️⃣ Grafana
Interface de visualisation accessible sur [http://localhost:3000](http://localhost:3000)  
Login par défaut :
```
User: admin
Pass: admin
```
➡️ Ajouter Prometheus comme **Data Source** :  
URL : `http://prometheus:9090`

➡️ Importer le dashboard FastAPI :  
**Dashboards → Import → ID: 4701**

---

## 🛠️ Technologies
- [FastAPI](https://fastapi.tiangolo.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Redis](https://redis.io/)
- [OpenWeather API](https://openweathermap.org/api)
- [Prometheus](https://prometheus.io/)
- [Grafana](https://grafana.com/)
- [Docker Compose](https://docs.docker.com/compose/)

---

## 👩‍💻 Auteur
Projet développé par **Katia**  
🎓 Master 2 Développement & Data

