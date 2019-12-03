import pygame
import random

HEIGHT = 500
WIDTH = 1000
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(WHITE)
pygame.display.update()


class Walker():
    def __init__(self, ht, wt):
        self.x = wt // 2
        self.y = ht // 2

    def display(self):
        pygame.draw.circle(screen, BLACK, (self.x, self.y), 0)
        pygame.display.flip()

    def walk(self):
        choice = random.randint(0,3)
        if choice == 0:
            self.x = self.x + 1
        elif choice == 1:
            self.x = self.x - 1
        elif choice == 2:
            self.y = self.y + 1
        else:
            self.y = self.y - 1

w = Walker(HEIGHT, WIDTH)

def draw():
    w.walk()
    w.display()

while True:
    draw()
