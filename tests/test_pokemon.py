import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

client = TestClient(app)


@pytest.fixture(autouse=True, scope="function")
def setup_db():
    # Reset DB tables avant chaque test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


class TestPokemonCRUD:
    def test_create_and_conflict(self):
        payload = {"name": "Pikachu", "type_primary": "electric"}
        r1 = client.post("/pokemon", json=payload)
        assert r1.status_code == 201
        r2 = client.post("/pokemon", json=payload)
        assert r2.status_code == 409

    def test_patch_pokemon_name(self):
        r = client.post("/pokemon", json={"name": "Eevee", "type_primary": "normal"})
        poke_id = r.json()["id"]

        r = client.patch(f"/pokemon/{poke_id}", json={"name": "Evoli"})
        assert r.status_code == 200
        assert r.json()["name"] == "Evoli"

    def test_delete_pokemon(self):
        r = client.post("/pokemon", json={"name": "Charmander", "type_primary": "fire"})
        poke_id = r.json()["id"]

        r = client.delete(f"/pokemon/{poke_id}")
        assert r.status_code == 204

        r = client.get(f"/pokemon/{poke_id}?city=Paris")
        assert r.status_code == 404


class TestPokemonWeather:
    def test_fire_pokemon_weak_to_rain(self, monkeypatch):
        r = client.post("/pokemon", json={"name": "Salameche", "type_primary": "fire"})
        poke_id = r.json()["id"]

        # Mock geocode_city to return fake coordinates
        async def fake_geocode(city):
            return 48.8566, 2.3522  # Paris coordinates

        # Mock fetch_weather to return rainy weather (code 500)
        async def fake_weather(lat, lon, rds):
            return {"weather": [{"id": 500, "description": "pluie légère"}]}

        # Patch in the main module where the functions are imported and used
        from app import main
        monkeypatch.setattr(main, "geocode_city", fake_geocode)
        monkeypatch.setattr(main, "fetch_weather", fake_weather)

        r = client.get(f"/pokemon/{poke_id}?city=Paris")
        data = r.json()
        assert data["weakness_due_to_weather"] is True
