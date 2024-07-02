import pygame
import math
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600

# Create the screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tank Movement")



# Get the screen dimensions
screenWidth, screenHeight = pygame.display.get_surface().get_size()

# Tank sprite class
<<<<<<< HEAD
=======
import pygame
import os
import math

>>>>>>> 2a47df1a7d3ab3544beff01cc5225e1634e1af5c
class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, controls):
        super().__init__()
        try:
            # Load the tank image
            currentDir = os.path.dirname(__file__)
            tank_path = os.path.join(currentDir, 'Sprites', 'tank1.png')
            self.originalTankImage = pygame.image.load(tank_path).convert_alpha()
            print(f"Original tank image size: {self.originalTankImage.get_size()}")

            # Scale the tank image to a smaller size
            self.tankImage = pygame.transform.scale(self.originalTankImage, (200, 100))
            print(f"Scaled tank image size: {self.tankImage.get_size()}")
        except pygame.error as e:
            print(f"Failed to load image: {e}")
            pygame.quit()
            exit()

        self.image = self.tankImage
        self.rect = self.tankImage.get_rect(center=(x, y))
        
        self.angle = 0
        self.speed = 0
        self.rotationSpeed = 0
        self.controls = controls
        
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

    def update(self):
        keys = pygame.key.get_pressed()
        
        if keys[self.controls['up']]:
            self.speed = 3
        elif keys[self.controls['down']]:
            self.speed = -3
        else:
            self.speed = 0

        if keys[self.controls['left']]:
            self.rotationSpeed = 4
        elif keys[self.controls['right']]:
            self.rotationSpeed = -4
        else:
            self.rotationSpeed = 0

        self.angle += self.rotationSpeed
        self.angle %= 360

        self.image = pygame.transform.rotate(self.originalTankImage, self.angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))

        angleRad = math.radians(self.angle)
        dx = math.cos(angleRad) * self.speed
        dy = math.sin(angleRad) * self.speed

        self.x += dx
        self.y -= dy

        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)


<<<<<<< HEAD
=======
import pygame
import os
import math

>>>>>>> 2a47df1a7d3ab3544beff01cc5225e1634e1af5c
class Gun(pygame.sprite.Sprite):
    def __init__(self, tank, controls):
        """
        Initializes the Gun class.

        Parameters:
        ----------
        tank : pygame.sprite.Sprite
            The tank object to which the gun is attached.
        controls : dict
            A dictionary mapping control actions (e.g., 'rotate_left', 'fire') to specific keys.
        """
        super().__init__()

        currentDir = os.path.dirname(__file__)
        gunPath = os.path.join(currentDir, 'Sprites', 'gun1.png')
        self.originalGunImage = pygame.image.load(gunPath).convert_alpha()
        self.gunImage = self.originalGunImage
        self.image = self.gunImage
        self.rect = self.gunImage.get_rect(center=tank.rect.center)
        self.angle = 0
        self.rotationSpeed = 0
        self.tank = tank
<<<<<<< HEAD
        self.gunLength = -21
=======
        self.gunLength = -17
>>>>>>> 2a47df1a7d3ab3544beff01cc5225e1634e1af5c
        self.gunRotationDirection = 0
        self.tipOffSet = 30
        self.controls = controls

        self.originalGunLength = self.gunLength
        self.gunBackStartTime = 0
        self.gunBackDuration = 200
        self.canShoot = True
        self.shootCooldown = 0
        self.cooldownDuration = 3000
        self.lastUpdateTime = pygame.time.get_ticks()
        
        # Initialize the gun's floating-point position
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

    def update(self):
        """
        Updates the gun's position, rotation, and shooting state based on the current controls and time.

        This method checks for key presses to rotate the gun, 
        handles shooting if the fire key is pressed, 
        and updates the gun's visual position and rotation. 
        It also manages the shooting cooldown.

        Inputs:
        -------
        None

        Outputs:
        --------
        None
        """
        keys = pygame.key.get_pressed()
        
        # Check what keys are pressed and change rotation speed accordingly
        if keys[self.controls['rotate_left']]:
            self.rotationSpeed = 2
        elif keys[self.controls['rotate_right']]:
            self.rotationSpeed = -2
        elif  keys[self.controls['left']]:
            self.rotationSpeed = 4
        elif keys[self.controls['right']]:
            self.rotationSpeed = -4
        else:
            self.rotationSpeed = 0

        self.angle += self.rotationSpeed
        self.angle %= 360
        
        # Reload cooldown of bullet and determines the angle to fire the bullet,
        # which is relative to the position of the tank gun.
        if keys[self.controls['fire']] and self.canShoot:
            self.gunBackStartTime = pygame.time.get_ticks()  # Start moving the gun back
            bulletAngle = self.angle
            bulletX = self.rect.centerx + (self.gunLength + self.tipOffSet) * math.cos(math.radians(bulletAngle))
            bulletY = self.rect.centery - (self.gunLength + self.tipOffSet) * math.sin(math.radians(bulletAngle))
            bullet = Bullet(bulletX, bulletY, bulletAngle, self.gunLength, self.tipOffSet)
            allSprites.add(bullet)
            bulletSprites.add(bullet)

            self.canShoot = False
            self.shootCooldown = self.cooldownDuration

        # Handle the gun back movement when shooting
        elapsedTime = pygame.time.get_ticks() - self.gunBackStartTime
        if elapsedTime <= self.gunBackDuration:
            progress = elapsedTime / self.gunBackDuration
            self.gunLength = self.originalGunLength - 5 * progress
        else:
            self.gunLength = self.originalGunLength

        angleRad = math.radians(self.angle)
        gunEndX = self.tank.rect.centerx + (self.gunLength + self.tipOffSet) * math.cos(angleRad)
        gunEndY = self.tank.rect.centery - (self.gunLength + self.tipOffSet) * math.sin(angleRad)

        rotatedGunImage = pygame.transform.rotate(self.originalGunImage, self.angle)
        self.image = rotatedGunImage
        self.rect = self.image.get_rect(center=(gunEndX, gunEndY))

        # Handle shooting cooldown
        if self.shootCooldown > 0:
            self.shootCooldown -= pygame.time.get_ticks() - self.lastUpdateTime
        else:
            self.canShoot = True

        self.lastUpdateTime = pygame.time.get_ticks()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, gunLength, tipOffSet):
        """
        Initializes the Bullet class.

        Parameters:
        ----------
        x : int
            The x-coordinate of the bullet's starting position.
        y : int
            The y-coordinate of the bullet's starting position.
        angle : float
            The angle at which the bullet is fired.
        gunLength : float
            The length of the gun.
        tipOffSet : float
            The offset from the gun's tip to the bullet's starting position.
        """
        super().__init__()
        currentDir = os.path.dirname(__file__)
            
        bulletPath = os.path.join(currentDir, 'bullet.png')
        self.originalBulletImage = pygame.image.load(bulletPath).convert_alpha()
        self.bulletImage = self.originalBulletImage
        self.image = self.bulletImage
        self.angle = angle
        
        self.speed = 2

        angleRad = math.radians(self.angle)
        dx = (gunLength + tipOffSet - 32) * math.cos(angleRad)
        dy = -(gunLength + tipOffSet - 32) * math.sin(angleRad)
        
        self.rect = self.bulletImage.get_rect(center=(x + dx, y + dy))
        self.x = self.rect.centerx
        self.y = self.rect.centery

    def update(self):
        """
        Updates the bullet's position based on its speed and direction.

        This method calculates the new position of the bullet and updates its rect attribute accordingly.

        Inputs:
        -------
        None

        Outputs:
        --------
        None
        """
        angleRad = math.radians(self.angle)
        dx = self.speed * math.cos(angleRad)
        dy = -self.speed * math.sin(angleRad)
        
        self.x += dx
        self.y += dy
        
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
# Controls for the first tank
controlsTank1 = {
    'up': pygame.K_w,
    'down': pygame.K_s,
    'left': pygame.K_a,
    'right': pygame.K_d,
    'rotate_left': pygame.K_h,
    'rotate_right': pygame.K_k,
    'fire': pygame.K_j
}

# Controls for the second tank
controlsTank2 = {
    'up': pygame.K_UP,
    'down': pygame.K_DOWN,
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT,
    'rotate_left': pygame.K_COMMA,
    'rotate_right': pygame.K_PERIOD,
    'fire': pygame.K_SLASH
}

# Create two tank instances with different controls
tank1 = Tank(375, 300, controlsTank1)
tank2 = Tank(300, 375, controlsTank2)
gun1 = Gun(tank1, controlsTank1)
gun2 = Gun(tank2, controlsTank2)

allSprites = pygame.sprite.Group()
allSprites.add(tank1, gun1, tank2, gun2)
bulletSprites = pygame.sprite.Group()

running = True

#Updating GUI while window is open
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    allSprites.update()
    bulletSprites.update()

    screen.fill((255, 255, 255))
    allSprites.draw(screen)
    bulletSprites.draw(screen)
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
