import pygame
import random


HEIGHT = 500
WIDTH = 1000
GREY = (173, 173, 173)
WHITE = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(WHITE)
pygame.display.update()


random_counts = [0] * 20
rect_width = WIDTH/len(random_counts)

while True:
    index =  random.randint(0, len(random_counts) - 1)
    random_counts[index] = random_counts[index] + 1

    for i in range(len(random_counts)):
        pygame.draw.rect(
            screen,
            GREY,
            (
                i * rect_width,
                HEIGHT - random_counts[i],
                rect_width - 1,
                random_counts[i]
            )
        )
    pygame.display.flip()
