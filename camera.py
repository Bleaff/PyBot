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
        photo_path = "photo.jpg"
        res = cv2.imwrite(photo_path, image)
        cam.release()
        if res:
            logger.info("Photo saved successfully")
        else:
            logger.error("Failed to save the photo")
        return photo_path
    else:
        cam.release()
        logger.error("Failed to take a photo with the webcam")
        raise Exception("Не удалось сделать снимок")

if __name__ == '__main__':
    take_photo()