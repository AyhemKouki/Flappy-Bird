import pygame , sys , random , os

pygame.init()
pygame.mixer.init()

clock = pygame.time.Clock()

# Set up the screen dimensions and gravity
screen_width , screen_height = 500 , 650
gravity = 0.5
jump_strength = -8

score = 0
# Initialize high score
high_score = 0
if os.path.exists("high_score.txt"):
    with open("high_score.txt", "r") as file:
        high_score = int(file.read())

# Set up the screen
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Flappy Bird")
pygame.display.set_icon(pygame.image.load("UI/favicon.ico"))

# Load images and sounds
bg_img = pygame.transform.scale2x(pygame.image.load("imgs/bg.png"))
base_img = pygame.image.load("imgs/base.png").convert_alpha()
pipe_img = pygame.image.load("imgs/pipe.png").convert_alpha()
retart_img = pygame.image.load("UI/restart_button.png").convert_alpha()
retart_img = pygame.transform.scale(retart_img, (screen_width//3, screen_height//4))
def bird_img(color):
    bird_imgs = [pygame.image.load(f"imgs/{color}bird{i+1}.png").convert_alpha() for i in range(3)]
    return bird_imgs

flap_sfx = pygame.mixer.Sound("Sound_Effects/wing.ogg")
flap_sfx.set_volume(0.1)
point_sfx = pygame.mixer.Sound("Sound_Effects/point.ogg")
point_sfx.set_volume(0.1)
hit_sfx = pygame.mixer.Sound("Sound_Effects/hit.ogg")
hit_sfx.set_volume(0.1)

class Bird:
    def __init__(self):
        self.bird_imgs = bird_img("yellow") # Load bird images
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
        flap_sfx.play()

    def move(self):
        self.velocity += gravity
        self.rect.y += self.velocity

        # Check for collision with the base
        if self.rect.bottom >= screen_height - base_img.get_height():
            self.rect.bottom = screen_height - base_img.get_height()
            self.velocity = 0
            hit_sfx.play() # Play the hit sound effect
            # Show game over menu
            game_over_menu()
            pipe_list.clear()  # Clear the pipes when the bird hits the base

        # Check for collision with the top of the screen
        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0

    def draw(self):
        angle = min(max(self.velocity * -5, -25), 25)
        self.rotated_bird = pygame.transform.rotate(self.image, angle) # Cap angle between -25 and 25 degrees
        screen.blit(self.rotated_bird, self.rect)

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
            self.rect.x = self.rect.width * 2 # Reset the base position when it goes off screen

class Pipe:
    def __init__(self):
        self.gap = 130
        self.img = pipe_img
        self.rect = self.img.get_rect()
        self.rect.x = screen_width
        self.rect.y = random.randint( self.gap + 50 , screen_height - base_img.get_height() - 50 )
        self.passed = False
        self.rotated_img = pygame.transform.rotate(self.img , 180)
        self.rotated_rect = self.rotated_img.get_rect()
        self.rotated_rect.x = screen_width
        self.rotated_rect.bottom = self.rect.y - self.gap

    def draw(self):
        screen.blit(self.img , self.rect)
        screen.blit(self.rotated_img , self.rotated_rect)

    def move(self):
        global score
        self.rect.x -= 1
        self.rotated_rect.x -= 1

        if self.rect.right <= bird.rect.left and not self.passed:
            point_sfx.play()
            self.passed = True
            score += 1
            display_score()

    def collide(self):
        return self.rect.colliderect(bird.rect) or self.rotated_rect.colliderect(bird.rect)

def display_score():
    score_list.clear() # Clear the previous score images
    for i in str(score):
        score_number = pygame.image.load(f"UI/Numbers/{i}.png").convert_alpha()
        score_list.append(score_number)
    
def choose_skin():
    yellow_bird = pygame.image.load("imgs/yellowbird1.png").convert_alpha()
    yellow_bird_rect = yellow_bird.get_rect(center=(screen_width//3 - 75 , 130))
    red_bird = pygame.image.load("imgs/redbird1.png").convert_alpha()
    red_bird_rect = red_bird.get_rect(center=(screen_width//3 * 2 - 75, 130))
    blue_bird = pygame.image.load("imgs/bluebird1.png").convert_alpha()
    blue_bird_rect = blue_bird.get_rect(center=(screen_width//3 * 3 - 75 , 130))

    global bird
    bird = Bird()

    while True:
        for event in pygame.event.get():    
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if mouse_click[0] == 1 and yellow_bird_rect.collidepoint(mouse_pos):
            bird.bird_imgs = bird_img("yellow")  # Set the bird's images to the selected skin
            bird.image = bird.bird_imgs[0]  # Set the initial bird image
            bird_skin.bird_imgs = bird_img("yellow")
            bird_skin.image = bird.bird_imgs[0]  # Set the skin image to the first frame of the selected bird
            return "yellow"
        if mouse_click[0] == 1 and red_bird_rect.collidepoint(mouse_pos):
            bird.bird_imgs = bird_img("red")  # Set the bird's images to the selected skin
            bird.image = bird.bird_imgs[0]
            bird_skin.bird_imgs = bird_img("red")
            bird_skin.image = bird.bird_imgs[0]  # Set the skin image to the first frame of the selected bird
            return "red"
        if mouse_click[0] == 1 and blue_bird_rect.collidepoint(mouse_pos):
            bird.bird_imgs = bird_img("blue")  # Set the bird's images to the selected skin
            bird.image = bird.bird_imgs[0]
            bird_skin.bird_imgs = bird_img("blue")
            bird_skin.image = bird.bird_imgs[0]  # Set the skin image to the first frame of the selected bird
            return "blue"
        screen.blit(bg_img, (0, -300))  # Draw the background

        skin_text = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 20).render("Choose Your Skin", True, (255, 255, 255))
        screen.blit(skin_text, (screen_width//2 - skin_text.get_width()//2, 50))

        screen.blit(yellow_bird, yellow_bird_rect)  # Draw the yellow bird image
        screen.blit(red_bird,red_bird_rect)  # Draw the red bird image
        screen.blit(blue_bird, blue_bird_rect)  # Draw the blue bird image

        clock.tick(60)  # Limit the frame rate to 60 FPS
        pygame.display.flip()  # Update the display

def update_bases():
    for base in base_list:
        base.draw()
        base.move()


def start_menu():
    start_menu_img = pygame.image.load("UI/start.png").convert_alpha()
    start_menu_img = pygame.transform.scale(start_menu_img, (screen_width//2, screen_height//2))

    select_skin_text = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 10).render("skins", True, (255, 255, 255))

    while True:
        screen.blit(bg_img, (0, -300))  # Draw the background 
        screen.blit(start_menu_img, (screen_width//2 - start_menu_img.get_width()//2,100))  # Draw the start menu image
        bird_skin.rect.center = (screen_width - bird_skin.rect.width, 20)  # Center the bird image
        screen.blit(select_skin_text, (bird_skin.rect.x - 5 , bird_skin.rect.y + 30))  # Draw the text
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return  # Exit the start menu and start the game
        
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if mouse_click[0] == 1 and bird_skin.rect.collidepoint(mouse_pos):
            skin_color = choose_skin()
        bird.animate()
        bird.draw()
        bird_skin.draw()
            
        update_bases()  # Update the base positions

        clock.tick(60)  # Limit the frame rate to 60 FPS
        pygame.display.flip()


def game_over_menu():
    global score_list , score , high_score

    game_over_img = pygame.image.load("UI/gameover.png").convert_alpha()

    # Update high score if the current score is greater
    if score > high_score:
        high_score = score
        with open("high_score.txt", "w") as file:
            file.write(str(high_score))

    while True:
        screen.blit(bg_img, (0, -300))  # Draw the background
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                bird.rect.center = (100, screen_height // 2)  # Reset the bird position
                bird.velocity = 0  # Reset the bird's velocity 
                score_list = [pygame.image.load("UI/Numbers/0.png").convert_alpha()]  # Reset the score list
                score = 0  # Reset the score to 0
                return  # Exit the game over menu and restart the game
            
        for pipe in pipe_list:
            pipe.draw()

        for base in base_list: 
            base.draw()
        
        screen.blit(bird.rotated_bird, bird.rect)
        
        screen.blit(game_over_img, (screen_width//2 - game_over_img.get_width()//2, 100))  # Draw the game over image

        screen.blit(retart_img, (screen_width//2 - retart_img.get_width()//2, 300))  # Draw the restart image
        # Draw the score
        total_width = score_list[0].get_width() * len(score_list)
        x = (screen_width - total_width) // 2  # Center the score on the screen
        for i in range(len(score_list)):
            screen.blit(score_list[i], (x + i * score_list[0].get_width(), 50))

        # Display high score in the game over menu
        high_score_text = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 20).render(f"High Score: {high_score}", True, (255, 255, 255))
        screen.blit(high_score_text, (screen_width // 2 - high_score_text.get_width() // 2, 200))

            
        clock.tick(60)  # Limit the frame rate to 60 FPS
        pygame.display.flip()  # Update the display

# Initialize the base , pipe and bird objects
base_list =[Base(0),Base(base_img.get_width()),Base(base_img.get_width()*2)] 
pipe_list = []
bird = Bird()
bird_skin = Bird()
score_list = [pygame.image.load("UI/Numbers/0.png").convert_alpha()]  # Initialize the score list

# Set up a timer event for spawning pipes
# This event will be triggered every 3000 milliseconds (3 seconds)
PIPE_SPAWN_EVENT = pygame.USEREVENT
pygame.time.set_timer(PIPE_SPAWN_EVENT , 3000)

start_menu()  # Show the start menu before the game begins

# Main game loop
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

    screen.blit(bg_img,(0,-300)) # Draw the background

    bird.draw()
    bird.move()
    bird.animate()

    for pipe in pipe_list[:]:
        pipe.draw()
        pipe.move()

        if pipe.rect.right <= 0 :
            pipe_list.remove(pipe)

        if pipe.collide():
            hit_sfx.play() # Play the hit sound effect
            game_over_menu() # Show game over menu
            pipe_list.clear() # Clear the pipes when the bird collides with a pipe

    update_bases() # Update the base positions
    
    # Draw the score
    total_width = score_list[0].get_width() * len(score_list)
    x = (screen_width - total_width) // 2  # Center the score on the screen
    for i in range(len(score_list)):
        screen.blit(score_list[i], (x + i * score_list[0].get_width(), 50))

    clock.tick(60)
    pygame.display.flip()