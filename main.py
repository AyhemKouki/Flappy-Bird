import pygame , sys , random

pygame.init()

clock = pygame.time.Clock()

screen_width , screen_height = 500 , 650
gravity = 0.5
jump_strength = -8

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("flappy bird")

bg_img = pygame.transform.scale2x(pygame.image.load("imgs/bg.png"))
base_img = pygame.image.load("imgs/base.png").convert_alpha()
pipe_img = pygame.image.load("imgs/pipe.png").convert_alpha()
bird_imgs = [pygame.image.load(f"imgs/bird{i+1}.png").convert_alpha() for i in range(3)]

class Bird:
    def __init__(self):
        self.bird_imgs = bird_imgs
        self.index = 0
        self.image = self.bird_imgs[self.index]
        self.rect = self.image.get_rect(center=(100, screen_height // 2))
        self.velocity = 0
        self.animate_time = 0
    
    def animate(self):
        self.animate_time += 1
        if self.animate_time % 5 == 0:
            self.index += 1
            if self.index >= len(self.bird_imgs):
                self.index = 0
            self.image = self.bird_imgs[self.index]

    def jump(self):
        self.velocity = jump_strength

    def move(self):
        self.velocity += gravity
        self.rect.y += self.velocity
        if self.rect.bottom >= screen_height - base_img.get_height():
            self.rect.bottom = screen_height - base_img.get_height()
            self.velocity = 0

        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0

    def draw(self):
        angle = min(max(self.velocity * -5, -25), 25)
        rotated_bird = pygame.transform.rotate(self.image, angle) # Cap angle between -25 and 25 degrees
        rotated_rect = rotated_bird.get_rect(center=self.rect.center)
        screen.blit(rotated_bird, rotated_rect)


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

    def collide(self):
        return self.rect.colliderect(bird.rect) or self.rotated_rect.colliderect(bird.rect)

base_list =[Base(0),Base(base_img.get_width()),Base(base_img.get_width()*2)] 
pipe_list = []
bird = Bird()


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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()

    screen.blit(bg_img,(0,-300))

    bird.draw()
    bird.move()
    bird.animate()

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