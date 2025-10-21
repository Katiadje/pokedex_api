# 🌍 Pokédex + Weather API

Une API FastAPI qui combine un **Pokédex** avec la météo en temps réel grâce à **OpenWeather**.  
Chaque Pokémon peut avoir une **faiblesse météo** en fonction de sa ville actuelle.

---

## 🚀 Fonctionnalités
- Ajouter, lister, mettre à jour et supprimer des Pokémon (CRUD).
- Vérifier la **faiblesse météo** d’un Pokémon selon son type et la météo réelle dans une ville donnée :
  - 🔥 **Feu** → faible s’il pleut ☔
  - 💧 **Eau** → faible s’il neige ❄️
  - ⚡ **Électrique** → faible s’il y a un orage ⛈️
  - 🐾 **Normal** → pas de faiblesse météo

---

## 📂 Structure du projet
```
app/
 ├── main.py        # Routes FastAPI (CRUD + météo)
 ├── database.py    # Connexion à SQLite avec SQLAlchemy
 ├── models.py      # Modèle Pokemon
 ├── schemas.py     # Schémas Pydantic (entrée/sortie)
 ├── deps.py        # Redis (cache)
 ├── weather.py     # Intégration OpenWeather API
```

---

## ⚙️ Installation

### 1. Cloner le projet
```bash
git clone https://github.com/Katiadje/pokedex-weather.git
cd pokedex-weather
```

### 2. Créer un environnement virtuel
```bash
python3 -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate    # Windows PowerShell
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Créer un fichier `.env`
Dans la racine du projet, ajoute un fichier `.env` :

```
OPENWEATHER_API_KEY=ta_cle_api_openweather
```

---

## ▶️ Lancer l’API
```bash
uvicorn app.main:app --reload
```

Par défaut, l’API tourne sur :  
👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🔥 Exemple d’utilisation

### 1. Créer un Pokémon
```bash
curl -X POST "http://127.0.0.1:8000/pokemon" \
     -H "Content-Type: application/json" \
     -d '{"name":"Charmander","type_primary":"fire","type_secondary":"flying"}'
```

### 2. Vérifier sa faiblesse météo (ex: Londres 🌧️)
```bash
curl "http://127.0.0.1:8000/pokemon/1?city=London"
```

### 3. Liste des Pokémon
```bash
curl "http://127.0.0.1:8000/pokemon"
```

### 4. Mise à jour partielle (PATCH)
```bash
curl -X PATCH "http://127.0.0.1:8000/pokemon/1" \
     -H "Content-Type: application/json" \
     -d '{"type_secondary":"dragon"}'
```

### 5. Suppression
```bash
curl -X DELETE "http://127.0.0.1:8000/pokemon/1"
```

---

## ✅ Exemple de résultat
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

---

## 👩‍💻 Auteur
Projet développé par **Katia** dans le cadre du cours *M2 Dev Web*.  
