import pygame
#pip install pygame --user

def sound_print(soundfile):
    pygame.mixer.init()
    bb = pygame.mixer.Sound(soundfile)
    bb.play()

#sound_print()
