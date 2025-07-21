import cv2
import numpy as np
import mediapipe as mp
import time

# Mediapipe Setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Canvas and Color Palette
canvas = None
colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0),
          (0, 255, 255), (255, 255, 255), (0, 0, 0)]
color_names = ['Red', 'Green', 'Blue', 'Yellow', 'White', 'Eraser']
color_index = 0

rainbow_colors = [(255, 0, 0), (255, 128, 0), (255, 255, 0),
                  (0, 255, 0), (0, 255, 255), (0, 0, 255), (128, 0, 255)]
rainbow_index = 0

xp, yp = 0, 0

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

def draw_color_palette(img):
    for i, color in enumerate(colors):
        x = i * 100
        cv2.rectangle(img, (x, 0), (x + 100, 100), color, -1)
        cv2.putText(img, color_names[i], (x + 5, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (50, 50, 50), 2)

def fingers_up(hand_landmarks):
    tips = [8, 12, 16, 20]
    return [hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y for tip in tips]

def explode_canvas(canvas):
    explosion = canvas.copy()
    for _ in range(30):
        M = np.float32([[1, 0, np.random.randint(-20, 20)],
                        [0, 1, np.random.randint(-20, 20)]])
        explosion = cv2.warpAffine(explosion, M, (canvas.shape[1], canvas.shape[0]))
        yield explosion

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    if canvas is None:
        canvas = np.zeros_like(frame)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    draw_color_palette(frame)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lm_list = []
            for lm in handLms.landmark:
                h, w, _ = frame.shape
                lm_list.append((int(lm.x * w), int(lm.y * h)))

            x1, y1 = lm_list[8]  # Index fingertip
            fingers = fingers_up(handLms)
            finger_count = sum(fingers)

            # Explode (5 fingers up)
            if finger_count == 5:
                for exploded in explode_canvas(canvas):
                    blend = cv2.addWeighted(frame, 0.3, exploded, 0.7, 0)
                    cv2.imshow("Virtual Painter", blend)
                    cv2.waitKey(30)
                canvas = np.zeros_like(canvas)
                xp, yp = 0, 0
                continue

            # Auto Save (4 fingers up)
            if finger_count == 4 and all(fingers[:4]):
                filename = f"drawing_{int(time.time())}.png"
                cv2.imwrite(filename, canvas)
                print(f"Saved as {filename}")
                continue

            # Eraser (Fist = 0 fingers)
            if finger_count == 0:
                brush_color = (0, 0, 0)
                if xp == 0 and yp == 0:
                    xp, yp = x1, y1
                cv2.line(canvas, (xp, yp), (x1, y1), brush_color, 50)
                xp, yp = x1, y1
                continue

            # Top Palette Bar Selection
            if y1 < 100:
                color_index = x1 // 100
                if color_index >= len(colors):
                    color_index = 0
            else:
                # Rainbow Brush (3 fingers)
                if finger_count == 3:
                    brush_color = rainbow_colors[rainbow_index % len(rainbow_colors)]
                    rainbow_index += 1
                else:
                    brush_color = colors[color_index]

                # Draw with index only
                if fingers[0] and not any(fingers[1:]):
                    if xp == 0 and yp == 0:
                        xp, yp = x1, y1
                    cv2.line(canvas, (xp, yp), (x1, y1), brush_color,
                             15 if color_index != 5 else 50)
                    xp, yp = x1, y1
                else:
                    xp, yp = 0, 0

            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

    # Merge canvas and frame
    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, inv = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
    inv = cv2.cvtColor(inv, cv2.COLOR_GRAY2BGR)
    frame = cv2.bitwise_and(frame, inv)
    frame = cv2.bitwise_or(frame, canvas)

    cv2.imshow("Virtual Painter", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
