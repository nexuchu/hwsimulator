import pygame, sys
from pygame.locals import *
import socket
import os
import random
import sys

HOST = socket.gethostbyname("xcloud.ddns.net")
PORT = 55000

if getattr(sys, 'frozen', False):
   program_directory = os.path.dirname(os.path.abspath(sys.executable))
   ENV = "PROD" # Run in .exe File. Assume it's a production environment.
else:
   program_directory = os.path.dirname(os.path.abspath(__file__))
   ENV = "DEV" # Run in .py File. Assume it's a development environment.
os.chdir(program_directory)

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("loading.wav")
pygame.mixer.music.play(10, 0.0)
pygame.mixer.music.set_volume(0.2)
screen = pygame.display.set_mode((425, 800))
clock = pygame.time.Clock()
running = True
screen_rect=screen.get_rect()
myFont = pygame.font.Font("ambitsek.ttf", 40)
bg = pygame.image.load("background.jpg")
bg = pygame.transform.scale(bg, (425, 800))
bg2 = pygame.image.load("bluebackground.jpg").convert()
bg2 = pygame.transform.scale(bg2, (425, 800))
pygame.mouse.set_visible(False)
objects = []
readymade = 0
username = ''

def check_server_connection(): #avoids crash due to server not responding
    try:
        s = socket.socket()
        host = HOST
        port = PORT
        s.connect((host, port))
        s.send("REQ=CHECKCONN".encode())
        reply = s.recv(256).decode()
        if reply == "OK":
            print("Server Connection Successful!")
            s.close()
            return True
        else:
            print("Could not connect to Server.")
            return False
    except socket.error as e:
        print(f"A Socket Error occoured. Could not connect to Server. ({e})")
        return False
    except Exception as e:
        print(f"Exception Occoured. Could not connect to Server. ({e})")




def read_scores():
    if check_server_connection() == True:
        s = socket.socket()
        host = HOST
        port = PORT
        s.connect((host, port))
        s.send(f"REQ=GETSCORES".encode())
        scores = s.recv(4098).decode()
        scores = scores.split("#")
        del scores[-1]
        s.close()
        return scores

def post_scores(username, readymade):
    if check_server_connection() == True:
        s = socket.socket()
        host = HOST
        port = PORT
        s.connect((host, port))
        if username != "" and readymade < 1:
            s.send(f"REQ=POSTSCORES+{username}+{readymade}".encode())
        elif readymade > 1 and username == "":
            s.send(f"REQ=POSTSCORES+{os.getlogin()}+{readymade}".encode())
        s.close()

scorelol = read_scores()
if scorelol is not None:
    scorelol.sort(key=lambda x: x[-1], reverse=True)


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
        self.clickable = True
        self.visible = True
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

class Puddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('puddle.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(30, 350)
        self.rect.y = random.randint(250, 550)
        self.sound = pygame.mixer.Sound("water.mp3")

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
        self.available = True
    def update(self):
        cursor_rect = cursor.rect
        pan_rect = pan.rect 
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

class Arrow(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('arrow.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (154/4, 221/4))
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 20

def spawn():
    if egg.current_image == 'side2.png':
        egg.image = egg.egg_image
        egg.image = pygame.transform.scale(egg.image, (460 // 3, 382 // 3))
        egg.current_image = 'egg.png'
    egg_group.add(egg)
    egg_group.draw(screen)
    egg.available = True
def remove():
    global readymade
    if egg.current_image == 'side2.png':
        if egg.available:
            egg.kill()
            readymade += 1
            egg.available = False
def cooking():
    game_state.state = 'main_game'
    cookbutton.visible = False
    cookbutton.clickable = False
    cleanbutton.visible = False
    cleanbutton.clickable = False
    leaderboardbutton.visible = False
    leaderboardbutton.clickable = False
    pygame.mixer.music.load("kitchen.wav")
    pygame.mixer.music.play(10, 0.0)
    pygame.mixer.music.set_volume(0.2)

def cleaning():
    game_state.state = 'clean'
    cookbutton.visible = False
    cookbutton.clickable = False
    cleanbutton.visible = False
    cleanbutton.clickable = False
    leaderboardbutton.visible = False
    leaderboardbutton.clickable = False
    pygame.mixer.music.load("cleaning.wav")
    pygame.mixer.music.play(10, 0.0)
    pygame.mixer.music.set_volume(0.2)

def scores():
    game_state.state = 'scores'
    cookbutton.visible = False
    cookbutton.clickable = False
    cleanbutton.visible = False
    cleanbutton.clickable = False
    leaderboardbutton.visible = False
    leaderboardbutton.clickable = False

Button(30, 650, 100, 100, 'egg', spawn, True)
Button(300, 650, 100, 100, 'done', remove, True)
cookbutton = Button(63, 250, 300, 100, 'Cook', cooking, True)
cleanbutton = Button(63, 400, 300, 100, 'Clean', cleaning, True)
leaderboardbutton = Button(63, 550, 300, 100, 'Scores', scores, True)

class Maingame:
    def __init__(self):
        super().__init__()
        self.state = 'intro'

    def intro(self):
        global running
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                post_scores(username, readymade)
                running = False


        screen.blit(bg, (0, 0))

        cookbutton.process()
        cleanbutton.process()
        leaderboardbutton.process()

        cursor_group.draw(screen)
        cursor.image = pygame.image.load('cursor.png').convert_alpha()   
        cursor.rect = cursor.image.get_rect()
        cursor_group.update()

        housewife = myFont.render("Housewife", 1, "white")
        simulator = myFont.render("Simulator 23", 1, "white")
        screen.blit(housewife, (60, 60))
        screen.blit(simulator, (20, 100))
        pygame.display.flip()

    def main_game(self):
        self.state = 'main_game'
        global running
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                s = socket.socket()
                host = "192.168.1.127"
                port = 55000
                s.connect((host, port))
                s.send(f"{username}={readymade}".encode())
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                egg.update()
                arrow_rect = arrow.rect
                cursor_rect = cursor.rect
                if cursor_rect.colliderect(arrow_rect):
                    game_state.state = 'intro'
                    cookbutton.visible = True
                    cookbutton.clickable = True
                    cleanbutton.visible = True
                    cleanbutton.clickable = True
                    leaderboardbutton.visible = True
                    leaderboardbutton.clickable = True
                    pygame.mixer.music.load("loading.wav")
                    pygame.mixer.music.play(10, 0.0)
                    pygame.mixer.music.set_volume(0.2)


        screen.blit(bg, (0, 0))
        for object in objects:
            object.process()
        pan_group.draw(screen)
        egg_group.draw(screen)
        arrow_group.draw(screen)
        cursor_group.draw(screen)
        cursor.image = pygame.image.load('cursor.png').convert_alpha()   
        cursor.rect = cursor.image.get_rect()
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
    
    def clean(self):
        self.state = 'clean'
        global running
        global puddle
        global readymade
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                post_scores(username, readymade)
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                cursor_rect = cursor.rect
                puddle_rect = puddle.rect 
                arrow_rect = arrow.rect
                if cursor_rect.colliderect(puddle_rect):
                    puddle.kill()
                    new_puddle = Puddle()
                    puddle_group.add(new_puddle)
                    puddle = new_puddle
                    readymade += 1
                    puddle.sound.play()
                if cursor_rect.colliderect(arrow_rect):
                    game_state.state = 'intro'
                    cookbutton.visible = True
                    cookbutton.clickable = True
                    cleanbutton.visible = True
                    cleanbutton.clickable = True
                    leaderboardbutton.visible = True
                    leaderboardbutton.clickable = True
                    pygame.mixer.music.load("loading.wav")
                    pygame.mixer.music.play(10, 0.0)
                    pygame.mixer.music.set_volume(0.2)


        screen.blit(bg2, (0, 0))
        arrow_group.draw(screen)
        puddle_group.draw(screen)
        cursor_group.draw(screen)
        cursor.image = pygame.image.load('mop.png').convert_alpha()
        cursor.image = pygame.transform.scale(cursor.image, (120, 120))
        cursor.rect = cursor.image.get_rect()
        cursor_group.update()

        housewife = myFont.render("Housewife", 1, "white")
        simulator = myFont.render("Simulator 23", 1, "white")
        screen.blit(housewife, (60, 60))
        screen.blit(simulator, (20, 100))
        readymadetext = myFont.render(f"{readymade}", 1, "white")
        if readymade < 10:
            screen.blit(readymadetext, (screen.get_width() / 2-15, 650))
        if readymade > 10 or readymade == 10: 
            screen.blit(readymadetext, (screen.get_width() / 2-30, 650))
        if readymade > 100 or readymade == 100:
            screen.blit(readymadetext, (screen.get_width() / 2-45, 650))
        pygame.display.flip()


    def scores(self):
        self.state = 'scores'
        global username
        global running
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                post_scores(username, readymade)
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                arrow_rect = arrow.rect
                cursor_rect = cursor.rect
                if cursor_rect.colliderect(arrow_rect):
                    game_state.state = 'intro'
                    cookbutton.visible = True
                    cookbutton.clickable = True
                    cleanbutton.visible = True
                    cleanbutton.clickable = True
                    leaderboardbutton.visible = True
                    leaderboardbutton.clickable = True
                    pygame.mixer.music.load("loading.wav")
                    pygame.mixer.music.play(10, 0.0)
                    pygame.mixer.music.set_volume(0.2)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    if len(username) < 5:
                        username += event.unicode


        screen.blit(bg, (0, 0))
        arrow_group.draw(screen)
        cursor_group.draw(screen)
        cursor.image = pygame.image.load('cursor.png').convert_alpha()
        cursor.rect = cursor.image.get_rect()
        cursor_group.update()

        scoretextfont = pygame.font.Font("ambitsek.ttf", 30)
        tutotextfont = pygame.font.Font("ambitsek.ttf", 17)
        housewife = myFont.render("Housewife", 1, "white")
        simulator = myFont.render("Simulator 23", 1, "white")
        readymadetext = myFont.render(f"{readymade}", 1, "white")
        usernametext = myFont.render(username,True,(255,255,255))
        tutotext = tutotextfont.render("Start typing your username", 1, "white")
        tutotext2 = tutotextfont.render("it will be saved automatically!", 1, "white")
        screen.blit(housewife, (60, 60))
        screen.blit(simulator, (20, 100))
        screen.blit(usernametext, (125, 175))
        screen.blit(tutotext, (27, 250))
        screen.blit(tutotext2, (14, 270))
        y_position = 350

        if scorelol != None: # scorelol will be none by default. If this is not changed via a successful connection, it will say that no connection could be established.
            for i, element in enumerate(scorelol[:5]):
                # Just take the List elements as a whole and split them up. ~iLollek
                element = element.split(":")
                name = element[0]
                scorex = element[1]
                if name != "":
                    score_text = scoretextfont.render(f"{i + 1}. {name}: {scorex}", 1, "white")
                    screen.blit(score_text, (10, y_position))
                    y_position += 30
        else:
            score_text = scoretextfont.render(f"No Connection", 1, "white")
            screen.blit(score_text, (44, y_position))

        if readymade < 10:
            screen.blit(readymadetext, (screen.get_width() / 2-15, 650))
        if readymade > 10 or readymade == 10: 
            screen.blit(readymadetext, (screen.get_width() / 2-30, 650))
        if readymade > 100 or readymade == 100:
            screen.blit(readymadetext, (screen.get_width() / 2-45, 650))
        pygame.display.flip()

    def statemanager(self):
        if self.state == 'intro':
            self.intro()
        if self.state == 'main_game':
            self.main_game()
        if self.state == 'clean':
            self.clean()
        if self.state == 'scores':
            self.scores()

arrow = Arrow()
arrow_group = pygame.sprite.Group()
arrow_group.add(arrow)

cursor = Cursor()
cursor_group = pygame.sprite.Group()
cursor_group.add(cursor)

pan = Pan()
pan_group = pygame.sprite.Group()
pan_group.add(pan)

egg = Egg()
egg_group = pygame.sprite.Group()
egg_group.add(egg)

puddle = Puddle()
puddle_group = pygame.sprite.Group()
puddle_group.add(puddle)

game_state = Maingame()

while running:
    game_state.statemanager()
    dt = clock.tick(60) / 1000
pygame.quit()