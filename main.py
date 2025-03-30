import pygame , sys , random

pygame.init()

clock = pygame.time.Clock()

screen_width , screen_height = 500 , 650

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("flappy bird")

bg_img = pygame.transform.scale2x(pygame.image.load("imgs/bg.png"))
base_img = pygame.image.load("imgs/base.png").convert_alpha()
pipe_img = pygame.image.load("imgs/pipe.png").convert_alpha()

class Base:
    def __init__(self , x):
        self.base_img = base_img
        self.rect = self.base_img.get_rect()
        self.rect.x = x
        self.rect.y = screen_height - self.rect.height

    def draw(self):
        screen.blit(self.base_img,self.rect)

    def move(self):
        self.rect.x -= 1
        if self.rect.right <= 0 :
            self.rect.x = self.rect.width * 2 


class Pipe:
    def __init__(self):
        self.gap = 130
        self.img = pipe_img
        self.rect = self.img.get_rect()
        self.rect.x = screen_width
        self.rect.y = random.randint( self.gap + 50 , screen_height - base_img.get_height() - 50 )

        self.rotated_img = pygame.transform.rotate(self.img , 180)
        self.rotated_rect = self.rotated_img.get_rect()
        self.rotated_rect.x = screen_width
        self.rotated_rect.bottom = self.rect.y - self.gap

    def draw(self):
        screen.blit(self.img , self.rect)
        screen.blit(self.rotated_img , self.rotated_rect)

    def move(self):
        self.rect.x -= 1
        self.rotated_rect.x -= 1

base_list =[Base(0),Base(base_img.get_width()),Base(base_img.get_width()*2)] 
pipe_list = []


PIPE_SPAWN_EVENT = pygame.USEREVENT
pygame.time.set_timer(PIPE_SPAWN_EVENT , 3000)

while True:
    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == PIPE_SPAWN_EVENT:
            pipe_list.append(Pipe())

    screen.blit(bg_img,(0,-300))

    for pipe in pipe_list[:]:
        pipe.draw()
        pipe.move()

        if pipe.rect.right <= 0 :
            pipe_list.remove(pipe)

    for base in base_list:
        base.draw()
        base.move()
    clock.tick(60)
    pygame.display.flip()