# CORE - Coaching Assisted Recovery Ecosystem (Backend)
<img src="LogoCORE.svg" alt="Logo" width="200" height="200">

## Description
Backend Python de CORE permettant d'établir une connexion avec les capteurs intelligents, de traiter et stocker les données ainsi que d'envoyer au frontend en temps réel les nouvelles données.

### Contexte du Projet
CORE (Coaching Assisted Recovery Ecosystem) est une solution conçue pour optimiser la gestion de la récupération des joueurs dans des sports à haute intensité, tels que le hockey. Le projet vise à fournir aux entraîneurs des données physiologiques en temps réel, comme le rythme cardiaque et la variabilité de récupération, collectées via des capteurs connectés portés par les joueurs. 

Grâce à ces informations, les entraîneurs peuvent prendre des décisions éclairées pour optimiser les rotations, maximiser la performance de l’équipe, et minimiser le risque de fatigue excessive. CORE met l’accent sur l’interprétation rapide et fiable des données pour permettre des interventions immédiates pendant les matchs, contribuant ainsi à une stratégie de jeu dynamique et bien informée.

## Installation

### Venv
Installer une venv Python. La version 3.12 est recommanée. 

### Librairies
Les librairies requises sont spécifiées dans requirements.txt. Il est possible de les installer avec la commande suivante:
```bash
pip install -r requirements.txt
```

### Capteurs
Afin de se connecter avec les capteurs corporels openant, les étapes suivantes sont requises:

- Ajouter la dernière version de libusb https://libusb.info/ dans le dossier de l'exécutable du venv python.

- Installer les drivers libusb https://github.com/libusb/libusb/wiki/Windows#Driver_Installation, fonctionne
bien avec Zadig.

### Base de données
Le backend utilise une base de données PostgreSQL. Il est nécéssaire d'avoir téléchargé et installé PostgreSQL sur votre machine. Il est possible de télécharger PostgreSQL à l'adresse suivante: https://www.postgresql.org/download/


### Variables d'environnement
Le fichier .env.template contient la liste des variables d'environnement requises. Il est nécessaire de créer un fichier .env à la racine du projet et d'y insérer les variables d'environnement requises.

## Exécution
Voici quelques commandes utiles afin de se servir du backend. Elles doivent être exécutées depuis la racine du projet.

Pour démarrer le serveur:
```bash
python -m server.launch_server
```
Pour supprimer et créer les tables de la base de données:
```bash
python -m database.create_database
```
Pour lancer le module de connexion avec les capteurs:
```bash
python -m devices.launch_devices
```

## Dictionnaire de Données

### Table: `Coach`
- **id** (`int`, `Primary Key`, `autoincrement`) : Identifiant unique du coach.
- **first_name** (`str`, `nullable=False`) : Prénom du coach.
- **last_name** (`str`, `nullable=False`) : Nom de famille du coach.
- **email** (`str`, `unique=True`, `nullable=False`) : Adresse email du coach.
- **password_hash** (`str`, `nullable=False`) : Hash du mot de passe du coach.

### Table: `Device`
- **id** (`str`, `Primary Key`) : Identifiant unique de l’appareil.
- **brand** (`str`, `nullable=True`) : Marque de l’appareil.
- **model** (`str`, `nullable=True`) : Modèle de l’appareil.

### Table: `Game`
- **id** (`int`, `Primary Key`, `autoincrement`) : Identifiant unique du match.
- **team_id** (`int`, `Foreign Key`) : Identifiant de l'équipe associée au match.
- **start_ts** (`datetime`, `nullable=False`) : Timestamp du début du match.
- **end_ts** (`datetime`, `nullable=True`) : Timestamp de fin du match.
- **is_underway** (`bool`, `default=False`) : Statut indiquant si le match est en cours.

### Table: `HeartRateData`
- **id** (`int`, `Primary Key`, `autoincrement`) : Identifiant unique des données de rythme cardiaque.
- **device_id** (`str`, `Foreign Key`) : Identifiant de l’appareil.
- **game_id** (`int`, `Foreign Key`) : Identifiant du match.
- **heart_rate** (`int`) : Rythme cardiaque mesuré.
- **timestamp** (`datetime`, `nullable=False`) : Timestamp de la mesure.

### Table: `Line`
- **id** (`int`, `Primary Key`, `autoincrement`) : Identifiant unique de la ligne.
- **team_id** (`int`, `Foreign Key`) : Identifiant de l'équipe associée.
- **is_offense** (`bool`, `default=True`, `nullable=False`) : Indique si la ligne est offensive.
- **line_number** (`int`, `nullable=False`) : Numéro de la ligne.

### Table: `Player`
- **id** (`int`, `Primary Key`, `autoincrement`) : Identifiant unique du joueur.
- **team_id** (`int`, `Foreign Key`) : Identifiant de l'équipe.
- **line_id** (`int`, `Foreign Key`, `nullable=True`) : Identifiant de la ligne actuelle du joueur.
- **first_name** (`str`, `nullable=False`) : Prénom du joueur.
- **last_name** (`str`, `nullable=False`) : Nom de famille du joueur.
- **birth_date** (`datetime`) : Date de naissance du joueur.
- **position** (`str`) : Position du joueur (ex: attaquant, défenseur).
- **email** (`str`, `unique=True`, `nullable=True`) : Email du joueur.
- **number** (`int`) : Numéro du joueur sur la glace.

### Table: `PlayerDeviceAt`
- **id** (`int`, `Primary Key`, `autoincrement`) : Identifiant unique de l'association joueur-appareil.
- **device_id** (`str`, `Foreign Key`) : Identifiant de l’appareil.
- **player_id** (`int`, `Foreign Key`) : Identifiant du joueur.
- **timestamp** (`datetime`, `nullable=False`) : Timestamp de l'association.

### Table: `GameMedicalData`
- **id** (`int`, `Primary Key`, `autoincrement`) : Identifiant unique des données médicales.
- **player_id** (`int`, `Foreign Key`) : Identifiant du joueur.
- **timestamp** (`datetime`, `nullable=False`) : Timestamp de la collecte de données.
- **max_HR** (`int`, `nullable=False`) : Fréquence cardiaque maximale du joueur.
- **rest_HR** (`int`, `nullable=False`) : Fréquence cardiaque au repos.
- **zone1_min_HR** - **zone5_min_HR** (`int`, `nullable=False`) : Fréquence cardiaque pour chaque zone d’intensité.

### Table: `PlayerState`
- **id** (`int`, `Primary Key`, `autoincrement`) : Identifiant unique de l'état du joueur.
- **player_id** (`int`, `Foreign Key`) : Identifiant du joueur.
- **game_id** (`int`, `Foreign Key`) : Identifiant du match.
- **state** (`str`, `nullable=False`) : État actuel du joueur (ex : en jeu, en repos).
- **rec_score** (`int`, `nullable=False`) : Score de récupération du joueur.
- **timestamp** (`datetime`, `nullable=False`) : Timestamp de l'enregistrement de l'état.

### Table: `Team`
- **id** (`int`, `Primary Key`, `autoincrement`) : Identifiant unique de l'équipe.
- **coach_id** (`int`, `Foreign Key`) : Identifiant du coach de l'équipe.
- **team_name** (`str`, `nullable=False`) : Nom de l'équipe.
- **primary_color** (`str`, `nullable=False`) : Couleur principale de l'équipe.
- **secondary_color** (`str`, `nullable=False`) : Couleur secondaire de l'équipe.
- **logo** (`str`, `nullable=True`) : Logo de l'équipe.
- **description** (`str`, `nullable=True`) : Description de l'équipe.

## Glossaire des Termes et Concepts

- **Coach** : Personne responsable de la gestion et de la stratégie d'une équipe. Un coach peut accéder aux données de récupération et de performance des joueurs pour optimiser les rotations et le jeu.
- **Récupération Active** : Phase de repos après un effort intense où le joueur se prépare à revenir sur la glace.
- **Score de Récupération (rec_score)** : Indicateur calculé pour estimer si un joueur est prêt à retourner au jeu.
- **Zone d'Intensité** : Niveau d'effort des joueurs, représenté par différentes zones de fréquence cardiaque (zone1 à zone5).
- **Rythme Cardiaque (Heart Rate)** : Mesure des battements cardiaques par minute, utilisée pour évaluer la fatigue et la récupération.
- **Dispositif Connecté** : Appareil porté par les joueurs pour collecter les données physiologiques en temps réel.
- **Rotation des Joueurs** : Processus de remplacement rapide des joueurs pour maintenir une intensité optimale.
- **Algorithme de Récupération** : Ensemble de règles et calculs pour interpréter les données de récupération.

## Exemples d'Utilisation de l'API

### Exemple d’Endpoint pour Récupérer les Joueurs d'une Équipe
**Endpoint** : `/team/{team_id}/players`  
**Méthode** : `GET`  
**Description** : Récupère la liste des joueurs pour une équipe donnée.  
**Réponse** :
```json
[
  {
    "id": 1,
    "first_name": "Nick",
    "last_name": "Suzuki",
    "position": "C",
    "number": 14
  },
  ...
]
```

## Exemples de Requêtes SQL

### Requête de Sélection des Joueurs
```sql
SELECT * FROM Player WHERE team_id = <team_id>;
```

### Requête pour Ajouter un Nouveau Dispositif
```sql
INSERT INTO Device (id, brand, model) VALUES ('552-26', 'COOSPO', 'HW9');
```

### Requête pour Mettre à Jour l'État d'un Joueur
```sql
UPDATE PlayerState 
SET state = 'en repos', rec_score = 85 
WHERE player_id = <player_id> AND game_id = <game_id>;
```

### Requête pour Supprimer un Match
```sql
DELETE FROM Game WHERE id = <game_id>;
```

### Requête pour Obtenir les Données de Fréquence Cardiaque d'un Joueur
```sql
SELECT heart_rate, timestamp 
FROM HeartRateData 
WHERE device_id = <device_id> AND game_id = <game_id> 
ORDER BY timestamp DESC;
```

### Requête pour Obtenir la Liste des Joueurs d'une Équipe
```sql
SELECT id, first_name, last_name, position, number 
FROM Player 
WHERE team_id = <team_id>;
```

### Requête pour Associer un Appareil à un Joueur
```sql
INSERT INTO PlayerDeviceAt (device_id, player_id, timestamp) 
VALUES ('552-26', <player_id>, NOW());
```

## Auteurs
Benjamin Carignan - Jérémy Généreux