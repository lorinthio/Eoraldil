import sys
sys.path.append('.//Pygame')
import pygame
import os


def play_music(musicname):
    pygame.mixer.pre_init(22050, -16, 2, 4096)
    pygame.init()
    
    pygame.mixer.music.load('forest_travel.ogg')
    pygame.mixer.music.play()
    
    pygame.mixer.music.set_volume(1.0)
    
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
play_music("forest")