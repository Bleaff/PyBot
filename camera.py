import cv2
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def take_photo():
    logger.info("Attempting to take a photo with the webcam")
    cam = cv2.VideoCapture(0)
    for _ in range(15):
        result, image = cam.read()
    if result:
        cam.release()
        return cv2.imencode('.jpg', image)[1].tobytes()
    else:
        cam.release()
        logger.error("Failed to take a photo with the webcam")
        raise Exception("Не удалось сделать снимок")

if __name__ == '__main__':
    take_photo()