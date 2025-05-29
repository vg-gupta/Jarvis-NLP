import cv2

def AuthenticateFace():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('C:/Users/vikra/Downloads/jarvis-main/jarvis-main/engine/auth/trainer/trainer.yml')

    faceCascade = cv2.CascadeClassifier('C:/Users/vikra/Downloads/jarvis-main/jarvis-main/engine/auth/haarcascade_frontalface_default.xml')
    font = cv2.FONT_HERSHEY_SIMPLEX
    names = ['', 'Vikram']

    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(3, 640)
    cam.set(4, 480)

    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    while True:
        ret, img = cam.read()
        if not ret:
            print("Failed to capture frame")
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(int(minW), int(minH)))

        for (x, y, w, h) in faces:
            id, accuracy = recognizer.predict(gray[y:y+h, x:x+w])

            if accuracy < 60:  # tighten the threshold if needed
                print(f"Face recognized as {names[id]} with {round(100 - accuracy)}% confidence")
                cam.release()
                cv2.destroyAllWindows()
                return True
            else:
                print(f"Face not recognized. Confidence: {round(100 - accuracy)}%")

            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(img, names[id] if accuracy < 100 else "Unknown", (x+5, y-5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, f"{round(100 - accuracy)}%", (x+5, y+h-5), font, 1, (255, 255, 0), 1)

        cv2.imshow('Face Authentication', img)

        if cv2.waitKey(10) & 0xff == 27:
            break

    cam.release()
    cv2.destroyAllWindows()
    return False
