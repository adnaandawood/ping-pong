import pygame
from .paddle import Paddle
from .ball import Ball

# Game Engine

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.win_score = 5  # default win condition
        self.font = pygame.font.SysFont("Arial", 30)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset()

        self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))
    
    
    def check_game_over(self, screen):
    # Determine if the game has reached the win condition
        if self.player_score >= self.win_score or self.ai_score >= self.win_score:
            winner = "Player Wins!" if self.player_score >= self.win_score else "AI Wins!"

            # Display winner message
            screen.fill((0, 0, 0))
            winner_text = self.font.render(winner, True, WHITE)
            options = [
                self.font.render("Press 3 for Best of 3", True, WHITE),
                self.font.render("Press 5 for Best of 5", True, WHITE),
                self.font.render("Press 7 for Best of 7", True, WHITE),
                self.font.render("Press ESC to Exit", True, WHITE),
            ]

            # Center the winner text
            screen.blit(
                winner_text,
                (self.width // 2 - winner_text.get_width() // 2, self.height // 3)
            )

            # Show options below
            for i, opt in enumerate(options):
                screen.blit(
                    opt,
                    (self.width // 2 - opt.get_width() // 2, self.height // 2 + i * 40)
                )

            pygame.display.flip()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_3:
                            self.win_score = 3
                            waiting = False
                        elif event.key == pygame.K_5:
                            self.win_score = 5
                            waiting = False
                        elif event.key == pygame.K_7:
                            self.win_score = 7
                            waiting = False
                        elif event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            return True

            # Reset scores and ball for next round
            self.player_score = 0
            self.ai_score = 0
            self.ball.reset()
            return False

        return False


