import pygame
import random
import sys
import time

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

DEFAULT_KEYS = {
    "haut": pygame.K_UP,
    "bas": pygame.K_DOWN,
    "gauche": pygame.K_LEFT,
    "droite": pygame.K_RIGHT
}

custom_keys = DEFAULT_KEYS.copy()
def show_loading_screen(screen):
    screen.fill(WHITE)
    
    try:
        logo = pygame.image.load("logo.png").convert_alpha()
        logo = pygame.transform.scale(logo, (200, 200))
        logo_rect = logo.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(logo, logo_rect)
    except pygame.error:
        print("Le fichier 'logo.png' n'a pas été trouvé dans le répertoire spécifié.")
    
    pygame.draw.rect(screen, BLACK, (100, SCREEN_HEIGHT // 2 + 50, SCREEN_WIDTH - 200, 25))
    pygame.display.update()
    
    start_time = time.time()
    while time.time() - start_time < 5:
        progress = (time.time() - start_time) / 5
        bar_width = (SCREEN_WIDTH - 200) * progress
        
        pygame.draw.rect(screen, GREEN, (100, SCREEN_HEIGHT // 2 + 50, bar_width, 25))
        pygame.display.update()
        pygame.time.Clock().tick(30)

    fade_out_to_menu(screen)

def fade_out_to_menu(screen):
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill(WHITE)
    for alpha in range(255, 0, -10): 
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.Clock().tick(30)

class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * GRID_SIZE)) % SCREEN_WIDTH), (cur[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
            return True 
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
            return False

    def reset(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, BLACK, r, 1)

    def handle_keys(self, keys):
        for key, direction in keys.items():
            if pygame.key.get_pressed()[key]:
                self.turn(direction)

class Apple:
    def __init__(self):
        self.position = (0, 0)
        self.load_texture()

    def load_texture(self):
        try:
            self.texture = pygame.image.load("apple.png").convert_alpha()
            self.texture = pygame.transform.scale(self.texture, (GRID_SIZE, GRID_SIZE))
        except pygame.error:
            print("Le fichier 'apple.png' n'a pas été trouvé dans le répertoire spécifié.")
            pygame.quit()
            sys.exit()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self, surface):
        surface.blit(self.texture, self.position)

def show_menu():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game")

    font = pygame.font.Font(None, 36)
    play_text = font.render("Jouer", True, BLACK)
    play_rect = play_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    options_text = font.render("Options", True, BLACK)
    options_rect = options_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    quit_text = font.render("Quitter", True, RED)
    quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

    while True:
        screen.fill(WHITE)
        screen.blit(play_text, play_rect)
        screen.blit(quit_text, quit_rect)
        screen.blit(options_text, options_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_rect.collidepoint(mouse_pos):
                    return "play"
                elif quit_rect.collidepoint(mouse_pos):
                    return "quit"
                elif options_rect.collidepoint(mouse_pos):
                    show_options_menu()

def show_options_menu():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Options")

    font = pygame.font.Font(None, 36)
    back_text = font.render("Retour", True, BLACK)
    back_rect = back_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
    validate_text = font.render("Valider", True, BLACK)
    validate_rect = validate_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))

    key_texts = {}
    key_rects = {}

    for idx, (direction, key) in enumerate(custom_keys.items()):
        text = font.render(f"{direction.capitalize()}: {pygame.key.name(key)}", True, BLACK)
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, 50 + idx * 50))
        key_texts[direction] = text
        key_rects[direction] = rect

    while True:
        screen.fill(WHITE)
        screen.blit(back_text, back_rect)
        screen.blit(validate_text, validate_rect)
        for direction in key_texts:
            screen.blit(key_texts[direction], key_rects[direction])
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for direction, rect in key_rects.items():
                    if rect.collidepoint(event.pos):
                        key_pressed = wait_for_key()
                        if key_pressed:
                            custom_keys[direction] = key_pressed
                            key_texts[direction] = font.render(f"{direction.capitalize()}: {pygame.key.name(key_pressed)}", True, BLACK)
                if back_rect.collidepoint(event.pos):
                    return
                elif validate_rect.collidepoint(event.pos):
                    return
                
def wait_for_key():
    while True:
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN:
            return event.key


def show_game_over_menu(screen):
    global score

    font = pygame.font.Font(None, 36)
    game_over_text = font.render("Partie PERDU! :'(", True, RED)
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    score_text = font.render(f"Score: {score}", True, BLACK)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    menu_text = font.render("Menu Principal", True, BLACK)
    menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

    screen.fill(WHITE)
    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    screen.blit(menu_text, menu_rect)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if menu_rect.collidepoint(mouse_pos):
                    return "menu"

score = 0

def draw_score(surface):
    font = pygame.font.Font(None, 24)
    score_text = font.render("Score: " + str(score), True, BLACK)
    score_rect = score_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
    surface.blit(score_text, score_rect)

def play_game(screen):
    global score

    snake = Snake()
    apple = Apple()
    apple.randomize_position()

    clock = pygame.time.Clock() 

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"
        
        keys = {custom_keys["haut"]: UP, custom_keys["bas"]: DOWN, custom_keys["gauche"]: LEFT, custom_keys["droite"]: RIGHT}
        
        snake.handle_keys(keys)
        
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            score += 1

        if snake.move():
            return "game_over"

        screen.fill(WHITE)
        snake.draw(screen)
        apple.draw(screen)
        draw_score(screen)
        pygame.display.update()

        clock.tick(10) 

def start_game():
    global score

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game")
    
    show_loading_screen(screen)

    while True:
        action = show_menu()

        if action == "play":
            score = 0
            result = play_game(screen)
            if result == "game_over":
                action = show_game_over_menu(screen)

        if action == "quit":
            pygame.quit()
            sys.exit()

def main():
    while True:
        start_game()

if __name__ == "__main__":
    main()
