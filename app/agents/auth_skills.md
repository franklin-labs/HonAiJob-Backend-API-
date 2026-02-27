# Compétences de l'Agent d'Authentification (AuthAgent)

Cet agent est le gardien de la sécurité propulsé par **Llama-3.1-8b-instant** de Groq.

## Compétences principales
- **Gestion des Sessions** : Émission et validation des tokens JWT (Access & Refresh).
- **Protection des Données** : Assure que l'accès aux projets et CV est restreint au bon utilisateur.
- **Sécurité Google OAuth** : Intégration minimaliste pour une authentification fluide.

## Outils utilisés
- **Groq Llama-3.1-8b-instant** : Pour un traitement sécurisé et rapide des informations de session.
- **Python-Jose / Passlib** : Chiffrement et validation des tokens.
