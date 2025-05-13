import asyncio
import json
from datetime import datetime
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
                now = datetime.now().astimezone()
                data = {
                    "date": now.strftime("%d/%m/%Y"),
                    "time": now.strftime("%H:%M:%S"),
                    "timezone": str(now.tzinfo),
                    "image_base64": snapshot_b64
                }
                json_data = json.dumps(data)

                logger.info("Pessoa detectada. Enviando snapshot com metadados...")
                await websocket.send_text(json_data)
                await asyncio.sleep(5)
            else:
                logger.info("Nenhuma pessoa detectada. Tentando novamente...")
                await asyncio.sleep(1)
    except WebSocketDisconnect:
        logger.info("Cliente desconectado")