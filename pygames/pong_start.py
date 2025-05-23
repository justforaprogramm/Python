import pygame

pygame. init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1000

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

y1:int = 425
y2:int = 425
y3:int = 500
x3:int = 960

def Player1(player:int, keys) -> int:
    player += (keys[pygame.K_s] - keys[pygame.K_w])

    if player > 850:
        player = 850
    if player < 0:
        player = 0 
    return player

def Player2(player:int, keys) -> int:
    player += (keys[pygame.K_DOWN] - keys[pygame.K_UP])

    if player > 850:
        player = 850
    if player < 0:
        player = 0
    return player 

def Ball(xpos, ypos):

    y = ''
    if xpos < 0:
        y = 'Player1 Won!'
    if xpos > 1920:
        y = 'player2 Won!'
    return xpos, ypos, y

def end(p):
    l:bool = True
    while l:
        screen.fill((0, 0, 0))
        print(p)
        if keys[pygame.K_w] and keys[pygame.K_UP]:
            l = False
        pygame.display.flip()

winner:str = 'W and Up to Start'
run:bool = True
while run:
    keys = pygame.key.get_pressed()
    screen.fill((0, 0, 0))
    

    # makes the square
    pygame.draw.line(screen, (255, 0, 0), [0, y1], [0, (y1 + 150)], 5)
    pygame.draw.line(screen, (255, 0, 0), [1920, y2], [1920, (y2 + 150)], 5)
    pygame.draw.circle(screen, (255, 255, 255), [x3,y3], radius=25, width=0)

    if winner:
        end(winner)
        winner = ''

    y1 = Player1(y1, keys)
    y2 = Player2(y2, keys)
    x3, y3, winner = Ball(x3, y3)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()