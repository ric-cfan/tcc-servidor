import cv2
from ultralytics import YOLO
import base64
import logging

confidence_threshold = 0.5
logger = logging.getLogger(__name__)

class CameraService:
    def __init__(self, camera_id: int):
        self.camera_id = camera_id
        self.cap = cv2.VideoCapture(camera_id)
        self.model = YOLO("yolo12s.pt")

    def get_person_snapshot_base64(self):
        success, frame = self.cap.read()
        if not success:
            logger.error(f"Erro ao capturar frame da câmera {self.camera_id}")
            return None

        results = self.model(frame)[0]
        logger.info(f"YOLO rodou sobre o frame da câmera {self.camera_id}.")

        for box in results.boxes:
            if int(box.cls[0]) == 0 and box.conf[0] > confidence_threshold:
                xyxy = box.xyxy[0].cpu().numpy().astype(int)
                cv2.rectangle(frame, (xyxy[0], xyxy[1]), (xyxy[2], xyxy[3]), (0, 255, 0), 2)
                logger.info(f"Câmera {self.camera_id}: Pessoa detectada! Coordenadas: {xyxy}")

                _, buffer = cv2.imencode('.jpg', frame)
                jpg_as_text = base64.b64encode(buffer).decode('utf-8')
                return jpg_as_text

        logger.info(f"Câmera {self.camera_id}: Nenhuma pessoa detectada no frame.")
        return None
