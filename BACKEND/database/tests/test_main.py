"""
fichier : test_main.py
auteur  : Jeremy Genereux - genj2110
          Benjamin Carignan - carb1101
date    : oct. 2024
projet  : CORE
description : Fichier de tests unitaires pour le backend FastAPI.
"""
from fastapi.testclient import TestClient
from app.main import app
import pytest

# Créer une instance de TestClient pour interagir avec l'application FastAPI
client = TestClient(app)

# Test pour la création d'un joueur avec succès
def test_create_player():
    response = client.post("/players/", json={
        "first_name": "Jeremy",
        "last_name": "Genereux",
        "email": "jeremy.genereux@example.com",
        "numero": 18
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "jeremy.genereux@example.com"
    assert data["first_name"] == "Jeremy"
    assert data["numero"] == 18

# Test pour la gestion d'une erreur d'email en double
def test_create_player_duplicate_email():
    client.post("/players/", json={
        "first_name": "Benjamin",
        "last_name": "Carignan",
        "email": "benjamin.carignan@example.com",
        "numero": 10
    })
    response = client.post("/players/", json={
        "first_name": "Benjamin",
        "last_name": "Carignan",
        "email": "benjamin.carignan@example.com",
        "numero": 10
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

# Test pour récupérer la liste des joueurs
def test_read_players():
    response = client.get("/players/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0  # En supposant qu'il y a des joueurs créés

# Test pour lire un joueur spécifique par ID
def test_read_player():
    # Créer un joueur d'abord pour tester sa lecture
    player_response = client.post("/players/", json={
        "first_name": "Jeremy",
        "last_name": "Genereux",
        "email": "jeremy.genereux@example.com",
        "numero": 18
    })
    player_id = player_response.json()["id"]

    # Maintenant, lire le joueur par son ID
    response = client.get(f"/players/{player_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "jeremy.genereux@example.com"
    assert data["id"] == player_id

# Test pour lire un joueur inexistant (erreur 404)
def test_read_non_existent_player():
    response = client.get("/players/9999999")  # Joueur inexistant
    assert response.status_code == 404
    assert response.json()["detail"] == "Player not found"