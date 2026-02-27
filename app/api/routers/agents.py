from fastapi import APIRouter, Depends, HTTPException, Header
from typing import Any, Optional
from app.api.deps import get_current_active_user
from app.models.sqlalchemy_user import User
from app.agents.factory import get_full_agent_team, get_job_search_agent, get_analysis_agent, handle_groq_error
from app.agents.workflow import get_job_search_workflow
from pydantic import BaseModel

router = APIRouter()

class AgentRequest(BaseModel):
    message: str
    project_id: Optional[int] = None

class JobSearchRequest(BaseModel):
    query: str
    contract_type: Optional[str] = None
    location: Optional[str] = None
    experience_level: Optional[str] = None

@router.post("/chat")
def chat_with_orchestrator(
    request: AgentRequest,
    current_user: User = Depends(get_current_active_user),
    x_groq_api_key: Optional[str] = Header(None, alias="X-Groq-Api-Key")
) -> Any:
    """
    Communique avec l'orchestrateur avec mémoire liée au projet et clé API personnalisée.
    """
    try:
        orchestrator = get_full_agent_team(
            project_id=request.project_id, 
            user_api_key=x_groq_api_key
        )
        response = orchestrator.run(request.message)
        return {"response": response.content}
    except Exception as e:
        error_msg = handle_groq_error(e)
        return {"response": error_msg, "error": True}

@router.post("/search-jobs")
def search_jobs(
    request: JobSearchRequest,
    project_id: Optional[int] = None,
    current_user: User = Depends(get_current_active_user),
    x_groq_api_key: Optional[str] = Header(None, alias="X-Groq-Api-Key")
) -> Any:
    """
    Route de recherche avec workflow multi-sources et mémoire projet.
    """
    try:
        # Note: Le workflow actuel ne supporte pas encore la clé utilisateur dynamiquement dans son init
        # On pourrait passer la clé au factory.py via le workflow
        workflow = get_job_search_workflow(project_id=project_id)
        # Injection manuelle de la clé dans les agents du workflow pour cette session
        if x_groq_api_key:
            workflow.job_search_agent.model.api_key = x_groq_api_key
            workflow.verifier_agent.model.api_key = x_groq_api_key
            
        query = f"Recherche des offres pour: {request.query}"
        if request.location:
            query += f" à {request.location}"
        if request.contract_type:
            query += f" en {request.contract_type}"
            
        responses = list(workflow.run(query))
        final_response = responses[-1] if responses else "Aucune offre vérifiée trouvée."
        return {"response": final_response.content}
    except Exception as e:
        error_msg = handle_groq_error(e)
        return {"response": error_msg, "error": True}

@router.post("/analyze-cv")
def analyze_cv(
    request: AgentRequest,
    current_user: User = Depends(get_current_active_user),
    x_groq_api_key: Optional[str] = Header(None, alias="X-Groq-Api-Key")
) -> Any:
    """
    Route spécifique pour l'analyse de CV via l'AnalysisAgent.
    """
    try:
        agent = get_analysis_agent(user_api_key=x_groq_api_key)
        response = agent.run(f"Analyse ce contenu de CV: {request.message}")
        return {"response": response.content}
    except Exception as e:
        error_msg = handle_groq_error(e)
        return {"response": error_msg, "error": True}
