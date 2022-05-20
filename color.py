import cv2
import numpy as np


def draw(mask, color, frame_c):
    contours,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        area = cv2.contourArea(c)
        if area > 1000:
            new_countour = cv2.convexHull(c)
            cv2.drawContours(frame_c, [new_countour], 0, color, 3)
            M = cv2.moments(c)
            if M["m00"] == 0: M["m00"] = 1
            x = int(M["m10"] / M["m00"])
            y = int(M['m01'] / M['m00'])
            font = cv2.FONT_HERSHEY_COMPLEX
            if color == [0, 255, 255]:
                cv2.putText(frame_c, 'Amarillo', (x + 10, y), font, 0.75, (0, 255, 255), 1, cv2.LINE_AA)
            elif color == [255, 0, 0]:
                cv2.putText(frame_c, 'Azul', (x + 10, y), font, 0.75, (255, 0, 0), 1, cv2.LINE_AA)
            elif color == [0, 143, 57]:
                cv2.putText(frame_c, 'Verde', (x + 10, y), font, 0.75, (0, 143, 57), 1, cv2.LINE_AA)
            elif color == [0, 0, 255]:
                cv2.putText(frame_c, 'Rojo', (x + 10, y), font, 0.75, (0, 0, 255), 1, cv2.LINE_AA)


def capture():

    cap = cv2.VideoCapture(0)
    low_yellow = np.array([25, 192, 20], np.uint8)
    high_yellow = np.array([30, 255, 255], np.uint8)
    
    low_blue = np.array([85, 200, 20], np.uint8)
    high_blue = np.array([125, 255, 255], np.uint8)

    low_green = np.array([45, 100, 20], np.uint8)
    high_green = np.array([75, 255, 255], np.uint8)

    low_red1 = np.array([0, 100, 20], np.uint8)
    high_red1 = np.array([5, 255, 255], np.uint8)
    low_red2 = np.array([175, 100, 20], np.uint8)
    high_red2 = np.array([180, 255, 255], np.uint8)

    while True:
        comp,frame = cap.read()
        if comp==True:
            frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            yellow_mask = cv2.inRange(frame_HSV, low_yellow, high_yellow)
            blue_mask = cv2.inRange(frame_HSV, low_blue, high_blue)
            green_mask = cv2.inRange(frame_HSV, low_green, high_green)
            red_mask1 = cv2.inRange(frame_HSV, low_red1, high_red1)
            red_mask2 = cv2.inRange(frame_HSV, low_red2, high_red2)
            red_mask = cv2.add(red_mask1, red_mask2)

            draw(yellow_mask, [0, 255, 255], frame)
            draw(blue_mask, (255, 0, 0), frame)
            draw(green_mask,(0, 143, 57), frame)
            draw(red_mask, [0, 0, 255], frame)
            cv2.imshow('webcam', frame)

            if cv2.waitKey(1) & 0xFF == ord('s'):
                break
                cap.release()
                cv2.destroyAllWindows()
                