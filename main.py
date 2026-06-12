import cv2
import numpy as np
import mediapipe as mp
import os

THICKNESS = 5
ERASER_THICKNESS = 50
SMOOTHENING = 5

# Colors (B, G, R) - Adjusted Blue
COLOR_RED   = (0, 0, 255)   
COLOR_GREEN = (0, 255, 0)   
COLOR_BLUE  = (255, 0, 0)   # Pure Blue (Try (200, 0, 0) if you want it darker)
COLOR_BLACK = (0, 0, 0)     

# Variables
draw_color = COLOR_RED
xp, yp = 0.0, 0.0          
ploc_x, ploc_y = 0.0, 0.0
timer_delay = 0  # To show "Saved!" text for a short time
clear_timer = 0  # To show "Cleared!" text for a short time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.85, min_tracking_confidence=0.5, max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

img_canvas = None

def draw_palette(img):
    # Header
    cv2.rectangle(img, (0,0), (1280, 85), (50, 50, 50), cv2.FILLED)
    # Colors
    cv2.rectangle(img, (40, 10), (140, 75), COLOR_RED, cv2.FILLED)
    cv2.rectangle(img, (160, 10), (260, 75), COLOR_GREEN, cv2.FILLED)
    cv2.rectangle(img, (280, 10), (380, 75), COLOR_BLUE, cv2.FILLED)
    # Eraser
    cv2.rectangle(img, (1150, 10), (1250, 75), (255, 255, 255), cv2.FILLED)
    cv2.putText(img, "Eraser", (1160, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 2)
    cv2.putText(img, "Press 'c' to clear", (430, 52), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
    return img

print("Air Canvas")

while True:
    ret, frame = cap.read()
    if not ret: break

    frame = cv2.flip(frame, 1)
    
    if img_canvas is None:
        img_canvas = np.zeros_like(frame)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)
    
    frame = draw_palette(frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            h, w, c = frame.shape
            
            # Key Points
            x1_raw = int(hand_landmarks.landmark[8].x * w)
            y1_raw = int(hand_landmarks.landmark[8].y * h)
            x2_raw = int(hand_landmarks.landmark[12].x * w)
            y2_raw = int(hand_landmarks.landmark[12].y * h)

            # Smoothing
            cloc_x = ploc_x + (x1_raw - ploc_x) / SMOOTHENING
            cloc_y = ploc_y + (y1_raw - ploc_y) / SMOOTHENING

            index_up = hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y
            middle_up = hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y

            # --- LOGIC ---
            if y1_raw < 85 and index_up and middle_up: # Header selection
                xp, yp = 0.0, 0.0
                if 40 < x1_raw < 140:
                    draw_color = COLOR_RED
                elif 160 < x1_raw < 260:
                    draw_color = COLOR_GREEN
                elif 280 < x1_raw < 380:
                    draw_color = COLOR_BLUE
                elif 1150 < x1_raw < 1250:
                    draw_color = COLOR_BLACK
                cv2.rectangle(frame, (x1_raw-20, y1_raw-20), (x2_raw+20, y2_raw+20), (255,255,255), 2)

            elif index_up and not middle_up: # Draw mode
                if xp == 0.0 and yp == 0.0:
                    xp, yp = cloc_x, cloc_y

                distance = np.hypot(cloc_x - xp, cloc_y - yp)
                if distance > 180:
                    xp, yp = cloc_x, cloc_y

                curr_thick = ERASER_THICKNESS if draw_color == COLOR_BLACK else THICKNESS
                cv2.line(img_canvas, (int(xp), int(yp)), (int(cloc_x), int(cloc_y)), draw_color, curr_thick)
                cv2.circle(frame, (int(cloc_x), int(cloc_y)), 15, draw_color, cv2.FILLED)
                xp, yp = cloc_x, cloc_y

            elif index_up and middle_up: # Hover mode without drawing
                xp, yp = 0.0, 0.0
                cv2.rectangle(frame, (int(cloc_x)-20, int(cloc_y)-25), (int(cloc_x)+20, int(cloc_y)+25), draw_color, cv2.FILLED)

            else:
                xp, yp = 0.0, 0.0

            ploc_x, ploc_y = cloc_x, cloc_y
    else:
        ploc_x, ploc_y = 0, 0
        xp, yp = 0, 0

    # Merge Layers
    img_gray = cv2.cvtColor(img_canvas, cv2.COLOR_BGR2GRAY)
    _, img_inv = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY_INV)
    frame = cv2.bitwise_and(frame, frame, mask=img_inv)
    frame = cv2.bitwise_or(frame, img_canvas)

    # --- FEEDBACK MESSAGES ---
    if timer_delay > 0:
        timer_delay -= 1
        cv2.putText(frame, "SAVED TO FOLDER!", (400, 360), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
    
    if clear_timer > 0:
        clear_timer -= 1
        cv2.putText(frame, "CANVAS CLEARED!", (400, 360), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

    cv2.imshow("Air Canvas", frame)
    
    # --- CONTROLS ---
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord('q'): # Quit
        break
    
    elif key == ord('s'): # Save
        # Save the pure artwork (black background)
        cv2.imwrite("my_air_canvas_art.jpg", img_canvas)
        # OR uncomment this line to save the photo with your face:
        # cv2.imwrite("my_air_canvas_photo.jpg", frame)
        
        print("Image Saved!")
        timer_delay = 50 # Show "Saved" message for ~2 seconds
    
    elif key == ord('c'): # Clear
        img_canvas[:] = 0  # Clear entire canvas to black
        print("Canvas Cleared!")
        clear_timer = 50 # Show "Cleared" message for ~2 seconds

cap.release()
cv2.destroyAllWindows()
