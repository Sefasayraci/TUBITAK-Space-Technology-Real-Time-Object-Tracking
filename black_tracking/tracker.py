import cv2
import numpy as np

# Harici kamera cihaz numarasını belirtin (genellikle 0, 1, 2 gibi)
camera_device = 1

# Kamerayı başlatın
cap = cv2.VideoCapture(camera_device)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Görüntüyü HSV renk uzayına dönüştürün
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Siyah rengin HSV değerlerini belirleyin
    lower_black = np.array([0, 0, 0])  # Alt sınır HSV değerleri
    upper_black = np.array([180, 255, 30])  # Üst sınır HSV değerleri

    # Belirlenen siyah renk aralığını maskeleme yapın
    mask = cv2.inRange(hsv, lower_black, upper_black)

    # Maskeyi kullanarak nesne takibini gerçekleştirin
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # Siyah nesne konturlarını bulun
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # En büyük konturu bulun
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)

        # Konturun etrafına bir dikdörtgen çizin
        x, y, w, h = cv2.boundingRect(largest_contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Sonuçları gösterin
    cv2.imshow('Original', frame)
    cv2.imshow('Mask', mask)
    cv2.imshow('Result', result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Video yakalama işlemini serbest bırakın ve pencereleri kapatın
cap.release()
cv2.destroyAllWindows()
