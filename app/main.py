import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Pokemon
from .schemas import PokemonCreate, PokemonOut
from .deps import get_redis
from .weather import fetch_weather, is_raining_from_payload, geocode_city

# Création des tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pokedex + Weather", version="1.0.0")

# CREATE
@app.post("/pokemon", response_model=PokemonOut, status_code=201)
def create_pokemon(payload: PokemonCreate, db: Session = Depends(get_db)):
    exists = db.query(Pokemon).filter(Pokemon.name == payload.name).first()
    if exists:
        raise HTTPException(status_code=409, detail="Pokemon already exists")
    p = Pokemon(
        name=payload.name,
        type_primary=payload.type_primary.lower(),
        type_secondary=(payload.type_secondary.lower() if payload.type_secondary else None)
    )
    db.add(p)
    db.commit()
    db.refresh(p)
    return PokemonOut(
        id=p.id,
        name=p.name,
        type_primary=p.type_primary,
        type_secondary=p.type_secondary,
        weakness_due_to_weather=False,
        weather_summary=None
    )

# READ + météo/faiblesse
@app.get("/pokemon/{pokemon_id}", response_model=PokemonOut)
async def get_pokemon(
    pokemon_id: int,
    city: str = Query(..., description="Nom de la ville"),
    db: Session = Depends(get_db),
    rds = Depends(get_redis),
):
    p = db.query(Pokemon).filter(Pokemon.id == pokemon_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Pokemon not found")

    # Ville → coordonnées
    lat, lon = await geocode_city(city)

    # Météo
    weather = await fetch_weather(lat, lon, rds)
    raining, summary = is_raining_from_payload(weather)
    code = weather["weather"][0]["id"]

    weakness = False

    # 🔥 Feu → faible si pluie
    if (p.type_primary == "fire" or p.type_secondary == "fire") and (300 <= code < 600):
        weakness = True

    # 💧 Eau → faible si neige (600–699)
    if (p.type_primary == "water" or p.type_secondary == "water") and (600 <= code < 700):
        weakness = True

    # ⚡ Électrique → faible si orage (200–299)
    if (p.type_primary == "electric" or p.type_secondary == "electric") and (200 <= code < 300):
        weakness = True

    return PokemonOut(
        id=p.id,
        name=p.name,
        type_primary=p.type_primary,
        type_secondary=p.type_secondary,
        weakness_due_to_weather=weakness,
        weather_summary=summary
    )

# LIST
@app.get("/pokemon", response_model=list[PokemonOut])
def list_pokemon(db: Session = Depends(get_db)):
    rows = db.query(Pokemon).all()
    return [
        PokemonOut(
            id=r.id,
            name=r.name,
            type_primary=r.type_primary,
            type_secondary=r.type_secondary,
            weakness_due_to_weather=False,
            weather_summary=None
        )
        for r in rows
    ]

# PATCH
@app.patch("/pokemon/{pokemon_id}", response_model=PokemonOut)
def update_pokemon(pokemon_id: int, payload: dict = Body(...), db: Session = Depends(get_db)):
    p = db.query(Pokemon).filter(Pokemon.id == pokemon_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Pokemon not found")

    if "name" in payload:
        p.name = payload["name"]
    if "type_primary" in payload:
        p.type_primary = payload["type_primary"].lower()
    if "type_secondary" in payload:
        p.type_secondary = payload["type_secondary"].lower() if payload["type_secondary"] else None

    db.commit()
    db.refresh(p)
    return PokemonOut(
        id=p.id,
        name=p.name,
        type_primary=p.type_primary,
        type_secondary=p.type_secondary,
        weakness_due_to_weather=False,
        weather_summary=None
    )

# DELETE
@app.delete("/pokemon/{pokemon_id}", status_code=204)
def delete_pokemon(pokemon_id: int, db: Session = Depends(get_db)):
    p = db.query(Pokemon).filter(Pokemon.id == pokemon_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Pokemon not found")
    db.delete(p)
    db.commit()
    return None

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
