import pygame, time

pygame. init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1000

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("scenes")

def game():
    ...

def pause():
    ...
def start_end(text):
    font = pygame.font.SysFont("arial", 25)
    y_pos = x_pos = 5
    for line in text.splitlines():
        for pos in range(1, len(line)+1):
            text = font.render(line[:pos], 1, (255, 255, 255))
            screen.blit(text, (x_pos, y_pos))
            pygame.display.update()
        y_pos += 100
        x_pos += 100



game:bool = False
pause:bool = False
run:bool = True
while run:
    keys = pygame.key.get_pressed()
    screen.fill((0, 0, 0))
    

    # scenes
    if game == True:
        game()

    elif pause == True:
        pause()
    else:
        start_end('press w to start')
        time.sleep(1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()