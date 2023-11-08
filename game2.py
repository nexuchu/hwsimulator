import pygame, sys
from pygame.locals import *
import socket
import os


if getattr(sys, 'frozen', False):
   program_directory = os.path.dirname(os.path.abspath(sys.executable))
   ENV = "PROD" # Run in .exe File. Assume it's a production environment.
else:
   program_directory = os.path.dirname(os.path.abspath(__file__))
   ENV = "DEV" # Run in .py File. Assume it's a development environment.
os.chdir(program_directory)

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("kitchen.wav")
pygame.mixer.music.play(10, 0.0)
pygame.mixer.music.set_volume(0.2)
screen = pygame.display.set_mode((425, 800))
clock = pygame.time.Clock()
running = True
screen_rect=screen.get_rect()
myFont = pygame.font.Font("ambitsek.ttf", 40)
bg = pygame.image.load("background.jpg")
bg = pygame.transform.scale(bg, (425, 800))
pygame.mouse.set_visible(False)
objects = []
readymade = 0

class Button:
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = myFont.render(buttonText, True, (10, 10, 10))

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }
        objects.append(self)
        self.last_press_time = 0
        self.visible = True
        self.clickable = True
    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.clickable:
            if self.buttonRect.collidepoint(mousePos):
                self.buttonSurface.fill(self.fillColors['hover'])
                if pygame.mouse.get_pressed(num_buttons=3)[0]:
                    current_time = pygame.time.get_ticks()
                    if current_time - self.last_press_time > 500:
                        self.last_press_time = current_time
                        self.buttonSurface.fill(self.fillColors['pressed'])
                        if self.onePress:
                            self.onclickFunction()
                        elif not self.alreadyPressed:
                            self.onclickFunction()
                            self.alreadyPressed = True
                    else:
                        self.alreadyPressed = False
            self.buttonSurface.blit(self.buttonSurf, [
                self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
                self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
            ])
            if self.visible:
                screen.blit(self.buttonSurface, self.buttonRect)
    def hide(self):
        self.visible = False
        self.clickable = False



class RightArrow(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('arrow.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (154/2.2, 221/2.2))     
        self.rect = self.image.get_rect()
        screen_center_x = screen.get_width() / 2
        screen_center_y = screen.get_height() / 2
        self.rect.center = (screen_center_x+175, screen_center_y-100)
    def click(self):
        global bg
        cursor_rect = cursor.rect
        if cursor_rect.colliderect(self.rect):
            egg.kill()
            pan.kill()
            egg.is_alive = False
            for obj in objects:
                if isinstance(obj, Button):
                    obj.hide()
            bg = pygame.image.load("bluebackground.jpg")

class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('cursor.png').convert_alpha()   
        self.rect = self.image.get_rect()
        screen_center_x = screen.get_width() / 2
        screen_center_y = screen.get_height() / 2
        self.rect.center = (screen_center_x, screen_center_y)
    def update(self):
        self.rect.center = pygame.mouse.get_pos()



class Pan(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('pan.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (376/1.5, 664/1.5))        
        self.rect = self.image.get_rect()
        screen_center_x = screen.get_width() / 2
        screen_center_y = screen.get_height() / 2
        self.rect.center = (screen_center_x, screen_center_y)

class Egg(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.is_alive = True
        self.egg_image = pygame.image.load('egg.png').convert_alpha()
        self.side2_image = pygame.image.load('side2.png').convert_alpha()
        self.image = self.egg_image
        self.image = pygame.transform.scale(self.image, (460 // 3.25, 382 // 3.25))
        self.rect = self.image.get_rect()
        screen_center_x = screen.get_width() / 2
        screen_center_y = screen.get_height() / 2
        self.rect.center = (screen_center_x, screen_center_y-100)
        self.current_image = 'egg.png'
        self.sound = pygame.mixer.Sound("flipping.mp3")
    def update(self):
        cursor_rect = cursor.rect
        pan_rect = pan.rect 
        if self.is_alive:
            if cursor_rect.colliderect(pan_rect):
                if self.current_image == 'egg.png':
                    self.image = self.side2_image
                    self.image = pygame.transform.scale(self.image, (460 // 3, 382 // 3))
                    self.current_image = 'side2.png'
                    self.sound.play()
                else:
                    self.image = self.egg_image
                    self.image = pygame.transform.scale(self.image, (460 // 3.25, 382 // 3))
                    self.current_image = 'egg.png'
                    self.sound.play()


def spawn():
    if egg.current_image == 'side2.png':
        egg.image = egg.egg_image
        egg.image = pygame.transform.scale(egg.image, (460 // 3, 382 // 3))
        egg.current_image = 'egg.png'
    egg_group.add(egg)
    egg_group.draw(screen)
def remove():
    global readymade
    if egg.current_image == 'side2.png':
        egg.kill()
        readymade += 1

Button(30, 650, 100, 100, 'egg', spawn, True)
Button(300, 650, 100, 100, 'done', remove, True)


cursor = Cursor()
cursor_group = pygame.sprite.Group()
cursor_group.add(cursor)

pan = Pan()
pan_group = pygame.sprite.Group()
pan_group.add(pan)

egg = Egg()
egg_group = pygame.sprite.Group()
egg_group.add(egg)

arrow = RightArrow()
arrow_group = pygame.sprite.Group()
arrow_group.add(arrow)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            s = socket.socket()
            host = "192.168.1.127"
            port = 55000
            s.connect((host, port))
            s.send(f"{os.getlogin()}={readymade}".encode())
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            egg.update()
            arrow.click()


    screen.blit(bg, (0, 0))
    for object in objects:
        object.process()
    pan_group.draw(screen)
    egg_group.draw(screen)
    arrow_group.draw(screen)
    cursor_group.draw(screen)
    cursor_group.update()

    housewife = myFont.render("Housewife", 1, "white")
    simulator = myFont.render("Simulator 23", 1, "white")
    readymadetext = myFont.render(f"{readymade}", 1, "white")
    screen.blit(housewife, (60, 60))
    screen.blit(simulator, (20, 100))
    if readymade < 10:
        screen.blit(readymadetext, (screen.get_width() / 2-15, 650))
    if readymade > 10 or readymade == 10: 
        screen.blit(readymadetext, (screen.get_width() / 2-30, 650))
    if readymade > 100 or readymade == 100:
        screen.blit(readymadetext, (screen.get_width() / 2-45, 650))
    pygame.display.flip()
    pygame.display.set_caption(f'Housewife Simulator 23 : Points: {readymade}')
    dt = clock.tick(60) / 1000
pygame.quit()