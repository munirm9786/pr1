import pygame
import random
import time

# Window size
WINDOW_X = 720
WINDOW_Y = 480

# Defining colors
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)

class SnakeGame:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up the game window
        self.window_x = WINDOW_X
        self.window_y = WINDOW_Y
        self.game_window = pygame.display.set_mode((self.window_x, self.window_y))
        pygame.display.set_caption('Snake Game')

        # Set up the clock for controlling the frame rate
        self.fps = pygame.time.Clock()

        # Initialize Pygame mixer for sound
        pygame.mixer.init()

        # Load eating sound
        self.eating_sound = pygame.mixer.Sound('eating_sound.wav')  # Replace with the actual filename of your sound file

        # Snake properties
        self.snake_speed = 15
        self.snake_position = [100, 50]
        self.snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]

        # Fruit properties
        self.fruit_position = [random.randrange(1, (self.window_x // 10)) * 10,
                                random.randrange(1, (self.window_y // 10)) * 10]
        self.fruit_spawn = True

        # Initial direction of the snake
        self.direction = 'RIGHT'
        self.change_to = self.direction

        # Score and colors
        self.score = 0
        self.colors = [GREEN, RED]

        # Load background image
        self.background = pygame.image.load('background.jpg')
        self.background = pygame.transform.scale(self.background, (self.window_x, self.window_y))

    def show_score(self):
        # Set up font for displaying the score
        bubble_font = 'Anton_Regular.ttf'
        font = pygame.font.Font(bubble_font, 30)

        # Create surface for the score
        score_surface = font.render('Score : ' + str(self.score), True, WHITE)
        score_rect = score_surface.get_rect()
        score_rect.midtop = (self.window_x / 2, self.window_y / 4)

        # Display the score on the game window
        self.game_window.blit(score_surface, score_rect)

    def game_over(self):
        # Set up font for displaying the game over message
        font = pygame.font.Font('Anton_Regular.ttf', 50)

        # Create surface for the game over message
        game_over_surface = font.render('Your Score is : ' + str(self.score), True, RED)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (self.window_x / 2, self.window_y / 4)

        # Display the game over message on the game window
        self.game_window.blit(game_over_surface, game_over_rect)

        # Update the display
        pygame.display.flip()

        # Wait for 2 seconds
        time.sleep(2)

        # Quit Pygame
        pygame.mixer.quit()
        pygame.quit()
        quit()

    def run_game(self):
        while True:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.change_to = 'UP'
                    if event.key == pygame.K_DOWN:
                        self.change_to = 'DOWN'
                    if event.key == pygame.K_LEFT:
                        self.change_to = 'LEFT'
                    if event.key == pygame.K_RIGHT:
                        self.change_to = 'RIGHT'

            # Change direction based on key inputs
            if self.change_to == 'UP' and self.direction != 'DOWN':
                self.direction = 'UP'
            if self.change_to == 'DOWN' and self.direction != 'UP':
                self.direction = 'DOWN'
            if self.change_to == 'LEFT' and self.direction != 'RIGHT':
                self.direction = 'LEFT'
            if self.change_to == 'RIGHT' and self.direction != 'LEFT':
                self.direction = 'RIGHT'

            # Move the snake
            if self.direction == 'UP':
                self.snake_position[1] -= 10
            if self.direction == 'DOWN':
                self.snake_position[1] += 10
            if self.direction == 'LEFT':
                self.snake_position[0] -= 10
            if self.direction == 'RIGHT':
                self.snake_position[0] += 10

            # Update snake body and check for collisions
            self.snake_body.insert(0, list(self.snake_position))
            if self.snake_position[0] == self.fruit_position[0] and self.snake_position[1] == self.fruit_position[1]:
                self.score += 10
                self.fruit_spawn = False
                self.eating_sound.play()  # Play the sound effect
            else:
                self.snake_body.pop()

            # Spawn new fruit if the previous one is consumed
            if not self.fruit_spawn:
                self.fruit_position = [random.randrange(1, (self.window_x // 10)) * 10,
                                        random.randrange(1, (self.window_y // 10)) * 10]

            self.fruit_spawn = True

            # Draw the background
            self.game_window.blit(self.background, (0, 0))

            # Draw the snake
            for pos in self.snake_body:
                pygame.draw.rect(self.game_window, self.colors[0], pygame.Rect(pos[0], pos[1], 10, 10))

            # Draw the fruit
            pygame.draw.rect(self.game_window, self.colors[1], pygame.Rect(self.fruit_position[0], self.fruit_position[1], 10, 10))

            # Check for collisions with window borders
            if self.snake_position[0] < 0 or self.snake_position[0] > self.window_x - 10:
                self.game_over()
            if self.snake_position[1] < 0 or self.snake_position[1] > self.window_y - 10:
                self.game_over()

            # Check for collisions with itself
            for block in self.snake_body[1:]:
                if self.snake_position[0] == block[0] and self.snake_position[1] == block[1]:
                    self.game_over()

            # Display the score
            self.show_score()

            # Update the display
            pygame.display.update()

            # Control the frame rate
            self.fps.tick(self.snake_speed)

if __name__ == "__main__":
    # Run the game
    game = SnakeGame()
    game.run_game()
