import pygame
import sys

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
BALL_SIZE = 20
FPS = 60
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# Инициализация экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пинг-Понг")
clock = pygame.time.Clock()

# Шрифты
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def main_menu():
    while True:
        screen.fill(BLACK)
        draw_text("ПИНГ-ПОНГ", font, GREEN, WIDTH // 2 - 180, HEIGHT // 4)
        draw_text("Нажмите 1 - Один игрок", small_font, WHITE, WIDTH // 2 - 150, HEIGHT // 2 - 30)
        draw_text("Нажмите 2 - Два игрока", small_font, WHITE, WIDTH // 2 - 150, HEIGHT // 2 + 10)
        draw_text("Используйте клавиши 1 и 2 для выбора", small_font, WHITE, WIDTH // 2 - 200, HEIGHT // 2 + 50)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1
                elif event.key == pygame.K_2:
                    return 2

def get_max_score():
    input_active = True
    max_score = ""
    while input_active:
        screen.fill(BLACK)
        draw_text("Введите счет для победы:", small_font, WHITE, WIDTH // 2 - 150, HEIGHT // 2)
        draw_text("Используйте цифры и Enter", small_font, WHITE, WIDTH // 2 - 150, HEIGHT // 2 + 30)
        draw_text(max_score, small_font, GREEN, WIDTH // 2, HEIGHT // 2 + 60)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and max_score.isdigit() and int(max_score) > 0:
                    return int(max_score)
                elif event.key == pygame.K_BACKSPACE:
                    max_score = max_score[:-1]
                else:
                    max_score += event.unicode

def game_loop(players, max_score):
    # Инициализация объектов
    paddle1 = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    paddle2 = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
    ball_speed = [4, 4]
    score1, score2 = 0, 0

    while True:
        screen.fill(BLACK)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Управление платформами
        keys = pygame.key.get_pressed()
        if players == 2:
            if keys[pygame.K_w] and paddle1.top > 0:
                paddle1.y -= 5
            if keys[pygame.K_s] and paddle1.bottom < HEIGHT:
                paddle1.y += 5
            if keys[pygame.K_UP] and paddle2.top > 0:
                paddle2.y -= 5
            if keys[pygame.K_DOWN] and paddle2.bottom < HEIGHT:
                paddle2.y += 5
        else:
            if keys[pygame.K_w] and paddle1.top > 0:
                paddle1.y -= 5
            if keys[pygame.K_s] and paddle1.bottom < HEIGHT:
                paddle1.y += 5
            # Автоматическое управление второй платформой
            if ball.centery < paddle2.centery and paddle2.top > 0:
                paddle2.y -= 4
            if ball.centery > paddle2.centery and paddle2.bottom < HEIGHT:
                paddle2.y += 4

        # Движение мяча
        ball.x += ball_speed[0]
        ball.y += ball_speed[1]

        # Отскок от стен
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed[1] = -ball_speed[1]

        # Проверка столкновений с платформами
        if ball.colliderect(paddle1) or ball.colliderect(paddle2):
            ball_speed[0] = -ball_speed[0]

        # Проверка забивания гола
        if ball.left <= 0:
            score2 += 1
            ball.x, ball.y = WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2
            ball_speed = [4, 4]
        if ball.right >= WIDTH:
            score1 += 1
            ball.x, ball.y = WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2
            ball_speed = [-4, 4]

        # Отрисовка объектов
        pygame.draw.rect(screen, GREEN, paddle1)
        pygame.draw.rect(screen, GREEN, paddle2)
        pygame.draw.ellipse(screen, GREEN, ball)
        pygame.draw.aaline(screen, GREEN, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        # Отображение счета
        draw_text(f"{score1}", font, WHITE, WIDTH // 4, 50)
        draw_text(f"{score2}", font, WHITE, WIDTH * 3 // 4 - 50, 50)

        # Проверка победы
        if score1 >= max_score or score2 >= max_score:
            return score1, score2

        pygame.display.flip()
        clock.tick(FPS)

def end_screen(score1, score2):
    while True:
        screen.fill(BLACK)
        draw_text("ИГРА ОКОНЧЕНА", font, GREEN, WIDTH // 2 - 250, HEIGHT // 4)
        draw_text(f"Игрок 1: {score1}", small_font, WHITE, WIDTH // 2 - 100, HEIGHT // 2 - 30)
        draw_text(f"Игрок 2: {score2}", small_font, WHITE, WIDTH // 2 - 100, HEIGHT // 2)
        draw_text("Нажмите ESC для выхода", small_font, WHITE, WIDTH // 2 - 150, HEIGHT // 2 + 50)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

# Главный цикл программы
if __name__ == "__main__":
    players = main_menu()
    max_score = get_max_score()
    score1, score2 = game_loop(players, max_score)
    end_screen(score1, score2)