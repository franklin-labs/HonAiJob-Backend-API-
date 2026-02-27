import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

def test_agent_chat(client: TestClient, normal_user_token_headers: dict):
    with patch("app.agents.factory.get_full_agent_team") as mock_team:
        mock_agent = MagicMock()
        mock_response = MagicMock()
        mock_response.content = "Bonjour, je suis votre assistant."
        mock_agent.run.return_value = mock_response
        mock_team.return_value = mock_agent
        
        response = client.post(
            "/api/v1/agents/chat",
            json={"message": "Bonjour"},
            headers=normal_user_token_headers
        )
        assert response.status_code == 200
        assert response.json()["response"] == "Bonjour, je suis votre assistant."

from app.agents.workflow import RunResponse, RunEvent

def test_job_search_workflow(client: TestClient, normal_user_token_headers: dict):
    with patch("app.agents.workflow.get_job_search_workflow") as mock_workflow_factory:
        mock_workflow = MagicMock()
        mock_response = RunResponse(content="Offre vérifiée: Développeur chez Google", event=RunEvent.workflow_completed)
        mock_workflow.run.return_value = [mock_response]
        mock_workflow_factory.return_value = mock_workflow
        
        response = client.post(
            "/api/v1/agents/search-jobs",
            json={"query": "développeur", "location": "Paris"},
            headers=normal_user_token_headers
        )
        assert response.status_code == 200
        assert "Offre vérifiée" in response.json()["response"]
