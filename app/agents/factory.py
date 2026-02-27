from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGo
from agno.tools.wikipedia import WikipediaTools
from agno.memory import AgentMemory
from agno.storage.agent.sqlite import SqliteAgentStorage
from app.core.config import settings
from typing import List, Optional
import groq

# Import des prompts
from app.agents.prompts.orchestrator_prompt import ORCHESTRATOR_SYSTEM_PROMPT
from app.agents.prompts.auth_prompt import AUTH_SYSTEM_PROMPT
from app.agents.prompts.task_prompt import TASK_SYSTEM_PROMPT
from app.agents.prompts.analysis_prompt import ANALYSIS_SYSTEM_PROMPT
from app.agents.prompts.job_search_prompt import JOB_SEARCH_SYSTEM_PROMPT
from app.agents.prompts.notification_prompt import NOTIFICATION_SYSTEM_PROMPT
from app.agents.prompts.verifier_prompt import VERIFIER_SYSTEM_PROMPT

# Configuration du stockage pour la mémoire (apprentissage par projet)
agent_storage = SqliteAgentStorage(table_name="agent_memory", db_file="agents_storage.db")

def handle_groq_error(e: Exception) -> str:
    """
    Formate les erreurs Groq de manière conviviale pour l'utilisateur, 
    notamment les limites de taux (Rate Limits).
    """
    error_msg = str(e)
    if "rate_limit_exceeded" in error_msg or "429" in error_msg:
        return "Désolé, vous avez atteint la limite de requêtes de votre clé Groq. Veuillez patienter un moment ou vérifier votre quota sur groq.com."
    if "invalid_api_key" in error_msg or "401" in error_msg:
        return "Clé API Groq invalide. Veuillez vérifier votre configuration dans les paramètres."
    return f"Une erreur est survenue avec Groq : {error_msg}"

def get_model(model_id: str, user_api_key: Optional[str] = None):
    """
    Initialise le modèle Groq avec la clé API de l'utilisateur ou celle par défaut.
    """
    api_key = user_api_key or settings.GROQ_API_KEY
    return Groq(id=model_id, api_key=api_key)

def get_auth_agent(user_api_key: Optional[str] = None) -> Agent:
    return Agent(
        name="AuthAgent",
        model=get_model("llama-3.1-8b-instant", user_api_key),
        description="Expert en sécurité et gestion des identités",
        instructions=[AUTH_SYSTEM_PROMPT],
    )

def get_task_agent(session_id: Optional[str] = None, user_api_key: Optional[str] = None) -> Agent:
    return Agent(
        name="TaskAgent",
        model=get_model("llama-3.1-8b-instant", user_api_key),
        description="Gestionnaire de projet et d'organisation personnelle",
        instructions=[TASK_SYSTEM_PROMPT],
        storage=agent_storage,
        add_history_to_messages=True,
        session_id=session_id,
    )

def get_analysis_agent(session_id: Optional[str] = None, user_api_key: Optional[str] = None) -> Agent:
    return Agent(
        name="AnalysisAgent",
        model=get_model("llama-3.3-70b-versatile", user_api_key), # Production model
        description="Analyste RH expert en CV et matching de postes",
        instructions=[ANALYSIS_SYSTEM_PROMPT],
        storage=agent_storage,
        add_history_to_messages=True,
        session_id=session_id,
    )

def get_job_search_agent(session_id: Optional[str] = None, user_api_key: Optional[str] = None) -> Agent:
    return Agent(
        name="JobSearchAgent",
        model=get_model("llama-3.1-8b-instant", user_api_key),
        tools=[
            DuckDuckGo(
                search=True, 
                news=True, 
                modifier="site:linkedin.com/jobs OR site:indeed.com OR site:welcometothejungle.com"
            ),
            WikipediaTools()
        ],
        description="Chasseur de tête ultra-optimisé pour les sites d'emploi",
        instructions=[
            JOB_SEARCH_SYSTEM_PROMPT,
            "Tu dois impérativement te concentrer sur des offres réelles publiées il y a moins de 15 jours.",
            "Utilise les filtres de recherche DuckDuckGo pour cibler LinkedIn, Indeed et Welcome to the Jungle.",
            "Si aucun résultat n'est trouvé sur ces sites, élargis ta recherche mais vérifie scrupuleusement la date.",
            "Apprends des préférences du projet actuel de l'utilisateur."
        ],
        storage=agent_storage,
        add_history_to_messages=True,
        session_id=session_id,
        show_tool_calls=True
    )

def get_notification_agent(user_api_key: Optional[str] = None) -> Agent:
    return Agent(
        name="NotificationAgent",
        model=get_model("llama-3.1-8b-instant", user_api_key),
        description="Responsable de la communication et des alertes",
        instructions=[NOTIFICATION_SYSTEM_PROMPT],
    )

def get_verifier_agent(user_api_key: Optional[str] = None) -> Agent:
    return Agent(
        name="VerifierAgent",
        model=get_model("llama-3.3-70b-versatile", user_api_key), # Production model (Quality)
        tools=[DuckDuckGo(search=True)],
        description="Expert en validation et contrôle qualité anti-hallucination",
        instructions=[
            VERIFIER_SYSTEM_PROMPT,
            "Ta mission est d'éliminer TOUTE hallucination d'offre d'emploi.",
            "Vérifie chaque URL fournie par le JobSearchAgent.",
            "Si une offre semble suspecte ou périmée, rejette-la sans hésitation."
        ],
    )

def get_orchestrator_agent(team: List[Agent], session_id: Optional[str] = None, user_api_key: Optional[str] = None) -> Agent:
    return Agent(
        name="OrchestratorAgent",
        model=get_model("llama-3.3-70b-versatile", user_api_key), # Production model (Logic)
        team=team,
        description="Chef d'orchestre capable d'apprendre du contexte utilisateur",
        instructions=[
            ORCHESTRATOR_SYSTEM_PROMPT,
            "Tu dois TOUJOURS prendre en compte l'historique et les spécificités du projet actif de l'utilisateur.",
            "L'apprentissage est activé via le stockage persistant."
        ],
        storage=agent_storage,
        add_history_to_messages=True,
        session_id=session_id,
        markdown=True
    )

def get_full_agent_team(project_id: Optional[int] = None, user_api_key: Optional[str] = None) -> Agent:
    """
    Retourne l'agent orchestrateur avec une mémoire liée au projet et la clé API de l'utilisateur.
    """
    session_id = f"project_{project_id}" if project_id else "global_session"
    
    team = [
        get_auth_agent(user_api_key),
        get_task_agent(session_id=session_id, user_api_key=user_api_key),
        get_analysis_agent(session_id=session_id, user_api_key=user_api_key),
        get_job_search_agent(session_id=session_id, user_api_key=user_api_key),
        get_notification_agent(user_api_key),
        get_verifier_agent(user_api_key)
    ]
    return get_orchestrator_agent(team, session_id=session_id, user_api_key=user_api_key)
