from typing import Optional, Iterator
from agno.workflow import Workflow, RunResponse, RunEvent
from agno.agent import Agent
from app.agents.factory import get_job_search_agent, get_verifier_agent

class JobSearchWorkflow(Workflow):
    """
    Workflow optimisé avec mémoire par projet et multi-sources web (DuckDuckGo + Wikipedia).
    """
    
    def __init__(self, project_id: Optional[int] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        session_id = f"project_{project_id}" if project_id else "global_session"
        self.job_search_agent: Agent = get_job_search_agent(session_id=session_id)
        self.verifier_agent: Agent = get_verifier_agent()

    def run(self, query: str, **kwargs) -> Iterator[RunResponse]:
        """
        Exécute la recherche multi-sources et la validation croisée.
        """
        # Étape 1 : Recherche multi-sources (DuckDuckGo + Wikipedia)
        print(f"Étape 1 : Recherche multi-sources pour '{query}'...")
        search_prompt = (
            f"Recherche les meilleures offres d'emploi pour : {query}. "
            "Utilise Wikipedia pour obtenir des informations sur les entreprises trouvées "
            "et DuckDuckGo pour les offres récentes. "
            "Prends en compte les préférences apprises lors des sessions précédentes de ce projet."
        )
        search_response: RunResponse = self.job_search_agent.run(search_prompt)
        raw_offers = search_response.content

        # Étape 2 : Vérification croisée anti-hallucination
        print("Étape 2 : Vérification croisée et validation qualité...")
        verification_prompt = (
            "Vérifie la véracité des offres suivantes sur le web. "
            "Élimine toute offre suspecte ou expirée. "
            f"Offres à analyser :\n\n{raw_offers}"
        )
        verification_response: RunResponse = self.verifier_agent.run(verification_prompt)
        
        yield RunResponse(
            content=verification_response.content,
            event=RunEvent.workflow_completed
        )

def get_job_search_workflow(project_id: Optional[int] = None) -> JobSearchWorkflow:
    return JobSearchWorkflow(project_id=project_id)
