import pygame
import math
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tank Movement")



# Get the screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface().get_size()

# Tank sprite class
class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, controls):
        super().__init__()
        try:
            # Load the tank image
            current_dir = os.path.dirname(__file__)
            
            tank_path = os.path.join(current_dir,'Sprites','tank1.png')
            self.original_tank_image = pygame.image.load(tank_path).convert_alpha()
            print(f"Original tank image size: {self.original_tank_image.get_size()}")

            # Scale the tank image to a smaller size
            self.tank_image = pygame.transform.scale(self.original_tank_image, (200, 100))
            print(f"Scaled tank image size: {self.tank_image.get_size()}")
        except pygame.error as e:
            print(f"Failed to load image: {e}")
            pygame.quit()
            exit()

        self.image = self.tank_image
        self.rect = self.tank_image.get_rect(center=(x, y))
        
        self.angle = 0
        self.speed = 0
        self.rotation_speed = 0
        self.controls = controls

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[self.controls['up']]:
            self.speed = 3
        elif keys[self.controls['down']]:
            self.speed = -3
        else:
            self.speed = 0

        if keys[self.controls['left']]:
            self.rotation_speed = 4
        elif keys[self.controls['right']]:
            self.rotation_speed = -4
        else:
            self.rotation_speed = 0

        self.angle += self.rotation_speed
        self.angle %= 360

        self.image = pygame.transform.rotate(self.original_tank_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        angle_rad = math.radians(self.angle)
        dx = math.cos(angle_rad) * self.speed
        dy = math.sin(angle_rad) * self.speed

        self.rect.x += dx
        self.rect.y -= dy

class Gun(pygame.sprite.Sprite):
    def __init__(self, tank, controls):
        super().__init__()

        current_dir = os.path.dirname(__file__)
        gun_path = os.path.join(current_dir,'Sprites', 'gun1.png')
        self.original_gun_image = pygame.image.load(gun_path).convert_alpha()
        self.gun_image = self.original_gun_image
        self.image = self.gun_image
        self.rect = self.gun_image.get_rect(center=tank.rect.center)
        self.angle = 0
        self.rotation_speed = 0
        self.tank = tank
        self.gun_length = -17
        self.gun_rotation_direction = 0
        self.tip_offset = 30
        self.controls = controls

        self.original_gun_length = self.gun_length
        self.gun_back_start_time = 0
        self.gun_back_duration = 200
        self.can_shoot = True
        self.shoot_cooldown = 0
        self.cooldown_duration = 3000
        self.last_update_time = pygame.time.get_ticks()

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[self.controls['rotate_left']]:
            self.rotation_speed = 2
        elif keys[self.controls['rotate_right']]:
            self.rotation_speed = -2
        else:
            self.rotation_speed = 0

        self.angle += self.rotation_speed
        self.angle %= 360
        
        if keys[self.controls['fire']] and self.can_shoot:
            self.gun_back_start_time = pygame.time.get_ticks()  # Start moving the gun back
            bullet_angle = self.angle
            bullet_x = self.rect.centerx + (self.gun_length + self.tip_offset) * math.cos(math.radians(bullet_angle))
            bullet_y = self.rect.centery - (self.gun_length + self.tip_offset) * math.sin(math.radians(bullet_angle))
            bullet = Bullet(bullet_x, bullet_y, bullet_angle, self.gun_length, self.tip_offset)
            all_sprites.add(bullet)
            bullet_sprites.add(bullet)

            self.can_shoot = False
            self.shoot_cooldown = self.cooldown_duration

        elapsed_time = pygame.time.get_ticks() - self.gun_back_start_time
        if elapsed_time <= self.gun_back_duration:
            progress = elapsed_time / self.gun_back_duration
            self.gun_length = self.original_gun_length - 5 * progress
        else:
            self.gun_length = self.original_gun_length

        angle_rad = math.radians(self.angle)
        gun_end_x = self.tank.rect.centerx + (self.gun_length + self.tip_offset) * math.cos(angle_rad)
        gun_end_y = self.tank.rect.centery - (self.gun_length + self.tip_offset) * math.sin(angle_rad)

        rotated_gun_image = pygame.transform.rotate(self.original_gun_image, self.angle)
        self.image = rotated_gun_image
        self.rect = self.image.get_rect(center=(gun_end_x, gun_end_y))

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= pygame.time.get_ticks() - self.last_update_time
        else:
            self.can_shoot = True

        self.last_update_time = pygame.time.get_ticks()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, gun_length, tip_offset):
        super().__init__()
        current_dir = os.path.dirname(__file__)
            
        bullet_path = os.path.join(current_dir, 'bullet.png')
        self.original_bullet_image = pygame.image.load(bullet_path).convert_alpha()
        self.bullet_image = self.original_bullet_image
        self.image = self.bullet_image
        self.angle = angle
        self.speed = 10

        angle_rad = math.radians(self.angle)

        dx = (gun_length + tip_offset - 32) * math.cos(angle_rad)
        dy = -(gun_length + tip_offset - 32) * math.sin(angle_rad)

        self.rect = self.bullet_image.get_rect(center=(x + dx, y + dy))
        self.start_x = self.rect.centerx
        self.start_y = self.rect.centery

    def update(self):
        angle_rad = math.radians(self.angle)
        dx = self.speed * math.cos(angle_rad)
        dy = -self.speed * math.sin(angle_rad)
        self.rect.x += dx
        self.rect.y += dy

# Controls for the first tank
controls_tank1 = {
    'up': pygame.K_w,
    'down': pygame.K_s,
    'left': pygame.K_a,
    'right': pygame.K_d,
    'rotate_left': pygame.K_h,
    'rotate_right': pygame.K_k,
    'fire': pygame.K_j
}

# Controls for the second tank
controls_tank2 = {
    'up': pygame.K_UP,
    'down': pygame.K_DOWN,
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT,
    'rotate_left': pygame.K_COMMA,
    'rotate_right': pygame.K_PERIOD,
    'fire': pygame.K_SLASH
}

#Controls for the third tank
controls_tank3 = {
    'up': pygame.K_g,
    'down': pygame.K_t,
    'left': pygame.K_y,
    'right': pygame.K_r,
    'rotate_left': pygame.K_COMMA,
    'rotate_right': pygame.K_PERIOD,
    'fire': pygame.K_SLASH
}

# Create two tank instances with different controls
tank1 = Tank(375, 300, controls_tank1)
tank2 = Tank(300, 375, controls_tank2)
gun1 = Gun(tank1, controls_tank1)
gun2 = Gun(tank2, controls_tank2)

all_sprites = pygame.sprite.Group()
all_sprites.add(tank1, gun1, tank2, gun2)
bullet_sprites = pygame.sprite.Group()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()
    bullet_sprites.update()

    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    bullet_sprites.draw(screen)
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()