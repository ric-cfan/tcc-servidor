from fastapi import FastAPI, WebSocket
from fastapi.routing import APIRouter
from app.websocket_handler import handle_camera_websocket
from app.yolo_service import CameraService

app = FastAPI()

# Lista de IDs das câmeras disponíveis
camera_ids = [1]

# Inicializa serviços por câmera
camera_services = {camera_id: CameraService(camera_id) for camera_id in camera_ids}

# Endpoint HTTP GET para listar câmeras disponíveis
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
