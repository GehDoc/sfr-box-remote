# Spécifications et Roadmap du Projet SFR Box Remote

Ce document définit les fonctionnalités, l'architecture et les standards de qualité du projet, basés sur l'analyse technique de l'APK SFR TV.

## 1. Backlog des Fonctionnalités

- [ ] **Découverte (Discovery)** : Détection automatique via mDNS/Avahi et autres méthodes (DNS, API Router).
- [ ] **Contrôle de base** : Power (On/Off/Toggle), Volume (+/-/Mute), Navigation (Haut/Bas/Gauche/Droite/OK/Retour/Home).
- [ ] **Contrôle avancé** : Pavé numérique (0-9), touches de couleur, Guide, Replay, Menu.
- [ ] **Gestion des chaînes** : Changement direct par numéro et par nom.
- [ ] **Feedback d'état (WebSocket temps réel)** :
  - État de l'alimentation (On/Off/Veille).
  - Chaîne ou application actuellement diffusée.
  - Volume actuel.
- [ ] **Lancement d'applications** : Raccourcis directs (Netflix, YouTube, Prime Video, etc.).
- [ ] **Gestion multi-box** : Capacité à piloter plusieurs décodeurs (STB8, STB7, LaBox, EVO) sur le même réseau via des sessions WebSocket distinctes.

## 2. Architecture Technique (Stratégie de Commandes Polymorphiques)

Le projet utilise le **Design Pattern "Strategy"** appliqué aux Payloads JSON, centré sur un système de commandes polymorphiques. Le transport est standardisé pour toutes les versions.

- **WebSocket Core & Gestion des Commandes** :
  - `base_driver.py` : Classe mère `SFRBaseDriver` gérant la connexion persistante, le heartbeat, la file d'attente des messages, et fournissant une interface générique pour l'envoi et la réception de commandes (ex: `send_command(command, **params)`). Elle définit également la structure pour récupérer les commandes disponibles (`get_available_commands()`) pour chaque driver spécialisé.
- **Stratégies de Commandes Spécifiques (Drivers)** : Chaque driver implémente les commandes spécifiques à son modèle de box.
  - `v8_driver.py` : Définit et génère les commandes pour la Box TV 8.
  - `v7_driver.py` : Définit et génère les commandes pour la Box TV 7.
  - `labox_driver.py` : Définit et génère les commandes pour LaBox.
  - `evo_driver.py` : Définit et génère les commandes pour le modèle EVO.
- **Factory/Registry** : Instanciation du driver spécifique après identification (mDNS, DNS, API Router) par le listener.
- **`constants.py`** : Centralise les constantes partagées par la librairie, incluant les valeurs de certains paramètres de commande (ex: KeyCodes utilisés par une commande `send_key`).

## 3. Déliverables

1. **Librairie Core (Python)** : Bibliothèque asynchrone autonome.
2. **CLI Tool** : Utilitaire `sfr-control` pour test de connexion et envoi de commandes en terminal.
3. **Intégration Home Assistant** : Custom Component (`media_player` & `remote`).
4. **HACS Repository** : Structure conforme pour installation simplifiée.
5. **Dashboard UI** : Templates Lovelace (YAML) pour une interface mobile/tablette.

## 4. Standards de Développement

- **Langage** : Python 3.12+ (Asynchrone via `asyncio` et `websockets`).
- **Qualité** :
  - Typage statique complet.
  - Tests unitaires avec `pytest` incluant un serveur WebSocket de mock.
  - Qualité de code et formatage forcés par `ruff` via `pre-commit` hooks.
- **Robustesse Professionnelle** :
  - Gestion de la reconnexion avec **backoff exponentiel**.
  - Monitoring de l'état de connexion (Keep-alive/Heartbeat).
  - Journalisation (Logging) détaillée pour le support utilisateur.

## 5. Livraison et Maintenance

- **Méthode** : GitHub compatible HACS.
- **Documentation** : README.md (Utilisateur) + PROJECT_SPEC.md (Technique).
- **CI/CD** : GitHub Actions pour validation automatique du code et publication.

## 6. Plan d'Exécution (Séquencement)

Le projet est découpé en phases chronologiques. Chaque phase doit être validée (code + tests) avant de passer à la suivante.

### Phase 1 : Socle et Connectivité (Fondations)

1. **Step 1.1** : Implémentation du `base_driver.py` (Cœur WebSocket + Reconnexion).
2. **Step 1.2** : Implémentation de `discovery.py` (Listener Avahi pour identifier V7/V8/LaBox/EVO).
3. **Step 1.3** : Définir la structure des commandes et créer `sfr_box_core/constants.py` pour les valeurs de commandes partagées.

### Phase 2 : Drivers Spécifiques (Intelligence)

1. **Phase 2.1** : Driver v8_driver.py - *Priorité Haute*
2. **Phase 2.2** : Driver v7_driver.py - *Priorité Moyenne*

### Phase 3 : Intégration Home Assistant

1. **Step 3.1** : CLI Tool (`cli.py`) pour tests manuels.
2. **Step 3.2** : Intégration Home Assistant (`media_player` & `remote`).
3. **Step 3.3** : Blueprints UI Lovelace.

### Phase 4 : Industrialisation & Publication

1. **Phase 4.1** : CI (Workflows GitHub Actions) - **[x] Effectué**
2. **Phase 4.2** : CD (Publication HACS)

### Phase 5 : Drivers Anciens & Cas Spécifiques

1. **Phase 5.1** : Driver labox_driver.py - *Priorité Basse*
2. **Phase 5.2** : Implémenter la découverte EVO (Router API via MAC) - *Priorité Basse*
3. **Phase 5.3** : Driver evo_driver.py - *Priorité Basse*
