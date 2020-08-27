import random

import pygame

from pygame.locals import *
from player import Player
from virus import Virus
from soap import Soap


def setup(W, H, caption):
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    win = pygame.display.set_mode((W, H))
    pygame.display.set_caption(caption)

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("comicsans", 30, True)
    return win, clock, font


win, clock, font = setup(1000, 800, "Stay Healthy")


def update(*args, **kwargs):
    for arg in args:
        arg.update()
    for kw, arg in kwargs.items():
        if kw == "viruses":
            for virus in arg:
                result = virus.update()
                if not result:
                    kwargs["player"].health -= 1
                    if kwargs["player"].health <= 0:
                        kwargs["player"].dead()
        elif kw == "soaps":
            for soap in arg:
                soap.update()
        else:
            arg.update()


def endgame(player):
    player.is_alive = True
    player.health = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_c:
                    main()
        redraw(win, player=player, text=["Press q to quit and c to play again!", 200, 200])
        clock.tick(30)


def redraw_healthbar(win, player):
    drawing_x = player.x
    drawing_y = player.y + player.width + 5
    drawing_width = player.width
    drawing_height = 16
    drawing_sep = 2
    pygame.draw.rect(win, (255, 0, 0), pygame.Rect(drawing_x, drawing_y, drawing_width, drawing_height))
    pygame.draw.rect(win, (0, 255, 0), pygame.Rect(drawing_x + drawing_sep, drawing_y + drawing_sep,
                                                   (drawing_width - 2 * drawing_sep) * (player.health / 10),
                                                   drawing_height - 2 * drawing_sep))


def redraw(win, *args, **kwargs):
    win.fill((5, 5, 50))
    for arg in args:
        arg.draw(win)
    for kw, arg in kwargs.items():
        if kw == "player":
            alive = arg.draw(win)
            if not alive:
                endgame(kwargs["player"])
        if kw == "text":
            text = font.render(arg[0], 1, (220, 220, 220))
            win.blit(text, (arg[1], arg[2]))
        else:
            arg.draw(win)
    redraw_healthbar(win, kwargs["player"])
    pygame.display.flip()


def main():
    pygame.time.set_timer(USEREVENT + 1, 3000)  # Timer for Virus spawn
    pygame.time.set_timer(USEREVENT + 2, 10000)  # Timer for Soap spawn
    player = Player(468, 675, pygame.image.load("spaceship.png"), pygame.image.load("spaceship2.png"), 64, 64)
    viruses = []
    soaps = []
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                player.handle_key_pressed(event.key)
            if event.type == pygame.KEYUP:
                player.handle_key_unpressed(event.key)
            if event.type == USEREVENT + 1:
                viruses.append(Virus(random.randint(10, 958), 10, pygame.image.load("virus.png"), 64, 64))
            if event.type == USEREVENT + 2:
                soaps.append(Soap(random.randint(10, 958), 10, pygame.image.load("soap.png"), 64, 64))
        update(player=player, viruses=viruses, soaps=soaps)
        redraw(win, *viruses, *soaps, player=player)
        clock.tick(30)


if __name__ == '__main__':
    main()
