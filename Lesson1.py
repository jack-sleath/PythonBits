import pygame
pygame.init()

screen = pygame.display.set_mode([500,500])
running = True

#Pos setup
x=250
y=250

#Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    screen.fill((255,255,255))

    pygame.draw.circle(screen, (0,0,255),(x,y),75)

    keypressed = pygame.key.get_pressed()

    if keypressed[pygame.K_d]:
        x+=1
    if keypressed[pygame.K_a]:
        x-=1
    if keypressed[pygame.K_w]:
        y-=1
    if keypressed[pygame.K_s]:
        y+=1
    
    if x > 480:
        x=480
    if x < 20:
        x=20
    if y > 480:
        y=480
    if y < 20:
        y=20
    

    pygame.display.flip()

pygame.quit()