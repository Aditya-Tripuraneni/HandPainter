import cv2 as cv
import mediapipe as mp
import pygame

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

width, height = 480, 480

RED = (255, 0, 0)
pygame.init()

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Drawing Board")
run = True

hands = mp_hands.Hands(max_num_hands=1, min_tracking_confidence=0.7)

camera = cv.VideoCapture(0)

while run:
    ret, frame = camera.read()
    frame = cv.flip(frame, 1)
    imgRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks:
            for id, lm in enumerate(handlms.landmark):
                height, width, c = frame.shape
                cx, cy = int(lm.x * width), int(lm.y * height)
                print(height, height)
                if id == 8:
                    print("INDEX FINGER FOUND")
                    cv.circle(frame, (cx, cy), 25, (255, 0, 255), cv.FILLED)
                    normalizedlandmark = handlms.landmark[id]
                    pixelcoordiante = mp_drawing._normalized_to_pixel_coordinates(normalizedlandmark.x,
                                                                                  normalizedlandmark.y, width, height)

                    print(f"INDEX COORDINATES: {pixelcoordiante}")
                    if pixelcoordiante[0] and pixelcoordiante[1] != None:
                        pygame.draw.rect(window, RED, (pixelcoordiante[0], pixelcoordiante[1], 10, 10))
                        pygame.display.update()
                    else:
                        run = False
                        print("Out of bounds cannot draw!")


                mp_drawing.draw_landmarks(frame, handlms, mp_hands.HAND_CONNECTIONS)

    cv.imshow("Window", frame)

    if cv.waitKey(1) == ord('q'):
        print("breaking")
        break

camera.release()
cv.destroyAllWindows()
pygame.quit()
