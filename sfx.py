import pygame.mixer as mx
mx.init()

def eats():
    sound = mx.Sound('SFX/food.wav')
    mx.Sound.play(sound)
    return

def crash_sound(crash=False):
    if crash is True:
        sound = mx.Sound('SFX/crash.wav')
        mx.Sound.play(sound)
    else:
        None
    return

def game_music():
    sound = mx.Sound('SFX/game_music.wav')
    mx.Sound.play(sound)
    return