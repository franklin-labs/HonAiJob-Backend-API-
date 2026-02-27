# Architecture Multi-Agents HonaiJob (Propulsée par Groq)

L'architecture multi-agents de HonaiJob repose sur le framework **Agno (Phi)** et l'infrastructure **Groq**, organisée autour d'un **Agent Orchestrateur** central qui délègue les tâches à des agents spécialisés.

## L'Équipe d'Agents & Modèles Groq

Nous utilisons un système **multi-modèles** pour équilibrer intelligence, qualité et rapidité :

- **Llama-3.3-70b-versatile** : Pour les tâches de haute réflexion (Orchestration, Analyse, Vérification).
- **Llama-3.1-8b-instant** : Pour les tâches nécessitant une réponse ultra-rapide (Recherche, Tâches, Notifications).

### 1. Agent Orchestrateur (OrchestratorAgent)
- **Modèle** : `llama-3.3-70b-versatile`
- **Rôle** : Chef d'orchestre et interface principale.
- **Capacités** : 
  - Analyse l'intention et décompose les demandes complexes.
  - **Mémoire Persistante** : Apprend des préférences de l'utilisateur par projet (Sqlite Storage).

### 2. Agent de Recherche d'Offres (JobSearchAgent)
- **Modèle** : `llama-3.1-8b-instant` (Vitesse pure)
- **Outils** : DuckDuckGo (LinkedIn, Indeed, Welcome to the Jungle), Wikipedia.
- **Responsabilités** : Sourcing d'opportunités réelles avec filtres de date stricts (< 15j).

### 3. Agent de Vérification (VerifierAgent)
- **Modèle** : `llama-3.3-70b-versatile` (Qualité)
- **Outils** : DuckDuckGo (Vérification d'URL).
- **Responsabilités** : Élimine les hallucinations et valide l'existence réelle des offres d'emploi.

### 4. Agent d'Analyse (AnalysisAgent)
- **Modèle** : `llama-3.3-70b-versatile`
- **Responsabilités** : Extraction de compétences CV et calcul de score de matching prédictif.

### 5. Agents de Soutien (Auth, Task, Notification)
- **Modèle** : `llama-3.1-8b-instant`
- **Responsabilités** : Gestion de session, rappels de candidatures et alertes en temps réel.

## Système de Mémoire & Apprentissage

Chaque agent dispose d'une mémoire via `SqliteAgentStorage`. La mémoire est segmentée par `project_id`, permettant à l'IA d'apprendre les spécificités de chaque recherche de l'utilisateur (ex: préférence pour le télétravail, secteurs d'activité favoris).

## Workflows & Fiabilité (99.99%)

Le système utilise des **Workflows Agno** pour garantir des résultats fiables :

1. **Phase de Recherche** : Le `JobSearchAgent` collecte des offres via DuckDuckGo News et les sites spécialisés.
2. **Phase de Validation** : Le `VerifierAgent` prend chaque offre, tente de charger l'URL ou de croiser les informations pour confirmer qu'elle n'est pas périmée ou fictive.
3. **Phase de Livraison** : Seules les offres ayant passé le test de fiabilité sont affichées au client.

## Gestion des Limites (Rate Limits)

En cas de saturation de la clé API Groq de l'utilisateur, le système intercepte l'erreur via un middleware dédié et renvoie une notification formatée invitant l'utilisateur à patienter ou à vérifier son quota.

## Protocoles de Communication

Les agents communiquent via le bus d'événements interne d'Agno. L'orchestrateur maintient le contexte de la session utilisateur et le transmet aux agents lors de la délégation.
