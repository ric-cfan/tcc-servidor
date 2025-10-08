from fastapi import FastAPI, WebSocket
from fastapi.routing import APIRouter
from app.websocket_handler import handle_camera_websocket
from app.yolo_service import CameraService
import cv2
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

def detect_available_cameras(max_cameras=5):
    """Detecta câmeras disponíveis no sistema"""
    available_cameras = []
    for i in range(max_cameras):
        cap = None
        try:
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                ret, _ = cap.read()
                if ret:
                    available_cameras.append(i)
                    logger.info(f"Câmera {i} detectada e funcionando")
        except Exception as e:
            logger.error(f"Erro ao testar câmera {i}: {e}")
        finally:
            if cap:
                cap.release()
    return available_cameras

# Detecta câmeras automaticamente
camera_ids = detect_available_cameras()
logger.info(f"Câmeras detectadas: {camera_ids}")

# Inicializa serviços apenas para câmeras funcionais
camera_services = {}
for camera_id in camera_ids:
    try:
        service = CameraService(camera_id)
        if service.get_camera_status() == "connected":
            camera_services[camera_id] = service
            logger.info(f"Serviço da câmera {camera_id} inicializado com sucesso")
        else:
            logger.error(f"Câmera {camera_id} não está funcionando")
    except Exception as e:
        logger.error(f"Erro ao inicializar câmera {camera_id}: {e}")

# Atualiza lista apenas com câmeras funcionais
camera_ids = list(camera_services.keys())

@app.get("/cameras")
def list_cameras():
    return {"cameras": [str(c) for c in camera_ids]}

# Define rotas WebSocket para cada câmera
router = APIRouter()

for cam_id in camera_ids:
    path = f"/ws/{cam_id}"
    
    async def ws_endpoint(websocket: WebSocket, cam_id=cam_id):
        await handle_camera_websocket(websocket, camera_services[cam_id], str(cam_id))
    
    router.websocket(path)(ws_endpoint)

app.include_router(router)

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup ao fechar aplicação"""
    for service in camera_services.values():
        service.cleanup()