# Compétences de l'Agent de Vérification (VerifierAgent)

Cet agent est le gardien de la fiabilité propulsé par **Llama-3.3-70b-versatile** de Groq.

## Compétences principales
- **Anti-Hallucination** : Vérifie l'existence réelle des offres d'emploi suggérées par le JobSearchAgent.
- **Validation d'URL** : Teste la validité des liens d'offres d'emploi.
- **Contrôle Qualité** : Assure que les informations finales respectent les critères de l'utilisateur (lieu, contrat, etc.).
- **Filtrage des Fakes** : Identifie et rejette les offres suspectes ou périmées.

## Outils utilisés
- **DuckDuckGo Search** : Pour croiser les informations sur l'existence des postes.
- **Groq Llama-3.3-70b-versatile** : Pour une évaluation critique et sans concession.
- **Workflow de validation** : Intégration dans le pipeline de recherche avant livraison.
