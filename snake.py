from os import error
import pygame
import random
from pygame.constants import K_KP_ENTER
import pygame.freetype
import time

SIZE = 40

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)


class Apple:
    def __init__(self, surface):
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.x = SIZE*3
        self.y = SIZE*3
        self.surface = surface

    def draw(self):
        pygame.draw.circle(self.surface, (255, 255, 255),
                           (self.x+SIZE/2, self.y+SIZE/2), SIZE/2)
        pygame.display.update()

    def move(self):
        self.x = random.randint(0, 24) * SIZE
        self.y = random.randint(0, 19) * SIZE


class Snake:
    def __init__(self, surface, length):

        self.surface = surface
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = 'right'
        self.length = length
        self.takingInput = True
        self.score = 0

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        self.surface.fill((255, 0, 0))
        for i in range(self.length):
            if(i == 0):
                pygame.draw.rect(self.surface, black, pygame.Rect(
                    self.x[i], self.y[i], SIZE, SIZE))
            else:
                pygame.draw.rect(self.surface, green, pygame.Rect(
                    self.x[i], self.y[i], SIZE, SIZE))
        pygame.display.update()

    def moveLeft(self):
        if self.direction != 'right':
            self.takingInput = False
            self.direction = 'left'

    def moveRight(self):
        if self.direction != 'left':
            self.takingInput = False
            self.direction = 'right'

    def moveUp(self):
        if self.direction != 'down':
            self.takingInput = False
            self.direction = 'up'

    def moveDown(self):
        if self.direction != 'up':
            self.takingInput = False
            self.direction = 'down'

    def walk(self):

        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if(self.direction == 'left'):
            self.x[0] -= SIZE
        elif(self.direction == 'right'):
            self.x[0] += SIZE
        elif(self.direction == 'up'):
            self.y[0] -= SIZE
        elif(self.direction == 'down'):
            self.y[0] += SIZE
        self.takingInput = True
        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((1000, 800))
        pygame.display.set_caption("Snake")
        self.surface.fill((255, 0, 0))
        self.snake = Snake(self.surface, 3)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collision(self, x1, y1, x2, y2, direction):
        if direction == 'left':
            if x1 <= x2 + SIZE and x1 >= x2 and y1 == y2:
                return True
        elif direction == 'right':
            if x1 + SIZE >= x2 and x1 <= x2 and y1 == y2:
                return True
        elif direction == 'up':
            if y1 <= y2 + SIZE and y1 >= y2 and x1 == x2:
                return True
        elif direction == 'down':
            if y1 + SIZE >= y2 and y1 <= y2 and x1 == x2:
                return True

        return False

    def show_game_over(self):
        self.surface.fill((0, 0, 0))
        GAME_FONT = pygame.freetype.Font("roboto-regular.ttf", 24)
        text_surface, rect = GAME_FONT.render("Game Over  | Score: "+str((self.snake.length*10)-30), (255, 255, 255))
        self.surface.blit(text_surface, (350, 350))
        text_surface2, rect2 = GAME_FONT.render("To play again, hit enter", (255, 255, 255))
        self.surface.blit(text_surface2, (350, 400))
        pygame.display.update()

    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                print(self.snake.takingInput)
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and self.snake.takingInput:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_RETURN:
                        print("Enter")
                        self.snake = Snake(self.surface, 3)
                        self.snake.draw()
                        self.apple = Apple(self.surface)
                        self.apple.draw()
                        self.snake.score = 0
                        self.snake.length = 3
                        self.snake.draw()
                        self.apple.move()
                        self.display_score()
                        pygame.display.update()
                    if event.key == pygame.K_LEFT:
                        self.snake.moveLeft()
                    if event.key == pygame.K_RIGHT:
                        self.snake.moveRight()
                    if event.key == pygame.K_UP:
                        self.snake.moveUp()
                    if event.key == pygame.K_DOWN:
                        self.snake.moveDown()
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                
            time.sleep(.075)

    def play(self):
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y, self.snake.direction):
            print(
                "Snake: (" + str(self.snake.x[0]) + "," + str(self.snake.y[0])+")")
            print("Apple: (" + str(self.apple.x) + "," + str(self.apple.y)+")")
            self.snake.increase_length()
            self.apple.move()
            self.snake.score += 10
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i], self.snake.direction):
                print("Collision")
                self.takingInput = True
                raise "Game Over"

        self.snake.walk()
        self.apple.draw()
        # try:
        self.display_score()
        # except error:
        #    print(error)
        pygame.display.flip()

    def display_score(self):
        GAME_FONT = pygame.freetype.Font("roboto-regular.ttf", 24)
        text_surface, rect = GAME_FONT.render("Score: "+ str(self.snake.score), (0, 0, 0))
        self.surface.blit(text_surface, (900, 10))



if __name__ == "__main__":
    game = Game()
    game.run()