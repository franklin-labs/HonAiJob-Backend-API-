from fastapi.testclient import TestClient
from app.core.config import settings

def test_create_cv_unauthorized(client: TestClient):
    """
    Test que la création d'un CV sans token JWT échoue.
    """
    response = client.post(
        f"{settings.API_V1_STR}/cvs/",
        json={"title": "Mon CV", "content": "Contenu du CV", "user_id": 1}
    )
    assert response.status_code == 401

def test_get_cvs_unauthorized(client: TestClient):
    """
    Test que la récupération des CV sans token JWT échoue.
    """
    response = client.get(f"{settings.API_V1_STR}/cvs/")
    assert response.status_code == 401
