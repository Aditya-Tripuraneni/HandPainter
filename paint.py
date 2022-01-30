import cv2 as cv
import mediapipe as mp
import pygame
import math

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

WIDTH, HEIGHT = 480, 480

# COLOURS
RED = (255, 0, 0)
VIOLET = (148, 0, 211)
INDIGO = (75, 0, 130)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 127, 0)

color = RED

pygame.init()

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drawing Board")

run = True

hands = mp_hands.Hands(max_num_hands=1, min_tracking_confidence=0.7)

camera = cv.VideoCapture(0)

rainbow = [VIOLET, INDIGO, BLUE, GREEN, YELLOW, ORANGE, RED]


def generate_rainbow(rainbow):
    it = iter(rainbow)
    while True:
        try:
            yield next(it)
        except StopIteration:
            it = iter(rainbow)


def convert_to_pixel_coordinates():
    normalized_landmark = handlms.landmark[id]
    pixel_coordinate = mp_drawing._normalized_to_pixel_coordinates(normalized_landmark.x,
                                                                   normalized_landmark.y, width, height)

    return pixel_coordinate


gen_rainbow = generate_rainbow(rainbow)

while run:
    ret, frame = camera.read()
    frame = cv.flip(frame, 1)
    imgRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        run = False
    if keys[pygame.K_c]:
        window.fill((0, 0, 0))
    if keys[pygame.K_r]:
        color = RED
    if keys[pygame.K_b]:
        color = BLUE
    if keys[pygame.K_y]:
        color = YELLOW
    if keys[pygame.K_g]:
        color = GREEN
    if keys[pygame.K_o]:
        color = ORANGE
    if keys[pygame.K_l]:
        color = next(gen_rainbow)

    if results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks:
            for id, lm in enumerate(handlms.landmark):
                height, width, c = frame.shape
                cx, cy = int(lm.x * width), int(lm.y * height)
                if id == 4:
                    global thumb_coordinates
                    cv.circle(frame, (cx, cy), 15, (255, 0, 0), cv.FILLED)
                    thumb_coordinates = convert_to_pixel_coordinates()
                    print(f"THUMB COORDINATES: {thumb_coordinates}")
                if id == 8:
                    global index_coordinates
                    cv.circle(frame, (cx, cy), 15, (255, 0, 255), cv.FILLED)
                    index_coordinates = convert_to_pixel_coordinates()
                    print(f"INDEX COORDINATES: {index_coordinates}")

                    x_distance = index_coordinates[0] - thumb_coordinates[0]
                    y_distance = index_coordinates[1] - thumb_coordinates[1]
                    distance = math.sqrt((x_distance ** 2) + (y_distance ** 2))
                    print(f"DISTANCE {distance}")

                    try:
                        if 0 <= distance <= 20:

                            pygame.draw.circle(window, color,
                                               (index_coordinates[0], index_coordinates[1]), 5)
                            pygame.display.update()
                        else:
                            print("Too far!")
                    except TypeError:
                        run = False
                        print("Your index finger was out of bounds so program shutdown.")

                mp_drawing.draw_landmarks(frame, handlms, mp_hands.HAND_CONNECTIONS)

    cv.imshow("Window", frame)

camera.release()
cv.destroyAllWindows()
pygame.quit()
