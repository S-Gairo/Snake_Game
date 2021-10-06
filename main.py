import pygame
from pygame.locals import *
import time
import random

size = 40


class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("C:/Users/hp/Desktop/Project/SnakeGame/resources/snake_block.png").convert()
        self.x = [size] * length
        self.y = [size] * length
        self.direction = 'down'

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i] % 1000, self.y[i] % 600))
        pygame.display.flip()

    def move_up(self):
        if self.direction != 'down':
            self.direction = 'up'

    def move_left(self):
        if self.direction != 'right':
            self.direction = 'left'

    def move_right(self):
        if self.direction != 'left':
            self.direction = 'right'

    def move_down(self):
        if self.direction != 'up':
            self.direction = 'down'

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def walk(self):

        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'up':
            self.y[0] -= size
        if self.direction == 'down':
            self.y[0] += size
        if self.direction == 'left':
            self.x[0] -= size
        if self.direction == 'right':
            self.x[0] += size

        self.draw()


class Apple:
    def __init__(self, parent_screen):
        self.apple = pygame.image.load("C:/Users/hp/Desktop/Project/SnakeGame/resources/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = size * 10
        self.y = size * 10

    def draw(self):
        self.parent_screen.blit(self.apple, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0, 24) * size
        self.y = random.randint(0, 14) * size


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((1000, 600))
        self.snake = Snake(self.surface, 4)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score : {self.snake.length - 4}", True, (0, 0, 0))
        self.surface.blit(score, (800, 10))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.apple.move()
            self.snake.increase_length()

        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0] % 1000, self.snake.y[0] % 600, self.snake.x[i] % 1000, self.snake.y[i] % 600):
                raise "Game Over"

    def is_collision(self, x1, y1, x2, y2):

        if x2 <= x1 % 1000 < x2 + size:
            if y2 <= y1 % 600 < y2 + size:
                return True
        return False

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game Over! Score : {self.snake.length - 4}", True, (0, 0, 0))
        self.surface.blit(line1, (350, 250))
        line2 = font.render("To play again press Enter. To Exit press Escape!", True, (0, 0, 0))
        self.surface.blit(line2, (250, 300))
        pygame.display.flip()

    def render_background(self):
        bgg = pygame.image.load("C:/Users/hp/Desktop/Project/SnakeGame/resources/sky.jpg")
        self.surface.blit(bgg, (0, 0))

    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pause = False
                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        elif event.key == K_LEFT:
                            self.snake.move_left()
                        elif event.key == K_RIGHT:
                            self.snake.move_right()
                        elif event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.1)

    def reset(self):
        self.snake = Snake(self.surface, 4)
        self.apple = Apple(self.surface)


if __name__ == "__main__":
    game = Game()
    game.run()
