# CORE - Coaching Assisted Recovery Ecosystem (Frontend)

## Description
Ce module est une interface utilisateur réactive qui permet d’afficher les données recueillies et analysées par le backend.

## Prérequis

Assurez-vous d'avoir les outils suivants installés avant de commencer :
- **Node.js** : Version recommandée v20.17.0
- **npm** : Inclus avec Node.js
- **Backend CORE** : Le backend doit être opérationnel pour que le frontend puisse récupérer les données en temps réel.


## Installation
Installer les dépendances requises en exécutant la commande suivante :
```sh
npm install
```

### Développement
Pour compiler en développement avec hot-Reload, exécuter la commande suivante :
```sh
npm run dev
```

### Compiler pour production
```sh
npm run build
```

## Structure des Dossiers

- public/ : Contient les fichiers statiques (images, icônes, etc.).
- src/ : Contient l’intégralité du code source :
  - components/ : Composants Vue.js réutilisables.
  - views/ : Pages principales de l’application.
  - store/ : Gestion globale de l'état avec Vuex ou Pinia.
  - assets/ : Fichiers SCSS, images ou autres ressources spécifiques.
  - utils/ : Fonctions utilitaires.
- tailwind.config.js : Configuration de Tailwind CSS pour le design.
- vite.config.js : Configuration pour Vite, le bundler utilisé.

## Auteurs
Benjamin Carignan - Jérémy Généreux