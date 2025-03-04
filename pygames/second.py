import pygame

pygame. init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1000

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Working With Shapes")

i:int = 100

run = True
while run:
    
    screen.fill((0, 0, 0))
    
    # makes the square
    pygame.draw.rect(screen, (255, 0, 0), (500, i, 150, 150), width = 5)
    
    i += 1
    if i >=850:
        i = 850

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
    pygame.display.flip()

pygame. quit()