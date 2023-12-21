import pygame
from pygame.locals import *
from sys import exit
import os
from random import randrange, choice


pygame.init()
pygame.mixer.init()

main_directory = os.path.dirname(__file__)
alien_directory = os.path.join(main_directory, 'alien')
sound_directory = os.path.join(main_directory, 'sons')

width = 640
height = 480
white = (255, 255, 255)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Alien Invasion')

sprite_sheet = pygame.image.load(os.path.join(alien_directory, 'alien.png')).convert_alpha()

sound_collide = pygame.mixer.Sound(os.path.join(sound_directory, 'death_sound.wav'))
sound_collide.set_volume(1)

sound_pontuation = pygame.mixer.Sound(os.path.join(sound_directory, 'score_sound.wav'))
sound_pontuation.set_volume(1)

colize = False

choice_adversity = choice([0, 1])
points = 0
velocity_game = 10

def message_screen(msg, size_font, color_font):
    font = pygame.font.SysFont('comicsansms', size_font, True, False)
    msgt = f'{msg}'
    formated_text = font.render(msgt, True, color_font)
    return formated_text

def restart_game():
    global points, velocity_game, colize, choice_adversity
    points = 0
    velocity_game = 0
    colize = False
    alien.rect.y = height - 80 - 96 // 2
    alien.jumpil = False
    devil.rect.x = width
    monster.rect.x = width
    choice_adversity = choice([0, 1])

class Alien(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sound_jump = pygame.mixer.Sound(os.path.join(sound_directory, 'jump_sound.wav'))
        self.sound_jump.set_volume(1)
        self.image_alien = []
        for c in range(3):
            img = sprite_sheet.subsurface((c * 32, 0), (32, 32))
            img = pygame.transform.scale(img, (32 * 3, 32 * 3))
            self.image_alien.append(img)

        self.index_array = 0
        self.image = self.image_alien[self.index_array]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.pos_y_initial = height - 80 - 96 // 2
        self.rect.center = (100, height - 80)
        self.jumpil = False
        self.jump_height = 200 # Altura máxima do pulo
        self.jump_speed = 5  # Velocidade do pulo

    def perform_jump(self):
        if not self.jumpil:
            self.jumpil = True
            self.sound_jump.play()

    def update(self):
        if self.jumpil:
            if self.rect.y > self.pos_y_initial - self.jump_height:
                self.rect.y -= self.jump_speed
            else:
                self.jumpil = False
        elif self.rect.y < self.pos_y_initial:
            self.rect.y += self.jump_speed
        else:
            self.rect.y = self.pos_y_initial

        if self.index_array > 2:
            self.index_array = 0
        self.index_array += 0.25
        self.image = self.image_alien[int(self.index_array)]


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((6 * 32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32 * 3, 32 * 3))
        self.rect = self.image.get_rect()
        self.rect.y = randrange(50, 200, 50)
        self.rect.x = width - randrange(30, 300, 90)

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = width
            self.rect.y = randrange(50, 200, 50)
        self.rect.x -= velocity_game


class Floor(pygame.sprite.Sprite):
    def __init__(self, pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((7 * 32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32 * 2, 32 * 2))
        self.rect = self.image.get_rect()
        self.rect.y = height - 64
        self.rect.x = pos_x * 64

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = width

        self.rect.x -= 10

class Monster(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((3 * 32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32 * 2, 32 * 2))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.choice = choice_adversity
        self.rect.center = (width, height - 64)
        self.rect.x = width

    def update(self):
        if self.choice == 0:
            if self.rect.topright[0] < 0:
                self.rect.x = width
            self.rect.x -= velocity_game


class Devil(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.alien_image = []
        for i in range(4, 6):
            img = sprite_sheet.subsurface((i * 32, 0), (32, 32))
            img = pygame.transform.scale(img, (32 * 2, 32 * 2))
            self.alien_image.append(img)

        self.index_array = 0
        self.image = self.alien_image[self.index_array]
        self.mask = pygame.mask.from_surface(self.image)
        self.choice = choice_adversity
        self.rect = self.image.get_rect()
        self.rect.center = (width, 250)
        self.rect.x = width

    def update(self):
        if self.choice == 1:
            if self.rect.topright[0] < 0:
                self.rect.x = width
            self.rect.x -= velocity_game

            if self.index_array > 1:
                self.index_array = 0
            self.index_array += 0.25
            self.image = self.alien_image[int(self.index_array)]


todas_as_sprites = pygame.sprite.Group()
alien = Alien()
todas_as_sprites.add(alien)
oclock = pygame.time.Clock()

for c in range(4):
    cloud = Cloud()
    todas_as_sprites.add(cloud)

for c in range(width * 2 // 64):
    floor = Floor(c)
    todas_as_sprites.add(floor)


monster = Monster()
todas_as_sprites.add(monster)

devil = Devil()
todas_as_sprites.add(devil)

group_adversity = pygame.sprite.Group()
group_adversity.add(monster)
group_adversity.add(devil)

while True:
    oclock.tick(30)
    screen.fill(white)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if alien.rect.y != alien.pos_y_initial:
                    pass
                else:
                   alien.perform_jump()

            if event.key == K_r:
                restart_game()

    colisions = pygame.sprite.spritecollide(alien, group_adversity, True, pygame.sprite.collide_mask)

    todas_as_sprites.draw(screen)

    if monster.rect.topright[0] <= 0 or devil.rect.topright[0] <= 0:
        choice_adversity = choice([0, 1])
        monster.rect.x = width
        devil.rect.x = width
        monster.choice = choice_adversity
        devil.choice = choice_adversity

    if colisions and colize == False:
        sound_collide.play()
        colize = True
    if colize == True:
        if points % 100 == 0:
            points += 1
        game_over = message_screen('GAME OVER', 40, (0, 0, 0))
        screen.blit(game_over, (width// 2, height// 2))
        restart = message_screen('Pressione R para Reiniciar', 20, (0, 0, 0))
        screen.blit(restart, (width// 2, (height// 2) + 60))

    else:
        points += 1
        todas_as_sprites.update()
        points_text = message_screen(points, 40, (0, 0, 0))

    if points % 100 == 0:
        sound_pontuation.play()
        if velocity_game >= 33:
            velocity_game += 0
        else:
            velocity_game += 10


    screen.blit(points_text, (520, 30))

    todas_as_sprites.update()

    pygame.display.flip()
