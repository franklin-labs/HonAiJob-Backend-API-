# Compétences de l'Agent Orchestrateur (OrchestratorAgent)

Cet agent est le chef d'orchestre propulsé par **Llama-3.3-70b-versatile** de Groq.

## Compétences principales
- **Délégation Intelligente** : Analyse l'intention de l'utilisateur pour activer l'agent expert correspondant.
- **Apprentissage Persistant** : Apprend de l'historique et des spécificités du projet en cours via le stockage SQL.
- **Synthèse de Haut Niveau** : Combine les sorties de plusieurs agents pour une réponse claire et synthétisée.
- **Routage Dynamique** : Capacité à ajuster les tâches en cours de route pour plus de fiabilité.

## Outils utilisés
- **Bus d'événements Agno (Phi)** : Coordination et partage d'informations inter-agents.
- **SqliteAgentStorage** : Maintien du contexte de session et de projet.
- **Groq Llama-3.3-70b-versatile** : Pour une orchestration logique et sans faille.
