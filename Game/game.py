import numpy as np
import pygame
import random
from enum import Enum
from collections import namedtuple


pygame.init()
# font = pygame.font.Font('arial.ttf', 25)
font = pygame.font.SysFont("Arial", 20)
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)


class Direction(Enum):
    RIGHT = 1
    LEFT  = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x,y')

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

BLOCK_SIZE = 20
SPEED = 40

class SnakeGame:

    def __init__(self,w=640, h=480):
        self.w = w
        self.h = h

        # display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake AI Game')
        self.clock = pygame.time.Clock()
        self.reset()


    def reset(self):
        # init the game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head,
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2*BLOCK_SIZE), self.head.y)
                      ]

        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0


    def _place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x,y)
        if self.food in self.snake:
            self._place_food()


    def play_step(self, action):
        self.frame_iteration += 1
        #collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # elif event.type == pygame.VIDEORESIZE :
                # screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)


        # screen.fill((30,30,30))
        # pygame.display.flip()
        self._move(action)
        self.snake.insert(0, self.head)

        #check if the game is over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100 * len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # place the new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else :
            self.snake.pop()

        # update ui and the clock
        self._update_ui()
        self.clock.tick(SPEED)

        #return game over and score
        return reward, game_over, self.score

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head

        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True

        # hit itself
        if pt in self.snake[1:]:
            return True

        return False

    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score :" + str(self.score), True, WHITE)
        self.display.blit(text, [0,0])
        pygame.display.flip()


    def _move(self, action):
        #straight, right, left
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1,0,0]):
            new_dir = clock_wise[idx]    # no change at all
        elif np.array_equal(action, [0,1,0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # right turn r-> d-> l-> u
        else :
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] # left turn r-> u-> l-> d

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x,y)


