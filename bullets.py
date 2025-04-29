import pygame
import sys
import os
import math
import constants as const
from ColorDictionary import ColourDictionary as c # colors
import copy
import globalVariables as g


class Bullet(pygame.sprite.Sprite):

    originalCollision = True
    name = "Default"
    initialX = 0
    initialY = 0
    selfCollision = False
    originalBounce = 1
    def __init__(self, x, y, angle, gunLength, tipOffSet, gunOwner):
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
        if getattr(sys, 'frozen', False):  # Running as an .exe
            currentDir = sys._MEIPASS
        else:  # Running as a .py script
            currentDir = os.path.dirname(os.path.abspath(__file__))
            
        bulletPath = os.path.join(currentDir, './Assets/bullet.png')
        self.originalBulletImage = pygame.image.load(bulletPath).convert_alpha()
        self.bulletImage = self.originalBulletImage
        self.image = self.bulletImage
        self.angle = angle
        self.speed = 12
        self.drawable = False
        self.trail = False
        angleRad = math.radians(self.angle)

        dx = (gunLength + tipOffSet) * math.cos(angleRad)
        dy = -(gunLength + tipOffSet) * math.sin(angleRad)

        self.rect = self.bulletImage.get_rect(center=(x + dx, y + dy))
        self.x = self.rect.centerx
        self.y = self.rect.centery
        self.trailX =  self.rect.centerx
        self.trailY = self.rect.centery
        self.bounce = 1
        self.originalBounce = self.bounce
        self.corners = [(self.rect.x, self.rect.y), (self.rect.x + self.rect.width, self.rect.y),
                        (self.rect.x + self.rect.width, self.rect.y + self.rect.height), (self.rect.x, self.rect.y + self.rect.height)]
        self.damage = 700
        self.pleaseDraw = False
        self.initialX = x
        self.initialY = y
        self.deltaTime = 0
        self.gunOwner = gunOwner # who shot ya 

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
        # Calculate angle in radians
        angleRad = math.radians(self.angle)

        # Calculate the change in x and y
        dx = self.speed * math.cos(angleRad)
        dy = -self.speed * math.sin(angleRad)

        # Set the maximum step size
        max_step = 0.1

        # Track the progress along dx and dy
        remaining_dx = dx
        remaining_dy = dy
        # Continue while there's still distance to cover in either direction
        while abs(remaining_dx) > 0 or abs(remaining_dy) > 0:
            # Determine the step size, which should be limited to max_step
            step_dx = max(-max_step, min(max_step, remaining_dx))
            step_dy = max(-max_step, min(max_step, remaining_dy))
            # Update temp positions based on step size
            tempX = self.x + step_dx
            tempY = self.y + step_dy

            # Check if the bullet goes outside of the maze
            if tempX <= const.MAZE_X or tempY <= const.MAZE_Y or tempX >= const.MAZE_WIDTH + const.MAZE_X or tempY >= const.MAZE_HEIGHT + const.MAZE_Y:
                self.kill()
                return
            
            # Recalculate row and column based on the smaller steps
            row = math.ceil((self.getCenter()[1] - const.MAZE_Y) / const.TILE_SIZE)
            col = math.ceil((self.getCenter()[0] - const.MAZE_X) / const.TILE_SIZE)
            index = (row - 1) * const.COLUMN_AMOUNT + col

            # Check for collisions with tanks
            for i in range(g.difficultyType.playerCount):
                if not g.tankDead[i]:
                    tankCollision = self.getCollision(g.tankList[i].getCorners(), (tempX, tempY))
                    if self.name != g.tankList[i].getName() and tankCollision and g.tankList[i].getInvincibility() == 0:
                        g.damage(g.tankList[i], self.damage, self.gunOwner.getPlayer())
                        self.kill()
                        return
                    if self.bounce != self.originalBounce:
                        if tankCollision and g.tankList[i].getInvincibility() == 0:
                            g.damage(g.tankList[i], self.damage, self.gunOwner.getPlayer())
                            self.kill()
                            return

            # Handle wall collision
            tile = g.tileList[index-1]
            wallCollision = False
            if tile.border[0] and tempY - self.image.get_size()[1] <= tile.y: # Top border
                wallCollision = True
                self.angle = 180 - self.angle
            if tile.border[1] and tempX + self.image.get_size()[1] >= tile.x + const.TILE_SIZE: # Right border
                wallCollision = True
                self.angle = 360 - self.angle
            if tile.border[2] and tempY + self.image.get_size()[1] >= tile.y + const.TILE_SIZE: # Bottom border
                wallCollision = True
                self.angle = 180 - self.angle
            if tile.border[3] and tempX - self.image.get_size()[1] <= tile.x: # Left border
                wallCollision = True
                self.angle = 360 - self.angle
            if wallCollision:
                self.bounce -= 1
                self.speed *= -1
                if self.bounce == 0:
                    self.kill()
                return
            # After checking, update the current position
            self.x = tempX
            self.y = tempY

            # Subtract the amount we moved this step from the remaining distance
            remaining_dx -= step_dx
            remaining_dy -= step_dy

        # Once done with the loop, update the bullet's position and state
        self.updateCorners()
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        self.pleaseDraw = True

    def setBulletSpeed(self, speed):
        self.speed = speed

    def isDrawable(self):
        return self.drawable

    def getCenter(self):
        return (self.x, self.y)

    def updateCorners(self):
        # This function will update the corners of the tank based on the new position
        # Inputs: None
        # Outputs: None
        self.corners = [(self.rect.x, self.rect.y), (self.rect.x + self.rect.width, self.rect.y),
                        (self.rect.x + self.rect.width, self.rect.y + self.rect.height), (self.rect.x, self.rect.y + self.rect.height)]

    def setDamage(self, damage):
        self.damage = damage

    def customDraw(self, screen):
        # This function will draw the bullet on the screen and any additional features that may be needed
        # Inputs: screen: The screen that the bullet will be drawn on
        # Outputs: None
        if self.pleaseDraw and self.trail:
            offset = 5
            tX, tY = self.trailX, self.trailY
            if abs(self.trailX - self.x) < offset:
                tY += offset
            if abs(self.trailY - self.y) < offset:
                tX += offset
            pygame.draw.line(screen, c.geT("NEON_PURPLE"), (tX, tY), (self.x, self.y), 10)
            self.pleaseDraw = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def setName(self, name):
        self.name = name

    def setOriginalCollision(self, value):
        self.originalCollision = value

    def setBounce(self, bounceValue):
        self.bounce = bounceValue
        self.originalBounce = bounceValue
    
    def setDelta(self, delta):
        self.deltaTime = delta

    def getCollision(self, corners, point):
        # return point[0] >= corners[0][0] and point[0] <= corners[1][0] and point[1] >= corners[0][1] and point[1] <= corners[1][1]
        x,y = point
        inside = False
        for i in range(len(corners)):
            x1, y1 = corners[i]
            x2, y2 = corners[(i+1) % len(corners)]
            if ((y1 > y) != (y2 > y)) and (x < (x2 - x1) * (y - y1) / (y2 - y1) + x1):
                inside = not inside
        return inside

class SidewinderBullet(Bullet):

    def __init__(self, x, y, angle, gunLength, tipOffSet, gunOwner):
        super().__init__(x, y, angle, gunLength, tipOffSet, gunOwner)
        self.setBounce(5)

class JudgeBullet(Bullet):

    def __init__(self, x, y, angle, gunLength, tipOffSet, gunOwner):
        super().__init__(x, y, angle, gunLength, tipOffSet, gunOwner)
        self.setBounce(2)

class SilencerBullet(Bullet):

    def __init__(self, x, y, angle, gunLength, tipOffSet, gunOwner):
        super().__init__(x, y, angle, gunLength, tipOffSet, gunOwner)
        self.speed = 0.13
    
    def update(self):
        """
        Updates the bullet's position using ray tracing for precise collision detection.
        """
        # Convert angle to radians
        angleRad = math.radians(self.angle)

        # Calculate total movement in x and y
        dx = self.speed * math.cos(angleRad)
        dy = -self.speed * math.sin(angleRad)

        # Store initial position
        start_x, start_y = self.x, self.y

        # Track the path along the ray pixel by pixel
        steps = int(math.hypot(dx, dy))  # Number of pixels to check
        for i in range(steps + 1):  # Include the endpoint
            tempX = start_x + (dx * (i / steps))
            tempY = start_y + (dy * (i / steps))

            # Check if the bullet goes outside of the maze
            if tempX <= const.MAZE_X or tempY <= const.MAZE_Y or tempX >= const.MAZE_WIDTH + const.MAZE_X or tempY >= const.MAZE_HEIGHT + const.MAZE_Y:
                self.kill()
                return

            # Determine current tile based on precise position
            row = math.ceil((tempY - const.MAZE_Y) / const.TILE_SIZE)
            col = math.ceil((tempX - const.MAZE_X) / const.TILE_SIZE)
            index = (row - 1) * const.COLUMN_AMOUNT + col

            # Checking for self-damage
            if self.bounce != self.originalBounce:
                self.selfCollision = True

            # Check for collisions with tanks
            for i in range(g.difficultyType.playerCount):
                #<!HELP>
                # i'm not sure which collision to use so here is both
                if not g.tankDead[i]:
                    tankCollision = self.getCollision(g.tankList[i].getCorners(), (tempX, tempY))
                    # tankCollision = pygame.sprite.collide_rect(self, g.tankList[i])
                    if self.name != g.tankList[i].getName() and tankCollision and g.tankList[i].getInvincibility() == 0:
                        g.damage(g.tankList[i], self.damage, self.gunOwner.getPlayer())
                    if self.bounce != self.originalBounce:
                        if tankCollision and g.tankList[i].getInvincibility() == 0:
                            g.damage(g.tankList[i], self.damage, self.gunOwner.getPlayer())

            # Handle wall collision
            tile = g.tileList[index - 1]
            wallCollision = False

            # Check borders (ray-traced collision detection)
            if tile.border[0] and tempY - self.image.get_size()[1] <= tile.y:  # Top border
                wallCollision = True
                self.angle = 180 - self.angle
            if tile.border[1] and tempX + self.image.get_size()[1] >= tile.x + const.TILE_SIZE:  # Right border
                wallCollision = True
                self.angle = 360 - self.angle
            if tile.border[2] and tempY + self.image.get_size()[1] >= tile.y + const.TILE_SIZE:  # Bottom border
                wallCollision = True
                self.angle = 180 - self.angle
            if tile.border[3] and tempX - self.image.get_size()[1] <= tile.x:  # Left border
                wallCollision = True
                self.angle = 360 - self.angle

            if wallCollision:
                self.bounce -= 1
                if self.bounce == 0:
                    self.kill()
                    return
                # Stop at collision point
                break

        # Update bullet position to the last valid point before collision
        self.x, self.y = tempX, tempY

        # Update bullet state
        self.updateCorners()
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        self.pleaseDraw = True

class WatcherBullet(Bullet):

    trailColor = (255, 0, 0)

    def __init__(self, x, y, angle, gunLength, tipOffSet, gunOwner):
        super().__init__(x, y, angle, gunLength, tipOffSet, gunOwner)
        self.speed = 0.2

    def update(self):
        """
        Updates the bullet's position using ray-tracing for precise collision detection with walls and tanks.

        This method calculates the new position of the bullet, handles collisions with tanks and walls,
        and updates the bullet's state accordingly.
        """

        # Convert angle to radians for movement calculation
        angle_rad = math.radians(self.angle)

        # Calculate movement in x and y directions
        dx = self.speed * math.cos(angle_rad)
        dy = -self.speed * math.sin(angle_rad)

        # Determine the number of steps for fine-grained movement (ray tracing)
        steps = int(max(abs(dx), abs(dy)) * 10)  # Increase for more precision
        for step in range(steps + 1):
            temp_x = self.x + (dx * step / steps)
            temp_y = self.y + (dy * step / steps)

            # Check if the bullet goes outside the maze boundaries
            if temp_x <= const.MAZE_X or temp_y <= const.MAZE_Y or temp_x >= const.MAZE_WIDTH + const.MAZE_X or temp_y >= const.MAZE_HEIGHT + const.MAZE_Y:
                self.kill()
                return

            # Determine the current tile based on bullet position
            row = math.ceil((temp_y - const.MAZE_Y) / const.TILE_SIZE)
            col = math.ceil((temp_x - const.MAZE_X) / const.TILE_SIZE)
            index = (row - 1) * const.COLUMN_AMOUNT + col

            # Check for collisions with tanks
            for i in range(g.difficultyType.playerCount):
                #<!HELP>
                # i'm not sure which collision to use so here is both
                if not g.tankDead[i]:
                    tankCollision = self.getCollision(g.tankList[i].getCorners(), (temp_x, temp_y))
                    # tankCollision = pygame.sprite.collide_rect(self, g.tankList[i])
                    if self.name != g.tankList[i].getName() and tankCollision and g.tankList[i].getInvincibility() == 0:
                        g.damage(g.tankList[i], self.damage, self.gunOwner.getPlayer())
                        self.kill()
                        return
                    if self.bounce != self.originalBounce:
                        if tankCollision and g.tankList[i].getInvincibility() == 0:
                            g.damage(g.tankList[i], self.damage, self.gunOwner.getPlayer())
                            self.kill()
                            return

            # Handle wall collisions and bouncing
            tile = g.tileList[index - 1]
            bullet_size = self.image.get_size()[1]
            wall_collision = False

            # Check each wall (Top, Right, Bottom, Left)
            if tile.border[0] and temp_y - bullet_size <= tile.y:  # Top wall
                wall_collision = True
                self.angle = 180 - self.angle
            if tile.border[1] and temp_x + bullet_size >= tile.x + const.TILE_SIZE:  # Right wall
                wall_collision = True
                self.angle = 360 - self.angle
            if tile.border[2] and temp_y + bullet_size >= tile.y + const.TILE_SIZE:  # Bottom wall
                wall_collision = True
                self.angle = 180 - self.angle
            if tile.border[3] and temp_x - bullet_size <= tile.x:  # Left wall
                wall_collision = True
                self.angle = 360 - self.angle

            if wall_collision:
                self.bounce -= 1
                if self.bounce == 0:
                    self.kill()
                    return
            

        # After all steps, update the bullet's final position
        self.x = temp_x
        self.y = temp_y
        self.updateCorners()
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def customDraw(self, screen):
        # This function will draw the bullet on the screen and any additional features that may be needed
        # Inputs: screen: The screen that the bullet will be drawn on
        # Outputs: None
        if self.trail:
            pygame.draw.circle(screen, self.trailColor, (self.x, self.y), 1)
            self.pleaseDraw = False

    def setTrailColor(self, color):
        self.trailColor = color

    def draw(self,_):
        return # We don't want to draw the bullet

class ChamberBullet(Bullet):

    splash = True

    def __init__(self, x, y, angle, gunLength, tipOffSet, gunOwner):
        super().__init__(x, y, angle, gunLength, tipOffSet, gunOwner)
        self.speed = 0.5
        self.drawable = True

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
        # Calculate angle in radians
        angleRad = math.radians(self.angle)

        # Calculate the change in x and y
        dx = self.speed * math.cos(angleRad)
        dy = -self.speed * math.sin(angleRad)

        # Set the maximum step size
        max_step = 0.1

        # Track the progress along dx and dy
        remaining_dx = dx
        remaining_dy = dy
        # Continue while there's still distance to cover in either direction
        while abs(remaining_dx) > 0 or abs(remaining_dy) > 0:
            # Determine the step size, which should be limited to max_step
            step_dx = max(-max_step, min(max_step, remaining_dx))
            step_dy = max(-max_step, min(max_step, remaining_dy))
            # Update temp positions based on step size
            tempX = self.x + step_dx
            tempY = self.y + step_dy

            # Check if the bullet goes outside of the maze
            if tempX <= const.MAZE_X or tempY <= const.MAZE_Y or tempX >= const.MAZE_WIDTH + const.MAZE_X or tempY >= const.MAZE_HEIGHT + const.MAZE_Y:
                self.explode()
                return
            
            # Recalculate row and column based on the smaller steps
            row = math.ceil((self.getCenter()[1] - const.MAZE_Y) / const.TILE_SIZE)
            col = math.ceil((self.getCenter()[0] - const.MAZE_X) / const.TILE_SIZE)
            index = (row - 1) * const.COLUMN_AMOUNT + col

            # use the old collision
            # Check for collisions with tanks
            for i in range(g.difficultyType.playerCount):
                #<!HELP>
                # i'm not sure which collision to use so here is both
                if not g.tankDead[i]:
                    # tankCollision = self.getCollision(g.tankList[i].getCorners(), (tempX, tempY))
                    tankCollision = pygame.sprite.collide_rect(self, g.tankList[i])
                    if self.name != g.tankList[i].getName() and tankCollision and g.tankList[i].getInvincibility() == 0:
                        g.damage(g.tankList[i], self.damage, self.gunOwner.getPlayer())
                        self.kill()
                        return
                    if self.bounce != self.originalBounce:
                        if tankCollision and g.tankList[i].getInvincibility() == 0:
                            g.damage(g.tankList[i], self.damage, self.gunOwner.getPlayer())
                            self.kill()
                            return

            # Checking for self damage
            if self.bounce != self.originalBounce:
                self.selfCollision = True

            # Handle wall collision
            tile = g.tileList[index-1]
            wallCollision = False
            if tile.border[0] and tempY - self.image.get_size()[1] <= tile.y: # Top border
                wallCollision = True
                self.angle = 180 - self.angle
            if tile.border[1] and tempX + self.image.get_size()[1] >= tile.x + const.TILE_SIZE: # Right border
                wallCollision = True
                self.angle = 360 - self.angle
            if tile.border[2] and tempY + self.image.get_size()[1] >= tile.y + const.TILE_SIZE: # Bottom border
                wallCollision = True
                self.angle = 180 - self.angle
            if tile.border[3] and tempX - self.image.get_size()[1] <= tile.x: # Left border
                wallCollision = True
                self.angle = 360 - self.angle

            if wallCollision:
                for i in range(g.difficultyType.playerCount):
                    if not g.tankDead[i]:
                        tankCollision = self.getCollision(g.tankList[i].getCorners(), (tempX, tempY))
                        if self.name != g.tankList[i].getName() and tankCollision and g.tankList[i].getInvincibility() == 0:
                            g.damage(g.tankList[i], self.damage, self.gunOwner.getPlayer())
                            self.explode()
                            return
                        if self.bounce != self.originalBounce:
                            if tankCollision and g.tankList[i].getInvincibility() == 0:
                                g.damage(g.tankList[i], self.damage, self.gunOwner.getPlayer())
                                self.explode()
                                return
                self.bounce -= 1
                self.speed *= -1
                if self.bounce == 0:
                    self.explode()
                    return

            # After checking, update the current position
            self.x = tempX
            self.y = tempY

            # Subtract the amount we moved this step from the remaining distance
            remaining_dx -= step_dx
            remaining_dy -= step_dy

        # Once done with the loop, update the bullet's position and state
        self.updateCorners()
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        if abs(self.x- self.trailX) >= 1 and abs(tempY-self.trailY) >= 1:
            self.pleaseDraw = True

    def sizeImage(self, scale):
        # This function will resize the image
        # Inputs: Scale: The scale that the image will be resized to
        # Outputs: None
        originalCenter = self.rect.center
        originalCenter = copy.copy(originalCenter)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * scale, self.image.get_height()* scale))
        self.rect = self.image.get_rect()
        self.rect.center = originalCenter

    def setSplash(self, value):
        self.splash = value

    def explode(self):
        # This function will handle the explosion of the bullet and the respective splash damage
        # Inputs: None
        # Outputs: None
        if self.splash:
            #Middle radius
            splash1 = ChamberBullet(self.x, self.y, 0, 0, 0, self.gunOwner)
            splash1.sizeImage(10)
            splash1.updateCorners()
            splash1.setSplash(False)
            splash1.setDamage(self.damage)
            splash1.setName(self.name)
            splash1.setBulletSpeed(0.1)
            splash1.update()
            splash1.kill()
            # Outer radius
            splash2 = ChamberBullet(self.x, self.y, 0, 0, 0, self.gunOwner)
            splash2.sizeImage(20)
            splash2.updateCorners()
            splash2.setSplash(False)
            splash2.setDamage(self.damage)
            splash2.setName(self.name)
            splash2.setBulletSpeed(0.1)
            splash2.update()
            splash2.kill()
        self.kill()

    def draw(self,screen):
        # This function will only draw if the bullet is a splash and not a radius
        # Inputs: screen: The screen that the bullet will be drawn on
        # Outputs: None
        if self.splash:
            screen.blit(self.image, self.rect)
