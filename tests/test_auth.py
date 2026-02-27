from fastapi.testclient import TestClient
from app.core.config import settings

def test_login_no_user(client: TestClient):
    """
    Test que la connexion échoue sans utilisateur existant.
    """
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={"username": "test@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Email ou mot de passe incorrect"

def test_google_auth(client: TestClient):
    """
    Test de l'authentification Google simulée.
    """
    response = client.post(
        f"{settings.API_V1_STR}/auth/google",
        json={"id_token": "fake_token"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
