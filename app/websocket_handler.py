import asyncio
import json
from datetime import datetime
from fastapi import WebSocket, WebSocketDisconnect
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def handle_camera_websocket(websocket: WebSocket, camera_service, camera_id: str):
    await websocket.accept()
    logger.info(f"Novo cliente conectado na câmera {camera_id} via WebSocket")
    
    # Enviar mensagem de conexão inicial
    connection_data = {
        "type": "connection",
        "camera": camera_id,
        "status": "connected",
        "message": f"Câmera {camera_id} conectada com sucesso"
    }
    await websocket.send_text(json.dumps(connection_data))

    try:
        while True:
            snapshot_b64 = camera_service.get_person_snapshot_base64()

            if snapshot_b64:
                now = datetime.now().astimezone()
                data = {
                    "type": "detection",
                    "date": now.strftime("%d/%m/%Y"),
                    "time": now.strftime("%H:%M:%S"),
                    "timezone": str(now.tzinfo),
                    "image_base64": snapshot_b64,
                    "camera": camera_id,
                }
                json_data = json.dumps(data)
                logger.info(f"Câmera {camera_id}: Pessoa detectada. Enviando snapshot...")
                await websocket.send_text(json_data)
                await asyncio.sleep(5)
            else:
                logger.info(f"Câmera {camera_id}: Nenhuma pessoa detectada. Tentando novamente...")
                await asyncio.sleep(1)
    except WebSocketDisconnect:
        logger.info(f"Cliente desconectado da câmera {camera_id}")
