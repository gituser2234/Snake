# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 22:18:51 2016

@author: anonymous
"""

import pygame
import time
import random

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)

display_width = 800
display_height = 600

#it's our surface
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Slither")

icon = pygame.image.load("apple.png")
pygame.display.set_icon(icon)

img = pygame.image.load("snakehead.png")
appleimg = pygame.image.load("apple.png")
#update entire if no args
#pygame.display.update()

clock = pygame.time.Clock()

AppleThickness = 30
block_size = 20
FPS = 20

direction = "right"

smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("cosicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)

def game_intro():
    intro = True
    
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        
        gameDisplay.fill(white)
        message_to_screen("Welcome to Slither!", green, -100, "large")
        message_to_screen("The objetive is to eat red apples.",
                          black, -30)
        pygame.display.update()
        clock.tick(15)

def snake(block_size, snakelist):
    if direction == "right":
        head = pygame.transform.rotate(img, 270)
    elif direction == "left":
        head = pygame.transform.rotate(img, 90)
    elif direction == "down":
        head = pygame.transform.rotate(img, 180)
    elif direction == "up":
        head = img
    gameDisplay.blit(head, (snakelist[-1][0], snakelist[-1][1]))
    
    #all up to negative first
    for XnY in snakelist[:-1]:
        pygame.draw.rect(gameDisplay, green, (XnY[0], XnY[1], block_size, block_size))

def text_objects(text, color, size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    if size == "medium":
        textSurface = medfont.render(text, True, color)
    if size == "large":
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_to_screen(msg, color, y_displace=0, size="small"):
    textSurf, textRect = text_objects(msg, color, size)
#    screen_text = font.render(msg, True, color)
#    gameDisplay.blit(screen_text, [display_width // 2, display_height // 2])
    textRect.center = (display_width // 2), (display_height // 2)+y_displace
    gameDisplay.blit(textSurf, textRect)    

def gameLoop():
    global direction
    direction = "right"
    
    gameExit = False
    gameOver = False

    #lead means leader
    lead_x = display_width // 2
    lead_y = display_height // 2
    
    lead_x_change = 10
    lead_y_change = 0
    
    snakeList = []
    snakeLength = 1
    
    randAppleX = round(random.randrange(0, display_width-AppleThickness))#/10.0)*10.0
    randAppleY = round(random.randrange(0, display_height-AppleThickness))#/10.0)*10.0
    
    while not gameExit:
        
        while gameOver == True:
            gameDisplay.fill(white)
            message_to_screen("Game Over", red, -50, size="large")
            message_to_screen("Press C to play again or Q to quit", 
                              black, 50, size="medium")
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = "left"
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    lead_x_change = block_size
                    direction = "right"
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    direction = "up"
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    direction = "down"
                    lead_y_change = block_size
                    lead_x_change = 0
        
        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
            gameOver = True
                    
        lead_x += lead_x_change
        lead_y += lead_y_change
        
        gameDisplay.fill(white)
        
        #myApple = pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, AppleThickness, AppleThickness])
        myApple = pygame.Rect(randAppleX, randAppleY, AppleThickness, AppleThickness)
        gameDisplay.blit(appleimg, (randAppleX, randAppleY))
        #gameDisplay.fill(red, rect=[200, 200, 50, 50])
        
        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)   
        
        if len(snakeList) > snakeLength:
            del snakeList[0]
        
        #everything to last element
        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True
            
        snake(block_size, snakeList)
        
        #after all draw actions for this frame:
        pygame.display.update() # < why display not gameDisplay ??
 
        if myApple.colliderect(pygame.Rect((lead_x, lead_y, block_size, block_size))):
                randAppleX = round(random.randrange(0, display_width-block_size))#/10.0)*10.0
                randAppleY = round(random.randrange(0, display_height-block_size))#/10.0)*10.0
                snakeLength += 1 
            
        clock.tick(FPS)
    
    #update entire all ot once
    #pygame.display.flip()
    
    pygame.quit()
    quit()
    
game_intro()
gameLoop()