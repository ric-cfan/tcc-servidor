import cv2
from ultralytics import YOLO
import base64
import logging
import numpy as np

confidence_threshold = 0.5
logger = logging.getLogger(__name__)

class CameraService:
    def __init__(self, camera_id: int):
        self.camera_id = camera_id
        self.cap = cv2.VideoCapture(camera_id)
        self.model = YOLO("yolo12s.pt")
        self._running = True

    def __del__(self):
        self.cleanup()

    def cleanup(self):
        """Libera recursos da câmera"""
        self._running = False
        if hasattr(self, 'cap') and self.cap:
            self.cap.release()
            self.cap = None

    def get_camera_status(self):
        """Verifica status atual da câmera"""
        if not self.cap.isOpened():
            return "error"
        
        ret, _ = self.cap.read()
        return "connected" if ret else "error"

    def apply_night_vision_filter(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        contrasted = cv2.equalizeHist(gray)
        green_tinted = cv2.applyColorMap(contrasted, cv2.COLORMAP_SUMMER)
        return green_tinted

    def get_person_snapshot_base64(self):
        if not self._running or not self.cap or not self.cap.isOpened():
            return None
        
        success, frame = self.cap.read()
        if not success:
            return None

        try:
            #visao noturna
            #frame = self.apply_night_vision_filter(frame)

            results = self.model(frame)[0]
            
            # Verifica se há detecções
            if results.boxes is None or len(results.boxes) == 0:
                return None

            for box in results.boxes:
                # Verifica se é pessoa (classe 0) e confiança
                if len(box.cls) > 0 and len(box.conf) > 0:
                    if int(box.cls[0]) == 0 and box.conf[0] > confidence_threshold:
                        xyxy = box.xyxy[0].cpu().numpy().astype(int)
                        cv2.rectangle(frame, (xyxy[0], xyxy[1]), (xyxy[2], xyxy[3]), (0, 255, 0), 2)
                        logger.info(f"Câmera {self.camera_id}: Pessoa detectada!")

                        _, buffer = cv2.imencode('.jpg', frame)
                        jpg_as_text = base64.b64encode(buffer).decode('utf-8')
                        return jpg_as_text

            return None
        except Exception as e:
            logger.error(f"Erro no YOLO da câmera {self.camera_id}: {e}")
            return None