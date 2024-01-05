# Library imports
import pygame as pg
import random as rnd
import math

# Initiantion of pygame library
pg.init()

# Preparation of the 'window' display surface
windowWidth = 700
windowHeight = 700
window = pg.display.set_mode([windowWidth, windowHeight])

# Setting the scores for player one and player 2
p1Score = 0
p2Score = 0

# Sets the caption of the pygame window
pg.display.set_caption("AFUERA")

# Prepares the fps of the game
clock = pg.time.Clock()
fps = 60

# Loads images and fonts
Milei1 = pg.image.load("javier-milei.jpg")
Milei2 = pg.image.load("AFUERA.png")
font = pg.font.Font("COMIC.ttf", 32)
font2 = pg.font.Font("COMICBD.ttf", 100)

# The 'Sprite' mother class with some core values all sprites have
class Sprite(pg.sprite.Sprite):
    def __init__(self, width, height, xPos, yPos, speed):
        self.x = xPos
        self.y = yPos
        self.width = width
        self.height = height
        self.speed = speed
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)
        
# The 'playerSprite' is a sprite class underneath the 'Sprite' mother class, meant for the pong paddle(s)
class playerSprite(Sprite):
    # On initiation, the class sets some extra values not inherent to the 'Sprite' mother class
    def __init__(self, width, height, xPos, yPos, sprite1, sprite2, speed, keyUp, keyDown):
        super().__init__(width, height, xPos, yPos, speed)
        self.image1 = pg.transform.scale(sprite1, (width, height))
        self.image2 = pg.transform.flip(pg.transform.scale(sprite2, (width, height)), True, False)
        self.keyUp = keyUp
        self.keyDown = keyDown
    
    # A function for things that needs updating every frame
    def update(self):
        pressedButtons = pg.key.get_pressed()
        if pressedButtons[self.keyUp]:
            if self.y-self.speed/fps >= 0:
                self.y -= self.speed/fps
            else:
                self.y = 0
        if pressedButtons[self.keyDown]:
            if self.y + self.speed/fps <= windowHeight-self.height:
                self.y += self.speed/fps
            else:
                self.y = windowHeight-self.height
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)

# The 'ballSprite' class is a class beneath the 'Sprite' mother class, meant for the pong ball
class ballSprite(Sprite):
    # Upon initiation, some extra values not inherent to the 'Sprite' mother class needed to be set
    def __init__(self, width, height, xPos, yPos, speed):
        super().__init__(width, height, xPos, yPos, speed)
        self.xSpeed = -rnd.uniform(self.speed/4, self.speed)
        if rnd.randint(0, 1) == 1:
            self.ySpeed = math.sqrt(speed**2-self.xSpeed**2)
        else:
            self.ySpeed = -math.sqrt(speed**2-self.xSpeed**2)
    
    # A function for things that needs updating every frame
    def update(self):
        global p1Score, p2Score, i
        self.x += self.xSpeed
        self.y += self.ySpeed
        if self.y < 0 or self.y > (windowHeight-self.height):
            self.ySpeed *= -1
        if self.x < 0:
            p2Score += 1
            Ball.__init__(20, 20, windowWidth//2, windowHeight//2, 10)
        elif self.x > (windowWidth-self.width):
            p1Score += 1
            Ball.__init__(20, 20, windowWidth//2, windowHeight//2, 10)
        if (Player1.rect.collidepoint((self.x+self.width//2, self.y)) and self.ySpeed < 0) or (Player1.rect.collidepoint((self.x+self.width//2, self.y+self.height)) and self.ySpeed > 0):
            self.ySpeed *= -1
            i = 0
        if Player1.rect.collidepoint((self.x, self.y+self.height//2)):
            self.xSpeed *= -1
            i = 0

# Creates the 'Player1' paddle object of the 'playerSprite' class, and the 'Ball' ball object of the 'ballSprite' class
Player1 = playerSprite(75, 300, 0, 0, Milei1, Milei2, 200, pg.K_w, pg.K_s)
Ball = ballSprite(20, 20, windowWidth//2, windowHeight//2, 10)

# Creates easily accessible colour variable with the colour's rgb value
white = (255, 255, 255)
black = (0, 0, 0)

# Creates the text that goes "AFUERA!!!!" whenever Lord Milei throws away another necessary part of the Argentinian state organ, and all the variables needed for the displaying of that text
AFUERATEXT = font2.render("AFUERA!!!!", True, white)
AFUERATEXTRect = AFUERATEXT.get_rect()
AFUERATEXTRect.center = (windowWidth//2, windowHeight//2)

# Prepares the 'iLimit' variable for easily deciding how many frames the "AFUERA mode" is active (the "AFUERA mode" is the mode in which our Lord Milei goes "AFUERA!!!!" and changes his sprite's image). 'i' is the frame counter. 'run' is the bool variable determining if the program loop should be running or not.
iLimit = 30
i = iLimit
run = True
while run:
    # Checks if the program is exited or not
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    
    # Runs the update functions for the 2 objects 'Player1' (the paddle) and 'Ball' (the ball)
    Player1.update()
    Ball.update()

    # Fills the 'window' display surface (the screen) black
    window.fill(black)

    # Creates the text for displaying the players' scores (i'm noting that Player 2 doesn't have a paddle, which i consider to be a skill issue on their part) and the variables necessary for displaying this text
    pointText = font.render(f"{p1Score}:{p2Score}", True, white)
    pointTextRect = pointText.get_rect()
    pointTextRect.center = (windowWidth//2, 32)

    # Draws the text for the players' score
    window.blit(pointText, pointTextRect)

    # This is the conditional the frame counter is used for. If the frame counter is under the limit, then "AFUERA mode" (this term has been explained in an earlier comment) is activated, while if the frame counter is equal to or above the limit, then "AFUERA mode" is deactivated. The frame counter is reset when the ball and paddle collide, meaning that its effective function is to enter "AFUERA mode" for a certain amount of frames after collision
    i += 1
    if i < iLimit:
        window.blit(Player1.image2, Player1.rect)
        window.blit(AFUERATEXT, AFUERATEXTRect)
    else:
        window.blit(Player1.image1, Player1.rect)

    # Draws a circle with the values extracted from the Ball object
    pg.draw.circle(window, white, ((Ball.x+Ball.width//2), (Ball.y+Ball.height//2)), Ball.width//2)

    # Updates the display, and controls the FPS
    pg.display.flip()
    clock.tick(fps)

