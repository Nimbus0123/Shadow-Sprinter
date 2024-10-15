import pygame
import pygame.sprite
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.player_run = []
        directory = "data/"
        
        # player animation
        for i in range(1, 7):
            file_path = directory + f"Player/Run{i}.png"
            player_image = pygame.image.load(file_path).convert_alpha()
            scaled_image = pygame.transform.scale(player_image, (100, 100))
            self.player_run.append(scaled_image)
        
        # Player settings
        self.player_index = 0
        self.player_jump = pygame.image.load("data/Player/Jump4.png").convert_alpha()
        self.player_jump = pygame.transform.scale(self.player_jump, (100, 100))
        self.image = self.player_run[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 350))
        self.gravity = 0

    # Jump
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and (self.rect.bottom >= 350):
            self.gravity = -21

    # Gravity
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 350:
            self.rect.bottom = 350

    # Player animation
    def animation_state(self):
        if self.rect.bottom < 350:
            self.image = self.player_jump
        else:
            self.player_index += 0.15
            if self.player_index >= len(self.player_run):
                self.player_index = 0
            self.image = self.player_run[int(self.player_index)]

    def main_menu_animation(self):
        self.player_index += 0.15
        if self.player_index >= len(self.player_run):
            self.player_index = 0
        self.image = self.player_run[int(self.player_index)]
        self.rect.center = (300, 200)

    def reset_position(self):
        self.gravity = 0 
        self.rect.midbottom = (80,350)

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.frames = []
        directory = "data/"

        # bat animation
        if type == "bat":
            for i in range(1, 5):
                file_path = directory + f"Enemies/Bat/bat{i}.png"
                bat_image = pygame.image.load(file_path).convert_alpha()
                scaled_bat_image = pygame.transform.scale(bat_image, (75, 75))
                self.frames.append(scaled_bat_image)            

            y_pos = randint(200, 230)
        
        # slime animation
        else:           
            for i in range(1, 5):
                file_path = directory + f"Enemies/Slime/slime{i}.png"
                slime_image = pygame.image.load(file_path).convert_alpha()
                scaled_slime_image = pygame.transform.scale(slime_image, (60, 75))
                self.frames.append(scaled_slime_image)
                
            y_pos = 355

        # Enemy settings
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(700, 900), y_pos))

    # Enemy animation
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        if self.rect.x < -50:
            self.kill()

    def update(self):
        global score
        if self.rect.right > -4 and self.rect.right < 3:
            score += 1
        self.animation_state()
        self.rect.x -= 6

# Collision
def collision_sprite():
    global high_score
    if pygame.sprite.spritecollide(player.sprite, enemy_group, False):
        enemy_group.empty()
        if high_score < score:
            high_score = score
        return False
    else:
        return True

# Score
def active_text():
    score_surf = score_font.render(f"Score: {score}", False, "Black")
    score_rect = score_surf.get_rect(topleft = (20, 25))
    attempt_text = score_font.render(f"Attempts: {attempts}", False, "Black")
    attempt_text_rect = attempt_text.get_rect(topright = (580, 25))   
    screen.blit(attempt_text, attempt_text_rect)
    screen.blit(score_surf, score_rect)

def main_menu():

    # Text box variables
    score_message = score_font.render(f"Your Score: {score}", False, "Black")
    score_message_rect = score_message.get_rect(center = (300, 300))
    high_score_text = score_font.render(f"High Score: {high_score}", False, "Black")
    high_score_text_rect = high_score_text.get_rect(center = (300, 350))
    high_score_message = score_font.render(f"New High Score!", False, "Black")
    high_score_message_rect = high_score_message.get_rect(center = (300, 300))
    game_name = menu_font.render("Shadow Sprinter", False, "Black")
    game_name_rect = game_name.get_rect(center = (300, 50))
    game_message = menu_font.render("Press SPACE to start", False, "Black")
    game_message_rect = game_message.get_rect(center = (300, 350))

    # Drawing text boxes
    screen.blit(game_name, game_name_rect)
    if attempts == 0:
        screen.blit(game_message, game_message_rect)
    elif score == high_score:
        screen.blit(high_score_text, high_score_text_rect)
        screen.blit(high_score_message, high_score_message_rect)
    else:
        screen.blit(score_message, score_message_rect)
        screen.blit(high_score_text, high_score_text_rect)

# Settings
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Shadow Sprinter")
clock = pygame.time.Clock()
score_font = pygame.font.Font("data/font/Modern Pixels.ttf", 35)
menu_font = pygame.font.Font("data/font/Modern Pixels.ttf", 50)
game_active = False
score = 0
attempts = 0
try:
    with open("data/highscore.txt", "r") as file:
        high_score = int(file.read())
except FileNotFoundError:
    high_score = 0
except ValueError:
    high_score = 0

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())
enemy_group = pygame.sprite.Group()

# Background
sky_surf = pygame.image.load("data/Background/background.png").convert_alpha()
ground_surf = pygame.image.load("data/Background/ground.png").convert_alpha()

# Timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1200)

# Main game loop
while True:

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open("data/highscore.txt", "w") as file:
                file.write(str(high_score))       
            pygame.quit()
            exit()

        if game_active == False:
                if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    game_active = True
                    score = 0
                    attempts += 1
                    player.sprite.reset_position()                       

        if game_active:
            if event.type == obstacle_timer:
                enemy_group.add(Enemy(choice(["bat", "slime", "slime"])))

    # Gameplay
    if game_active:
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 350))
        active_text()

        player.draw(screen)
        player.update()
        enemy_group.draw(screen)
        enemy_group.update()
        game_active = collision_sprite()

    # Menu
    else:
        screen.blit(sky_surf, (0, 0))
        player.draw(screen)
        player.sprite.main_menu_animation()
        main_menu()
        
    pygame.display.update()
    clock.tick(60)