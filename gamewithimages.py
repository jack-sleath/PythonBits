import pygame
import random

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)



screen_width = 700
screen_height = 400

class Block(pygame.sprite.Sprite):
    def __init__(self, image_path, width, height):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()  # Load with transparency
        self.image = pygame.transform.scale(self.image, (width, height))  # Resize
        self.rect = self.image.get_rect()
    
    def reset_pos(self):
        self.rect.y = random.randrange(-300, -20)
        self.rect.x = random.randrange(0, screen_width)
    
    def update(self):
        self.rect.y += 1
        if self.rect.y > 410:
            self.reset_pos()

class Player(Block):
    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

pygame.init()

font = pygame.font.Font(None, 36)  # Use default font, size 36

screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("Block Dodger")

block_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()

for _ in range(50):
    block = Block("block.png", 20, 10)  # Replace with your image filename

    block.reset_pos()
    block_list.add(block)
    all_sprites_list.add(block)

player = Player("player.png", 50, 50)
all_sprites_list.add(player)

done = False
clock = pygame.time.Clock()

score = 0

savings = random.randrange(10,50)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.fill(WHITE)

    all_sprites_list.update()

    block_hit_list = pygame.sprite.spritecollide(player, block_list, False)

    for block in block_hit_list:
        score+=1
        block.reset_pos()
    
    all_sprites_list.draw(screen)

    score_text = font.render(f"Savings: {score}/{savings}", True, BLACK)
    screen.blit(score_text, (10, 10))


    pygame.display.flip()

    clock.tick(240)

    if(score>=savings):
        score = 0
        savings = random.randrange(10,50)

pygame.quit()