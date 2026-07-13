import pygame
import random
import numpy as np
from enum import Enum
from collections import namedtuple

# Initialize pygame
pygame.init()
font = pygame.font.SysFont('arial', 25)

# Directions the snake can move
class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

# A simple point (x, y) on the grid
Point = namedtuple('Point', 'x, y')

# Colors
WHITE  = (255, 255, 255)
RED    = (200, 0, 0)
BLUE   = (0, 0, 255)
BLUE2  = (0, 100, 255)
BLACK  = (0, 0, 0)
GREEN  = (0, 200, 0)

# Game settings
BLOCK_SIZE = 20   # size of each grid square in pixels
SPEED      = 40   # how fast the game runs (higher = faster training)

class SnakeGameAI:
    def __init__(self, width=640, height=480):
        self.width  = width
        self.height = height

        # Set up the display
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake RL')
        self.clock = pygame.time.Clock()

        # Start a fresh game
        self.reset()

    def reset(self):
        """Reset the game to initial state — called at the start of every new game."""
        self.direction = Direction.RIGHT

        # Snake starts as 3 blocks in the middle of the screen
        self.head = Point(self.width // 2, self.height // 2)
        self.snake = [
            self.head,
            Point(self.head.x - BLOCK_SIZE, self.head.y),
            Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)
        ]

        self.score      = 0
        self.food       = None
        self.frame_iter = 0   # tracks how long the snake has gone without eating

        self._place_food()

    def _place_food(self):
        """Randomly place food somewhere on the grid, not on the snake."""
        x = random.randint(0, (self.width  - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.height - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)

        # If food landed on the snake, try again
        if self.food in self.snake:
            self._place_food()

    def play_step(self, action):
        """
        Run one step of the game.
        action: [1,0,0] = go straight, [0,1,0] = turn right, [0,0,1] = turn left
        Returns: reward, game_over, score
        """
        self.frame_iter += 1

        # 1. Handle quit event (so the window doesn't freeze)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # 2. Move the snake in the chosen direction
        self._move(action)
        self.snake.insert(0, self.head)

        # 3. Check if game over
        reward    = 0
        game_over = False

        # Died by hitting wall or itself, or took too long (stuck in a loop)
        if self.is_collision() or self.frame_iter > 100 * len(self.snake):
            game_over = True
            reward    = -10   # punishment for dying
            return reward, game_over, self.score

        # 4. Check if food was eaten
        if self.head == self.food:
            self.score += 1
            reward = 10       # reward for eating food
            self._place_food()
        else:
            # Remove tail (snake didn't grow)
            self.snake.pop()

        # 5. Update the display
        self._update_ui()
        self.clock.tick(SPEED)

        return reward, game_over, self.score

    def is_collision(self, pt=None):
        """Check if a point collides with a wall or the snake's body."""
        if pt is None:
            pt = self.head

        # Hit a wall
        if pt.x > self.width  - BLOCK_SIZE or pt.x < 0:
            return True
        if pt.y > self.height - BLOCK_SIZE or pt.y < 0:
            return True

        # Hit itself
        if pt in self.snake[1:]:
            return True

        return False

    def _move(self, action):
        """
        Convert action to new direction and update head position.
        Actions are relative: straight, right turn, left turn.
        """
        # Clock-wise direction order
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx        = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]           # no change, go straight
        elif np.array_equal(action, [0, 1, 0]):
            new_dir = clock_wise[(idx + 1) % 4] # turn right
        else:
            new_dir = clock_wise[(idx - 1) % 4] # turn left

        self.direction = new_dir

        x = self.head.x
        y = self.head.y

        if self.direction == Direction.RIGHT: x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:  x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:  y += BLOCK_SIZE
        elif self.direction == Direction.UP:    y -= BLOCK_SIZE

        self.head = Point(x, y)

    def _update_ui(self):
        """Draw everything on screen."""
        self.display.fill(BLACK)

        # Draw snake
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE,  pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))

        # Draw food
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        # Draw score
        text = font.render(f"Score: {self.score}", True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()