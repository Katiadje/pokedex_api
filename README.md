# 🌍 Pokédex Weather API

Une API développée avec **FastAPI** qui combine un **Pokédex** avec la météo en temps réel via **OpenWeather**.  
Chaque Pokémon peut avoir une **faiblesse météo** selon son type et les conditions climatiques de sa ville actuelle.

---

## 🚀 Fonctionnalités
- 📌 CRUD complet sur les Pokémon (ajout, listing, modification, suppression).
- 🌦️ Vérification de la **faiblesse météo** d’un Pokémon selon :
  - 🔥 **Feu** → faible s’il pleut ☔
  - 💧 **Eau** → faible s’il neige ❄️
  - ⚡ **Électrique** → faible en cas d’orage ⛈️
  - 🐾 **Normal** → aucune faiblesse météo
- ⚡ Cache des résultats météo avec **Redis** pour de meilleures performances.

---

## 📂 Structure du projet
```
pokedex_api/
 ├── app/
 │   ├── main.py          # Point d'entrée FastAPI (routes)
 │   ├── database.py      # Connexion à SQLite (SQLAlchemy)
 │   ├── models.py        # Modèles SQLAlchemy (Pokemon)
 │   ├── schemas.py       # Schémas Pydantic (entrée/sortie)
 │   ├── deps.py          # Gestion du cache Redis
 │   ├── weather.py       # Intégration OpenWeather API
 │   └── crud.py          # Fonctions CRUD centralisées
 │
 ├── tests/               # Tests unitaires et d’intégration
 │   ├── test_pokemon.py
 │
 ├── Dockerfile           # Image Docker pour l’API
 ├── docker-compose.yml   # Stack complète (API + Redis)
 ├── requirements.txt     # Dépendances Python
 ├── pokemons.json        # Données initiales (exemple)
 ├── pokedex.db           # Base SQLite (dev/test)
 ├── .env                 # Variables d’environnement (clé OpenWeather)
 ├── .gitignore           # Fichiers ignorés par Git
 ├── pytest.ini           # Config pytest
 └── README.md            # Documentation
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
# Linux/Mac
source .venv/bin/activate
# Windows PowerShell
.venv\Scripts\activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configurer les variables d’environnement
Créer un fichier `.env` à la racine :
```
OPENWEATHER_API_KEY=ta_cle_api_openweather
```

---

## ▶️ Lancer l’API

### Avec Uvicorn (local)
```bash
uvicorn app.main:app --reload
```
👉 API disponible sur : [http://127.0.0.1:8000](http://127.0.0.1:8000)

### Avec Docker
```bash
docker-compose up --build
```

---

## 🔥 Exemple d’utilisation

### 1. Créer un Pokémon
```bash
curl -X POST "http://127.0.0.1:8000/pokemon"      -H "Content-Type: application/json"      -d '{"name":"Charmander","type_primary":"fire","type_secondary":"flying"}'
```

### 2. Vérifier la faiblesse météo (ex: Londres 🌧️)
```bash
curl "http://127.0.0.1:8000/pokemon/1?city=London"
```

### 3. Lister les Pokémon
```bash
curl "http://127.0.0.1:8000/pokemon"
```

### 4. Mise à jour (PATCH)
```bash
curl -X PATCH "http://127.0.0.1:8000/pokemon/1"      -H "Content-Type: application/json"      -d '{"type_secondary":"dragon"}'
```

### 5. Suppression
```bash
curl -X DELETE "http://127.0.0.1:8000/pokemon/1"
```

---

## ✅ Exemple de réponse JSON
```json
{
  "id": 1,
  "name": "Charmander",
  "type_primary": "fire",
  "type_secondary": "flying",
  "weakness_due_to_weather": true,
  "weather_summary": "id=500, desc=light rain"
}
```

---

## 🛠️ Technologies
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [Redis](https://redis.io/)
- [OpenWeather API](https://openweathermap.org/api)
- [Docker](https://www.docker.com/)

---

## 👩‍💻 Auteur
Projet développé par **Katia** dans le cadre du Master *M2 Développement & Data *.
