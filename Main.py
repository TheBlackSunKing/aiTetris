import sys
from Tetris import tetris
from copy import deepcopy
from Tplayer import tplayer
from random import choice, randrange, randint, Random

import pygame
from pygame.locals import *

pygame.init()    



class Music:
    def __init__(self, path):
        self.path = path
        pygame.mixer.music.load(path) 
        pygame.mixer.music.set_volume(0.8) 
        # Loading the song 
    def play(self):
        pygame.mixer.music.play(loops=-1)
    def stop(self):
        pygame.mixer.music.stop()
class Sound:
    def __init__(self, path):
        self.path = path
        self.sound = pygame.mixer.Sound(path)
        self.sound.set_volume(0.2)
    def play(self):
        pygame.mixer.Sound.stop(self.sound)
        pygame.mixer.Sound.play(self.sound)
    def stop(self):
        pygame.mixer.Sound.stop(self.sound)
class Soundboard:
    def __init__(self):
        self.placeSound= Sound("placed.wav")
        self.LineErased= Sound("lineerased.wav")
        self.loseSound= Sound ("Loss.wav")
    def checkSoundToPLay(self, tetrisinstance):
        if tetrisinstance.lineErased:
            self.LineErased.play()
            tetrisinstance.lineErased=False
        if tetrisinstance.placeSound:
            self.placeSound.play()
            tetrisinstance.placeSound=False
        if tetrisinstance.loseSound:
            self.loseSound.play()
            tetrisinstance.loseSound=False
def run():
        

    music = Music("TetrisProjectMusic.mp3")
    soundboard = Soundboard()
    music.play()

    fpsClock = pygame.time.Clock()
    font = pygame.font.SysFont('Comic Sans MS', 30)
    font_small = pygame.font.SysFont('Comic Sans MS', 22)
    title_score = font.render('Puntuacion', True, pygame.Color('green'))




    W, H = 10, 20
    TILE = 45
    GAME_RES = W * TILE, H * TILE
    RES = 750, 940
    FPS = 60
    grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]
    grid2 = [pygame.Rect(x * TILE + 20*TILE , y * TILE, TILE, TILE) for x in range(W) for y in range(H)]
    screen = pygame.display.set_mode((W*TILE*3, H*TILE))
    figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)
    tetrisnormal = tetris()
    tetrisnormalIA = tetris()


    # Game loop.
    count = 0
    seed = randint(0,2700000)

    tetrisnormal.initialize(seed)
    tetrisnormalIA.initialize(seed)

    Iasiniestra = tplayer(tetrisnormalIA)


    while True:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and count < 15:
                    tetrisnormal.dx = -1
                    #tetrisnormalIA.dx = -1
                elif event.key == pygame.K_RIGHT and count < 15:
                    tetrisnormal.dx = 1
                    #tetrisnormalIA.dx = 1
                elif event.key == pygame.K_UP:
                    tetrisnormal.rotate = True
                elif event.key == pygame.K_ESCAPE:
                    seed = randint(0,2700000)
                    tetrisnormal.initialize(seed)
                    tetrisnormalIA.initialize(seed)
                elif event.key == pygame.K_SPACE:
                    tetrisnormal.snap_down()
                elif event.key == pygame.K_c:
                    music.play()
                elif event.key == pygame.K_s:
                    music.stop()
        
            keys=pygame.key.get_pressed()
        
        if keys[K_DOWN]:
            tetrisnormal.anim_limit = 100
            tetrisnormalIA.anim_limit = 100
        if keys[K_RIGHT]:
            count+=2
            if count >= 15:
                tetrisnormal.dx = 1
                #tetrisnormalIA.dx = 1
                count = 10
            
        if keys[K_LEFT]:
            count+=2
            if count >= 15:
                tetrisnormal.dx = -1
                #tetrisnormalIA.dx = -1
                count = 10
            
        if count >0:
            count -=1
        
        # move x

        # Update.
        tetrisnormal.tick()
        Iasiniestra.movement(tetrisnormalIA)
        #tetrisnormalIA.tick()




        # Draw.
        [pygame.draw.rect(screen, (40, 40, 40), i_rect, 1) for i_rect in grid]
        [pygame.draw.rect(screen, (40, 40, 40), i_rect, 1) for i_rect in grid2]

        #PLAYER TETRIS
        for i  in range (4):
            figure_rect.x= tetrisnormal.figure[i].x * TILE
            figure_rect.y= tetrisnormal.figure[i].y * TILE
            pygame.draw.rect(screen, Color('white'), figure_rect)

        for y, raw in enumerate(tetrisnormal.field):
            for x, col in enumerate(raw):
                if col:
                    figure_rect.x, figure_rect.y = x * TILE, y * TILE
                    pygame.draw.rect(screen, col, figure_rect)
        for i in range(4):
            figure_rect.x = tetrisnormal.next_figure[i].x * TILE+7*TILE +25
            figure_rect.y = tetrisnormal.next_figure[i].y * TILE+2*TILE
            if tetrisnormal.gameover:
                pygame.draw.rect(screen, Color('red'), figure_rect)
            else:
                pygame.draw.rect(screen, Color('white'), figure_rect)


        #IA TETRIS
        for i  in range (4):
            figure_rect.x= tetrisnormalIA.figure[i].x * TILE + 20*TILE
            figure_rect.y= tetrisnormalIA.figure[i].y * TILE
            pygame.draw.rect(screen, Color('white'), figure_rect)
            
        for y, raw in enumerate(tetrisnormalIA.field):
            for x, col in enumerate(raw):
                if col:
                    figure_rect.x, figure_rect.y = x * TILE + 20*TILE, y * TILE
                    pygame.draw.rect(screen, col, figure_rect)
        for i in range(4):
            figure_rect.x = tetrisnormalIA.next_figure[i].x * TILE+13*TILE -25
            figure_rect.y = tetrisnormalIA.next_figure[i].y * TILE+2*TILE
            if tetrisnormalIA.gameover:
                pygame.draw.rect(screen, Color('red'), figure_rect)
            else:
                pygame.draw.rect(screen, Color('white'), figure_rect)

        soundboard.checkSoundToPLay(tetrisnormal)
        soundboard.checkSoundToPLay(tetrisnormalIA)
        #DRAW SCORE
        screen.blit(title_score, (600, 780))
        screen.blit(font.render(str(tetrisnormal.score), True, pygame.Color('white')), (550, 840))
        screen.blit(font.render(str(tetrisnormalIA.score), True, pygame.Color('white')), (750, 840))
        
        
        if not tetrisnormalIA.gameover and not tetrisnormal.gameover:
            screen.blit(font.render(str("Peleas contra la Ia Siniestra" ), True, pygame.Color('gray')), (475, 400))
            screen.blit(font.render(str("Controlas la izquierda" ), True, pygame.Color('gray')), (475, 450))
            screen.blit(font_small.render(str("-Usa las flechas para mover" ), True, pygame.Color('gray')), (475, 500))
            screen.blit(font_small.render(str("-Arriba rota la pieza" ), True, pygame.Color('gray')), (475, 540))
            screen.blit(font_small.render(str("-Espacio la deja caer inmmediatamente" ), True, pygame.Color('gray')), (475, 580))
            screen.blit(font_small.render(str("-ESC reinicia el juego" ), True, pygame.Color('gray')), (475, 620))
            screen.blit(font_small.render(str("Demuestra que la humanidad manda" ), True, pygame.Color('red')), (500, 660))
            #screen.blit(font.render(str("Current Number of rows"+ str(tetrisnormalIA.calculateNumberOfRows())), True, pygame.Color('gray')), (500, 600))
            #screen.blit(font.render(str("Expected Number of rows"+ str(Iasiniestra.maxRow)), True, pygame.Color('gray')), (500, 600+35*1))
            #screen.blit(font.render(str("Expected Y factor"+ str(Iasiniestra.yfactor)), True, pygame.Color('gray')), (500, 600+35*2))
            #screen.blit(font.render(str(Iasiniestra.maxScoreChoice), True, pygame.Color('gray')), (500, 600+35*3))
            #screen.blit(font.render(str("Expected erased lines: " + str(Iasiniestra.tetriserasedlines)), True, pygame.Color('gray')), (500, 600+35*4))
            #screen.blit(font.render(str("Trash quantity: "+ str(tetrisnormalIA.trash())), True, pygame.Color('gray')), (500, 600+35*5))
        elif tetrisnormal.score > tetrisnormalIA.score and tetrisnormalIA.gameover:
            screen.blit(font.render(str("LA IA SINIESTRA PERDIO"), True, pygame.Color('green')), (470, 500 ))
        elif tetrisnormal.gameover and tetrisnormal.score < tetrisnormalIA.score:
            screen.blit(font.render(str("LA IA SINIESTRA GANO"), True, pygame.Color('red')), (470, 500 ))


        pygame.display.flip()
        fpsClock.tick(FPS)


if __name__ == '__main__':
    run()