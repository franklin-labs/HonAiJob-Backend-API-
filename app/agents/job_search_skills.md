# Compétences de l'Agent de Recherche d'Offres (JobSearchAgent)

Cet agent est propulsé par **Llama-3.1-8b-instant** de Groq pour une réactivité maximale (560 T/sec).

## Compétences principales
- **Recherche multicritères (DuckDuckGo)** : Cible les offres par contrat (CDI, Freelance, Stage), expérience et localisation via des filtres de recherche avancés.
- **Sourcing ciblés (Linkedin, Indeed, Welcome to the Jungle)** : Utilise des modificateurs de recherche `site:` pour isoler les plateformes de recrutement majeures.
- **Vérification de fraîcheur (< 15j)** : Identifie et ne retient que les opportunités publiées récemment.
- **Veille par entreprise (Wikipedia)** : Récupère des informations sur la notoriété et le secteur d'activité des entreprises repérées.

## Outils utilisés
- **DuckDuckGo** : Recherche web et actualités (News) pour les offres récentes.
- **WikipediaTools** : Enrichissement des données sur les entreprises recruteuses.
- **Groq Llama-3.1-8b-instant** : Pour un traitement instantané des requêtes de recherche.
