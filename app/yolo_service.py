import cv2
from ultralytics import YOLO
import numpy as np
import base64
import logging

confidence_threshold = 0.5
logger = logging.getLogger(__name__)

model = YOLO("yolo12s.pt")  # Certifique-se de ter esse modelo baixado
cap = cv2.VideoCapture(1)   # ou coloque a URL/IP da câmera

def get_person_snapshot_base64():
    success, frame = cap.read()
    if not success:
        logger.error("Erro ao capturar o frame da câmera.")
        return None

    results = model(frame)[0]
    logger.info("YOLO rodou sobre o frame.")

    detected_person = False
    for box in results.boxes:
        if int(box.cls[0]) == 0 and box.conf[0] > confidence_threshold:  # class 0 == person
            detected_person = True
            xyxy = box.xyxy[0].cpu().numpy().astype(int)
            cv2.rectangle(frame, (xyxy[0], xyxy[1]), (xyxy[2], xyxy[3]), (0, 255, 0), 2)
            logger.info(f"Pessoa detectada! Coordenadas da caixa: {xyxy}")

            _, buffer = cv2.imencode('.jpg', frame)
            jpg_as_text = base64.b64encode(buffer).decode('utf-8')
            return jpg_as_text

    if not detected_person:
        logger.info("Nenhuma pessoa detectada no frame.")
    
    return None
