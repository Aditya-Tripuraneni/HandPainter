import cv2 as cv
import mediapipe as mp
import pygame
import math

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

WIDTH, HEIGHT = 640, 480

# COLOURS
RED = (255, 0, 0)
VIOLET = (148, 0, 211)
INDIGO = (75, 0, 130)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 127, 0)
WHITE = (255, 255, 255)

color = RED
rainbow = [VIOLET, INDIGO, BLUE, GREEN, YELLOW, ORANGE, RED]

run = True

pygame.init()

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drawing Board")

hands = mp_hands.Hands(max_num_hands=1, min_tracking_confidence=0.7)
camera = cv.VideoCapture(0)


def generate_rainbow(rainbow):
    it = iter(rainbow)
    while True:
        yield next(it)


def convert_to_pixel_coordinates():
    normalized_landmark = handlms.landmark[id]
    pixel_coordinate = mp_drawing._normalized_to_pixel_coordinates(normalized_landmark.x,
                                                                   normalized_landmark.y, width, height)

    return pixel_coordinate


gen_rainbow = generate_rainbow(rainbow)

window.fill(WHITE)
while run:
    ret, frame = camera.read()
    frame = cv.flip(frame, 1)
    imgRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    hand = results.multi_hand_landmarks

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        run = False
    if keys[pygame.K_c]:
        window.fill(WHITE)
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

    if hand:
        for handlms in hand:
            for id, lm in enumerate(handlms.landmark):
                height, width, c = frame.shape
                cx, cy = int(lm.x * width), int(lm.y * height)
                if id == 4:
                    global thumb_coordinates
                    cv.circle(frame, (cx, cy), 15, (255, 0, 0), cv.FILLED)
                    thumb_coordinates = convert_to_pixel_coordinates()
                if id == 8:
                    global index_coordinates
                    cv.circle(frame, (cx, cy), 15, (255, 0, 255), cv.FILLED)
                    index_coordinates = convert_to_pixel_coordinates()

                    x_distance = index_coordinates[0] - thumb_coordinates[0]
                    y_distance = index_coordinates[1] - thumb_coordinates[1]
                    distance = math.sqrt((x_distance ** 2) + (y_distance ** 2))

                    #try:
                    if 0 <= distance <= 20:
                        pygame.draw.circle(window, color,
                                               (index_coordinates[0], index_coordinates[1]), 5)

                    #except TypeError:
                        #run = False
                        #print("Your index finger was out of bounds so program shutdown.")

                mp_drawing.draw_landmarks(frame, handlms, mp_hands.HAND_CONNECTIONS)
    pygame.display.update()
    cv.imshow("Window", frame)

camera.release()
cv.destroyAllWindows()
pygame.quit()
