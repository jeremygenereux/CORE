# CORE - Coaching Assisted Recovery Ecosystem
<img src="ASSETS/Identité visuelle/Couleur/Logo Couleur.svg" alt="Logo" width="200" height="200">

## Contexte du Projet
**CORE** (Coaching Assisted Recovery Ecosystem) est un projet étudiant innovant visant à transformer la manière dont les performances des joueurs de hockey sont gérées en temps réel. Le projet vise à fournir aux entraîneurs des données physiologiques en temps réel, comme le rythme cardiaque et la variabilité de récupération, collectées via des capteurs connectés portés par les joueurs.

Grâce à ces informations, les entraîneurs peuvent prendre des décisions éclairées pour optimiser les rotations, maximiser la performance de l’équipe, et minimiser le risque de fatigue excessive. CORE met l’accent sur l’interprétation rapide et fiable des données pour permettre des interventions immédiates pendant les matchs, contribuant ainsi à une stratégie de jeu dynamique et bien informée.

## Structure du Projet

Le projet est organisé comme suit :

### main
- **BACKEND** :
    - Gestion des données physiologiques en temps réel via Python et FastAPI.
    - Communication avec une base de données PostgreSQL.
    - Algorithme validé par la FASAP, intégrant des concepts comme la variabilité cardiaque pour déterminer l'état de récupération des joueurs.
- **FRONTEND** :
    - Interface utilisateur réactive et intuitive développée avec Vue.js.
    - Affichage en temps réel des données via WebSockets.- 

### laandingPage
- **LANDING PAGE** :
    - Une vitrine déployée automatiquement via GitHub Pages : [CORE Landing Page](https://jeremygenereux.github.io/CORE/).

## Technologie et Architecture
- Communication des capteurs via ANT+ pour une portée optimale.
- Algorithme calculant un score de récupération :  
  `Rec Score = (FC Max - FC) / (FC Max - FC Min Zone 1) * 100`

## Vision
CORE pose les bases pour une adoption technologique dans le hockey professionnel et vise à :
- Améliorer la gestion des rotations en temps réel.
- Intégrer à terme des fonctionnalités avancées (IA, prédiction des blessures).
- Étendre l'expérience aux spectateurs avec des données enrichies en direct.

## Collaborateurs
- **Jérémy Généreux** [développeur initial]
- **Benjamin Carignan** [développeur initial]
- **Pre Nadia Tahiri** [superviseure]

## Équipement
- **Capteurs ANT+** :
  COOSPO - REALZONE HW9 Armband Heart Rate Monitor

## Universités et départements
- **Université de Sherbrooke** : Faculté des sciences de l'activité physique. [Département de kinésiologie]
- **Université de Sherbrooke** : Faculté des sciences. [Département d'informatique]

## Licence
Ce projet est sous licence Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0). Cela signifie que l'utilisation commerciale est interdite. Consultez le fichier `LICENSE` pour plus d'informations.

## Contact
Pour toute question ou commentaire, veuillez nous contacter via le profil GitHub.

---

Pour plus de détails techniques, veuillez consulter les sous-dossiers `BACKEND` et `FRONTEND`. Ce dépôt est public.
