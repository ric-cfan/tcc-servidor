import asyncio
from fastapi import WebSocket, WebSocketDisconnect
import logging
from app.yolo_service import get_person_snapshot_base64

# Configuração básica de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def handle_websocket(websocket: WebSocket):
    await websocket.accept()
    logger.info("Novo cliente conectado via WebSocket")
    
    try:
        while True:
            snapshot_b64 = get_person_snapshot_base64()
            
            if snapshot_b64:
                logger.info("Pessoa detectada. Enviando snapshot...")
                await websocket.send_text(snapshot_b64)
                await asyncio.sleep(5)  # tempo de "trava" entre envios
            else:
                logger.info("Nenhuma pessoa detectada. Tentando novamente...")
                await asyncio.sleep(1)
    except WebSocketDisconnect:
        logger.info("Cliente desconectado")
