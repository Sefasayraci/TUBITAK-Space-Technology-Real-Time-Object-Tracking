import cv2
import numpy as np
import serial

# Harici kamera cihaz numarasını belirtin (genellikle 0, 1, 2 gibi)
camera_device = 1

# Kamerayı başlatın
cap = cv2.VideoCapture(camera_device)

# Ekranın genişlik ve yükseklik bilgilerini alın
screen_width = int(cap.get(3))
screen_height = int(cap.get(4))

# Bölge sınırlarını hesaplayın
center_x = screen_width // 2
center_y = screen_height // 2
quarter_width = screen_width // 2
quarter_height = screen_height // 2

# Seri portu açın (Arduino'nun bağlı olduğu porta göre değiştirin)
ser = serial.Serial('COM9', 9600)  # COM3 ve 9600 hızınızı ve port numaranızı ayarlayın

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

        # Konturun merkez koordinatlarını bulun
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0

        # Nesnenin hangi bölgede olduğunu kontrol edin
        if cX < center_x and cY < center_y:
            # Sol üst bölge
            servo_acisi = 0  # Örneğin, 0 derece
        elif cX >= center_x and cY < center_y:
            # Sağ üst bölge
            servo_acisi = 90  # Örneğin, 90 derece
        elif cX < center_x and cY >= center_y:
            # Sol alt bölge
            servo_acisi = 180  # Örneğin, 180 derece
        else:
            # Sağ alt bölge
            servo_acisi = 270  # Örneğin, 270 derece

        # Servo açısını Arduino'ya gönderin
        ser.write(str(servo_acisi).encode())

    # Sonuçları gösterin
    cv2.imshow('Original', frame)
    cv2.imshow('Mask', mask)
    cv2.imshow('Result', result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Seri bağlantıyı kapatın
ser.close()

# Video yakalama işlemini serbest bırakın ve pencereleri kapatın
cap.release()
cv2.destroyAllWindows()
