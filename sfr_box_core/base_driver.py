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
