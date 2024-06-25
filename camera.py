import cv2

def take_photo():
	cam = cv2.VideoCapture(0)
	for _ in range(30):
		result, image = cam.read()
	
	if result:
		photo_path = "photo.jpg"
		cv2.imwrite(photo_path, image)
		cam.release()
		return photo_path
	else:
		cam.release()
		raise Exception("Не удалось сделать снимок")