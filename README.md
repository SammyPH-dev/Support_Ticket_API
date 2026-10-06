# Support Ticket API

API REST permettant de gérer des demandes de soutien informatique.

Le projet comprend :

- une API développée avec Flask;
- une base de données SQLite;
- une architecture modèle, DAO, service et routes;
- une authentification JWT;
- un client console Python;
- des tests automatisés avec pytest;
- une configuration Docker.

## Fonctionnalités

L'application permet de :

- s'authentifier;
- créer un ticket;
- consulter tous les tickets;
- consulter un ticket par son identifiant;
- modifier certains champs d'un ticket;
- supprimer un ticket.

## Technologies

- Python 3.14
- Flask
- Flask-SQLAlchemy
- Flask-JWT-Extended
- SQLite
- Requests
- Pytest
- Docker

## Structure du projet

```text
Support_Ticket_API/
├── app/
│   ├── api/
│   │   ├── authen_route.py
│   │   ├── sante_route.py
│   │   └── ticket_route.py
│   ├── dao/
│   │   └── ticket_dao.py
│   ├── models/
│   │   └── ticket.py
│   ├── services/
│   │   └── ticket_service.py
│   └── __init__.py
├── client/
│   └── client_console.py
├── tests/
│   ├── conftest.py
│   └── test_routes.py
├── data/
├── Dockerfile
├── requirements.txt
├── main.py
└── README.md
```

## Installation locale

### macOS et Linux

Créer et activer un environnement virtuel :

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Installer les dépendances :

```bash
python -m pip install -r requirements.txt
```

Démarrer l'API :

```bash
python main.py
```

### Windows avec PowerShell

Créer et activer un environnement virtuel :

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

Si PowerShell refuse l'activation des scripts, autoriser temporairement leur exécution dans la fenêtre actuelle :

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

Installer les dépendances :

```powershell
py -m pip install -r requirements.txt
```

Démarrer l'API :

```powershell
py main.py
```

### Windows avec l'invite de commandes

```bat
py -m venv .venv
.venv\Scripts\activate.bat
py -m pip install -r requirements.txt
py main.py
```

L'API locale est accessible à l'adresse suivante sur tous les systèmes :

```text
http://127.0.0.1:5000
```

## Authentification

Compte de démonstration :

```text
Utilisateur : admin
Mot de passe : secret
```

### Obtenir un jeton

```http
POST /authentification
Content-Type: application/json
```

Corps de la requête :

```json
{
  "utilisateur": "admin",
  "mot_de_passe": "secret"
}
```

Exemple de réponse :

```json
{
  "jeton": "<jeton-jwt>"
}
```

Les routes de gestion des tickets nécessitent ensuite cet en-tête :

```http
Authorization: Bearer <jeton-jwt>
```

## Modèle d'un ticket

```json
{
  "id": 1,
  "titre": "Écran défectueux",
  "description": "L'écran du poste 14 ne s'allume plus.",
  "priorite": "HAUTE",
  "statut": "OUVERT",
  "date_creation": "2026-10-05T14:30:00"
}
```

Priorités acceptées :

```text
BASSE
MOYENNE
HAUTE
```

Statuts acceptés :

```text
OUVERT
EN_COURS
RESOLU
```

## Routes

| Méthode | Route | Description | Authentification |
|---|---|---|---|
| GET | `/sante` | Vérifier la disponibilité de l'API | Non |
| POST | `/authentification` | Obtenir un jeton JWT | Non |
| POST | `/ticket` | Créer un ticket | Oui |
| GET | `/ticket` | Obtenir tous les tickets | Oui |
| GET | `/ticket/{id}` | Obtenir un ticket | Oui |
| PUT | `/ticket/{id}` | Modifier certains champs | Oui |
| DELETE | `/ticket/{id}` | Supprimer un ticket | Oui |

## Créer un ticket

```http
POST /ticket
Authorization: Bearer <jeton-jwt>
Content-Type: application/json
```

```json
{
  "titre": "Connexion réseau interrompue",
  "description": "La salle 204 ne peut plus accéder au réseau.",
  "priorite": "HAUTE"
}
```

Le serveur attribue automatiquement l'identifiant, le statut `OUVERT` et la date de création. Une création réussie retourne le statut HTTP `201`.

## Consulter les tickets

Tous les tickets :

```http
GET /ticket
Authorization: Bearer <jeton-jwt>
```

Un ticket particulier :

```http
GET /ticket/1
Authorization: Bearer <jeton-jwt>
```

## Modifier un ticket

Dans ce projet, la route PUT effectue une modification partielle. Seuls les champs fournis sont modifiés.

```http
PUT /ticket/1
Authorization: Bearer <jeton-jwt>
Content-Type: application/json
```

```json
{
  "priorite": "MOYENNE",
  "statut": "EN_COURS"
}
```

Les champs modifiables sont `titre`, `description`, `priorite` et `statut`.

## Supprimer un ticket

```http
DELETE /ticket/1
Authorization: Bearer <jeton-jwt>
```

Une suppression réussie retourne le ticket supprimé avec le statut HTTP `200`.

## Codes HTTP

| Code | Signification |
|---|---|
| 200 | Requête réussie |
| 201 | Ticket créé |
| 400 | Données JSON absentes ou invalides |
| 401 | Authentification absente ou invalide |
| 404 | Ticket inexistant |
| 500 | Erreur interne du serveur |

## Tests automatisés

Les tests utilisent une base de données temporaire et ne modifient pas la base de développement.

Sur macOS ou Linux :

```bash
python -m pytest -v
```

Sur Windows :

```powershell
py -m pytest -v
```

Les tests couvrent la route de santé, l'authentification, la protection JWT, le CRUD, la validation et les ressources inexistantes.

## Client console

Démarrer l'API avant le client.

Sur macOS ou Linux :

```bash
python client/client_console.py
```

Sur Windows :

```powershell
py client\client_console.py
```

Le menu permet d'effectuer toutes les opérations CRUD. La constante `URL_API` dans `client/client_console.py` doit correspondre au port utilisé par l'API :

```python
# API locale
URL_API = "http://127.0.0.1:5000"

# API exécutée dans Docker selon la configuration ci-dessous
URL_API = "http://127.0.0.1:5001"
```

## Docker

Docker Desktop doit être installé et démarré sur macOS ou Windows. Sous Linux, Docker Engine peut être utilisé.

Construire l'image sur tous les systèmes :

```bash
docker build -t support-ticket-api .
```

### Démarrage sur macOS ou Linux

```bash
docker run --name support-ticket-api-container \
  -p 5001:5000 \
  support-ticket-api
```

### Démarrage avec Windows PowerShell

```powershell
docker run --name support-ticket-api-container `
  -p 5001:5000 `
  support-ticket-api
```

### Démarrage avec l'invite de commandes Windows

```bat
docker run --name support-ticket-api-container ^
  -p 5001:5000 ^
  support-ticket-api
```

L'API Docker est accessible à l'adresse :

```text
http://127.0.0.1:5001
```

Sur certains ordinateurs macOS, AirPlay Receiver utilise déjà le port `5000` de l'ordinateur. Le mappage `5001:5000` évite ce conflit. Il fonctionne également sur Windows et Linux.

Arrêter le conteneur :

```bash
docker stop support-ticket-api-container
```

Redémarrer le conteneur existant :

```bash
docker start -a support-ticket-api-container
```

## Remarques de sécurité

Le compte administrateur et la clé JWT sont codés directement dans le projet uniquement à des fins pédagogiques.

Dans un environnement de production, il faudrait :

- stocker la clé JWT dans une variable d'environnement;
- stocker les mots de passe sous forme hachée;
- utiliser HTTPS;
- ajouter une gestion des utilisateurs;
- appliquer une limite de requêtes;
- utiliser un serveur de production plutôt que le serveur Flask intégré.
