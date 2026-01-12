# Spécifications et Roadmap du Projet SFR Box Remote

Ce document définit les fonctionnalités, l'architecture et les standards de qualité du projet, basés sur l'analyse technique de l'APK SFR TV.

## 1. Backlog des Fonctionnalités
- [ ] **Découverte (Discovery)** : Détection automatique via mDNS/Avahi.
- [ ] **Contrôle de base** : Power (On/Off/Toggle), Volume (+/-/Mute), Navigation (Haut/Bas/Gauche/Droite/OK/Retour/Home).
- [ ] **Contrôle avancé** : Pavé numérique (0-9), touches de couleur, Guide, Replay, Menu.
- [ ] **Gestion des chaînes** : Changement direct par numéro et par nom.
- [ ] **Feedback d'état (WebSocket temps réel)** :
    - État de l'alimentation (On/Off/Veille).
    - Chaîne ou application actuellement diffusée.
    - Volume actuel.
- [ ] **Lancement d'applications** : Raccourcis directs (Netflix, YouTube, Prime Video, etc.).
- [ ] **Gestion multi-box** : Capacité à piloter plusieurs décodeurs sur le même réseau via des sessions WebSocket distinctes.

## 2. Architecture Technique (Unified WebSocket)
Le projet utilise le **Design Pattern "Strategy"** appliqué aux Payloads JSON. Le transport est standardisé pour toutes les versions.

- **WebSocket Core** : Classe mère `SFRBaseDriver` gérant la connexion persistante, le heartbeat et la file d'attente des messages.
- **Payload Strategies** : 
    - `STB8Driver` : Génération de schémas JSON pour la Box 8.
    - `STB7Driver` : Génération de schémas JSON pour la Box 7.
    - `LaBoxDriver` : Génération de schémas JSON pour les versions antérieures.
- **Factory/Registry** : Instanciation du driver spécifique après identification mDNS par le listener Avahi.

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
- **Robustesse Professionnelle** :
    - Gestion de la reconnexion avec **backoff exponentiel**.
    - Monitoring de l'état de connexion (Keep-alive/Heartbeat).
    - Journalisation (Logging) détaillée pour le support utilisateur.

## 5. Livraison et Maintenance
- **Méthode** : GitHub compatible HACS.
- **Documentation** : README.md (Utilisateur) + PROJECT_SPEC.md (Technique).
- **CI/CD** : GitHub Actions pour validation automatique du code.

## 6. Plan d'Exécution (Séquencement)

Le projet est découpé en phases chronologiques. Chaque phase doit être validée (code + tests) avant de passer à la suivante.

### Phase 1 : Socle et Connectivité (Fondations)
1.  **Step 1.1** : Implémentation du `base_driver.py` (Cœur WebSocket + Reconnexion).
2.  **Step 1.2** : Implémentation de `discovery.py` (Listener Avahi pour identifier V7/V8/LaBox).
3.  **Step 1.3** : Centralisation des KeyCodes dans `constants.py` (Traduction de l'APK).

### Phase 2 : Drivers Spécifiques (Intelligence)
1.  **Step 2.1** : Driver V8 (Payloads JSON WebSocket).
2.  **Step 2.2** : Driver V7 (Adaptation Payloads).
3.  **Step 2.3** : Driver LaBox.

### Phase 3 : Interface et Intégration (HACS)
1.  **Step 3.1** : CLI Tool (`cli.py`) pour tests manuels.
2.  **Step 3.2** : Intégration Home Assistant (`media_player` & `remote`).
3.  **Step 3.3** : Blueprints UI Lovelace.

### Phase 4 : Industrialisation
1.  **Step 4.1** : GitHub Actions (CI/CD).
2.  **Step 4.2** : Documentation finale et publication HACS.