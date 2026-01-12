#!/bin/bash

# Script d'initialisation du projet SFR-Box-Remote
# Basé sur les spécifications AGENTS.md

echo "🚀 Initialisation de l'arborescence SFR-Box-Remote..."

# 1. Création de la structure des dossiers
mkdir -p .github/workflows
mkdir -p docs
mkdir -p sfr_box_core
mkdir -p custom_components/sfr_box_remote
mkdir -p ui
mkdir -p scripts
mkdir -p tests

# 3. Création du fichier PROGRESS.md (Suivi d'état)
cat << 'EOF' > PROGRESS.md
# PROGRESS.md : État d'avancement du projet

## État Actuel
- [x] Initialisation de l'arborescence
- [x] Création des documents de référence (AGENTS, README, SPEC)

## En cours (WIP)
- [ ] Définition de la classe de base WebSocket (`base_driver.py`)

## Blocages / Infos Manquantes
- Nécessite l'intégration des KeyCodes extraits de l'APK.

## Prochaine Étape (Next Step)
- Implémenter le squelette de `sfr_box_core/base_driver.py` avec gestion de la reconnexion.
EOF


# 5. Création du fichier pyproject.toml
cat << 'EOF' > pyproject.toml
[project]
name = "sfr-box-remote"
version = "0.1.0"
dependencies = [
    "websockets>=12.0",
    "zeroconf>=0.131.0",
    "aiohttp>=3.9.0",
]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
EOF

# 6. Création du fichier base_driver.py (Squelette initial)
cat << 'EOF' > sfr_box_core/base_driver.py
import asyncio
import logging
from abc import ABC, abstractmethod

_LOGGER = logging.getLogger(__name__)

class SFRBaseDriver(ABC):
    """Classe de base asynchrone pour le pilotage des box SFR via WebSocket."""
    
    def __init__(self, ip: str, port: int = 8080):
        self.ip = ip
        self.port = port
        self.is_connected = False

    @abstractmethod
    async def connect(self):
        """Établir la connexion."""
        pass

    @abstractmethod
    async def send_key(self, key: str):
        """Envoyer une touche."""
        pass
EOF

# 7. Finalisation
echo "✅ Initialisation terminée. Vous pouvez maintenant faire votre premier commit Git."