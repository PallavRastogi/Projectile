import pygame
from pygame import mixer
from pygame import freetype
import math

pygame.init()
mixer.init()
clock = pygame.time.Clock()
gamefont = freetype.SysFont("comicsansms", 20)
window_x, window_y = 960,540
white = [255,255,255]
black = [0, 0, 0]
run = True
screen = pygame.display.set_mode((window_x, window_y))
pygame.display.set_caption('Pallav Game')
clock = pygame.time.Clock()

u = 95
FPS = 180
projectile_list = []

colour_counter = 0
colour_list = ((255,255,255), (255,255,0), (255,0,255), (0,255,255), (255,0,0), (0,255,0), (0,0,255))
projectile_colour = []

def projectile(speed, angle, g):

    sin = math.sin(angle)
    cos = math.cos(angle)
    tan = math.tan(angle)
    TIME = 2*u*sin/g
    RANGE = 2*u*u*sin*cos/g
    last_x = TIME*FPS
    increment = RANGE/(last_x)
    counter = 0
    
    while True:
        if counter > RANGE:
            break
        yield (counter , (window_y - (counter*tan - g*counter*counter/(2*u*u*cos*cos))))
        counter+=increment
        
    yield None, None

while run:
    x, y = pygame.mouse.get_pos()
    y = window_y - y
    angle = math.pi/2
    try:
        angle = math.atan(y/x)
    except ZeroDivisionError:
        pass
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                            
                projectile_list.append(projectile(u, angle, 9.8))
                projectile_colour.append(colour_list[colour_counter%7])
                colour_counter += 1
            
            elif event.button == 3:
                screen.fill(black)
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                projectile_list.clear()
                projectile_colour.clear()
                screen.fill(black)
    
    
    for index, item in enumerate(projectile_list):
        x, y = next(item)
        if x == None:
            projectile_list.remove(item)
            projectile_colour.pop(index)
        
        else:
            pygame.draw.rect(screen, projectile_colour[index], [x, y, 1, 1])
    

    text_surface, rect = gamefont.render(str(angle*180/math.pi)[0:4]+"°", (255,255,255))
    screen.fill((0,0,0), [900, 0, 60, 40])
    screen.blit(text_surface, (900, 10))


    pygame.display.flip()
    clock.tick(FPS)
