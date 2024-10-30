import pygame
import sys
import random
import os
from GB import GameButton
pygame.init()
pygame.mixer.init()


pathh = os.path.dirname(__file__)
SCREEN_WIDTH= 600
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Racket(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 100
        self.height = 20
        self.color = (255, 255, 255)
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.score = 0

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.radius = 10
        self.color = (255, 255, 255)
        self.speed = 3.5
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(x, y))

        self.direction = self.get_initial_direction()
        self.colliding_with_racket1 = False

    def get_initial_direction(self):
        random_angle = (random.uniform(-1, 1), random.uniform(-1, 1))
        while abs(random_angle[1]) < 0.2:
            random_angle = (random.uniform(-1, 1), random.uniform(-1, 1))
        return pygame.Vector2(random_angle).normalize()

    def update(self, racket_group):
        self.rect.center += self.direction * self.speed
        self.check_wall_collisions()
        self.check_racket_collisions(racket_group)

    def check_wall_collisions(self):
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.direction.x *= -1
            sound_fx['Hit'].play()
            self.direction.x = self.normalize_direction(self.direction.x, 0.3, 0.2)

            if self.rect.left < 0:
                self.rect.left = 0
            elif self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH

        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.direction.y *= -1
            sound_fx['Hit'].play()
            self.direction.y = self.normalize_direction(self.direction.y, 0.2, 0.3)

            if self.rect.top < 0:
                self.rect.top = 0
            elif self.rect.bottom > SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT

    def check_racket_collisions(self, racket_group):
        for racket in racket_group:
            if self.rect.colliderect(racket):
                if not self.colliding_with_racket1:  
                    self.handle_collision(racket)
                    sound_fx['Hit'].play()
                    self.colliding_with_racket1 = True  
            else:
                if abs(self.rect.centery - racket.rect.centery) > 50:
                    self.colliding_with_racket1 = False

    def handle_collision(self, racket):
        self.direction.y *= -1
        if self.direction.y > 0:
            self.rect.top = racket.rect.bottom
        else:
            self.rect.bottom = racket.rect.top

    def normalize_direction(self, value, threshold, min_value):
        if abs(value) < threshold:
            return min_value * (-1 if value < 0 else 1)
        return value

def load_sound(file_path, volume=0.2):
    sound = pygame.mixer.Sound(file_path)
    sound.set_volume(volume)
    return sound

sound_fx = {
    'Hit': load_sound(r"C:\Users\panos\Desktop\TESTPY\pong.mp3", 0.4)
}

ball_group = pygame.sprite.Group()
ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
ball_group.add(ball)

racket = Racket((SCREEN_WIDTH - 100) // 2, SCREEN_HEIGHT - 40)
racket2 = Racket((SCREEN_WIDTH - 100) // 2, 40)
racket_group = pygame.sprite.Group()
racket_group.add(racket)
racket_group.add(racket2)

clock = pygame.time.Clock()

def add_ball(x, y):
    new_ball = Ball(x, y)
    ball_group.add(new_ball)

def draw_text(text, color, x, y):
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, color)
    text_x = x - text_surface.get_width() // 2
    screen.blit(text_surface, (text_x, y))

def ai_control(racket, balls):
    closest_ball = None
    min_distance = None
 
    for ball in balls:
        distance = abs(ball.rect.centery - racket.rect.centery)
        if ball.rect.centery < SCREEN_HEIGHT // 2 and ball.direction[1] < 0:
            if min_distance is None or distance < min_distance: # I DO NOT put min_distance is None as the second parameter because the programm will crash when comparing int and NoneType
                min_distance = distance
                closest_ball = ball


    if closest_ball:
        horizontal_distance = closest_ball.rect.centerx - racket.rect.centerx
        speed = horizontal_distance * 0.07
        racket.rect.x += speed

    if racket.rect.left < 0:
        racket.rect.left = 0
    if racket.rect.right > SCREEN_WIDTH:
        racket.rect.right = SCREEN_WIDTH
def load_image(file_path, scale=None):
        image = pygame.image.load(file_path).convert_alpha()
        if scale:
            image = pygame.transform.scale(image, scale)
        return image
    
button_images = {
        'start': load_image(f'{pathh}/start_btn.png',(250,75)),
        'exit': load_image(f'{pathh}/exit_btn.png', (250,75)),
}
BACKGROUND_COLOR= (149, 123, 123)
        

start_button =GameButton(SCREEN_HEIGHT//2-120 ,SCREEN_WIDTH//2-150,button_images['start'],False)
exit_button = GameButton(SCREEN_HEIGHT//2 -120,SCREEN_WIDTH//2,button_images['exit'],False)
run= True
start_game= False
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if not start_game:
        pygame.display.set_caption('PANOS KENTROS UNIWA')
        screen.fill(BACKGROUND_COLOR)
        if start_button.draw(screen):
            start_game = True

        if exit_button.draw(screen):
            run = False
    else:

        ai_control(racket2, ball_group)

        for ball in ball_group:
            if ball.rect.bottom > racket.rect.bottom:
                racket2.score += 1
                ball_group.remove(ball)
            elif ball.rect.top < racket2.rect.top:
                racket.score += 1
                ball_group.remove(ball)

        screen.fill(BACKGROUND_COLOR)
        ball_group.update(racket_group)
        ball_group.draw(screen)
        racket_group.draw(screen)

        pygame.display.set_caption(f' PRESS SPACE TO ADD MORE BALLS | BALLS: {len(ball_group)}')
        draw_text(f'Score: {racket.score}', (255, 255, 255), SCREEN_WIDTH // 2, SCREEN_HEIGHT - 23)
        draw_text(f'Score: {racket2.score}', (255, 255, 255), SCREEN_WIDTH // 2, 10)


        
        for event in events:
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                add_ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        if keys[pygame.K_LEFT] and racket.rect.left > 0:
            racket.rect.x -= 15
        if keys[pygame.K_RIGHT] and racket.rect.right < SCREEN_WIDTH:
            racket.rect.x += 15

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
