import pygame , sys , random , os

pygame.init()
pygame.mixer.init()

clock = pygame.time.Clock()

# Set up the screen dimensions, gravity and jump strength
screen_width , screen_height = 500 , 650
gravity = 0.5
jump_strength = -8

# Default colors for pipe, bird, and background (used for skin customization)
current_pipe_color = "green" 
current_bird_color = "yellow" 
current_bg_color = "day"  
selected_bird = "yellow" 
selected_pipe = "green" 
selected_bg = "day" 

# Initialize score
score = 0
# Initialize high score by loading it from a file if it exists
high_score = 0
if os.path.exists("high_score.txt"):
    with open("high_score.txt", "r") as file:
        high_score = int(file.read())

# Set up the screen
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Flappy Bird")
pygame.display.set_icon(pygame.image.load("UI/favicon.ico"))

# Load images and sounds
base_img = pygame.image.load("imgs/base.png").convert_alpha()
retart_img = pygame.image.load("UI/restart_button.png").convert_alpha()
retart_img = pygame.transform.scale(retart_img, (screen_width//3, screen_height//4))
def background_img(color):
    bg_img = pygame.transform.scale2x(pygame.image.load(f"imgs/bg-{color}.png"))
    return bg_img
def bird_img(color):
    bird_imgs = [pygame.image.load(f"imgs/{color}bird{i+1}.png").convert_alpha() for i in range(3)]
    return bird_imgs
def pipe_img(color):
    pipe_image = pygame.image.load(f"imgs/pipe-{color}.png").convert_alpha()
    pipe_image = pygame.transform.scale(pipe_image,(52 , 400))
    return pipe_image
back_button = pygame.transform.scale2x(pygame.image.load("UI/back.png").convert_alpha())
back_rect = back_button.get_rect()
back_rect.topleft = (10, 10)  # Set the position of the back button

flap_sfx = pygame.mixer.Sound("Sound_Effects/wing.ogg")
flap_sfx.set_volume(0.1)
point_sfx = pygame.mixer.Sound("Sound_Effects/point.ogg")
point_sfx.set_volume(0.1)
hit_sfx = pygame.mixer.Sound("Sound_Effects/hit.ogg")
hit_sfx.set_volume(0.1)
# Load and play background music
pygame.mixer.music.load("Sound_Effects/FlappyBirdMusic.mp3")  # Replace with your music file path
pygame.mixer.music.set_volume(0.1)  # Set the volume (0.0 to 1.0)
pygame.mixer.music.play(-1)  # Play the music in a loop

class Bird:
    def __init__(self):
        self.bird_imgs = bird_img(current_bird_color) # Load bird images
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
        self.img = pipe_img(current_pipe_color) # Load the pipe image
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
        if i !="1":
            score_number = pygame.image.load(f"UI/Numbers/{i}.png").convert_alpha()
        else:
            score_number = pygame.transform.scale(pygame.image.load(f"UI/Numbers/1.png").convert_alpha(),(24,36))
        score_list.append(score_number)

# Function to display the skin selection menu and allow the player to choose bird, pipe, and background skins
def choose_skin():
    global bird , current_pipe_color , current_bird_color ,current_bg_color, selected_bird , selected_pipe , selected_bg

    select_text = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 15).render("selected", True, (255, 255, 255),(17, 46, 112))
    

    #load skins for the game
    yellow_bird = pygame.image.load("imgs/yellowbird1.png").convert_alpha()
    yellow_bird_rect = yellow_bird.get_rect(center=(screen_width//3 - 75 , 130))
    red_bird = pygame.image.load("imgs/redbird1.png").convert_alpha()
    red_bird_rect = red_bird.get_rect(center=(screen_width//3 * 2 - 75, 130))
    blue_bird = pygame.image.load("imgs/bluebird1.png").convert_alpha()
    blue_bird_rect = blue_bird.get_rect(center=(screen_width//3 * 3 - 75 , 130))

    red_pipe = pygame.transform.scale(pipe_img("red"),(52 , 200))
    red_pipe_rect = red_pipe.get_rect(center=(screen_width//3  , 290))
    green_pipe = pygame.transform.scale(pipe_img("green"),(52 , 200))
    green_pipe_rect = green_pipe.get_rect(center=(screen_width//3 * 2  , 290))

    bg_img_day = pygame.transform.scale(pygame.image.load("imgs/bg-day.png") , (100 , 100) ) # Load the day background image
    bg_img_day_rect = bg_img_day.get_rect(center= (screen_width//3 , 500))
    bg_img_night = pygame.transform.scale(pygame.image.load("imgs/bg-night.png"), (100,100))  # Load the night background image
    bg_img_night_rect = bg_img_night.get_rect(center=(screen_width//3 * 2 , 500))

    bird = Bird()

    while True: 
        for event in pygame.event.get():    
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.blit(pygame.transform.scale2x(pygame.image.load(f"imgs/bg-{selected_bg}.png")), (0, -300))  # Draw the background
        screen.blit(bg_img_day, bg_img_day_rect)  # Draw the day background image
        screen.blit(bg_img_night, bg_img_night_rect)  # Draw the night background image

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        # bird selection
        if mouse_click[0] == 1 and yellow_bird_rect.collidepoint(mouse_pos):
            bird.bird_imgs = bird_img("yellow")  # Set the bird's images to the selected skin
            bird.image = bird.bird_imgs[0]  # Set the initial bird image
            bird_skin.bird_imgs = bird_img("yellow")
            bird_skin.image = bird.bird_imgs[0]  # Set the skin image to the first frame of the selected bird
            current_bird_color = "yellow"  # Set the current bird color to yellow
            selected_bird = "yellow"
             
        elif mouse_click[0] == 1 and red_bird_rect.collidepoint(mouse_pos):
            bird.bird_imgs = bird_img("red")  # Set the bird's images to the selected skin
            bird.image = bird.bird_imgs[0]
            bird_skin.bird_imgs = bird_img("red")
            bird_skin.image = bird.bird_imgs[0]  # Set the skin image to the first frame of the selected bird
            current_bird_color = "red"  # Set the current bird color to red
            selected_bird = "red"

        elif mouse_click[0] == 1 and blue_bird_rect.collidepoint(mouse_pos):
            bird.bird_imgs = bird_img("blue")  # Set the bird's images to the selected skin
            bird.image = bird.bird_imgs[0]
            bird_skin.bird_imgs = bird_img("blue")
            bird_skin.image = bird.bird_imgs[0]  # Set the skin image to the first frame of the selected bird
            current_bird_color = "blue"  # Set the current bird color to blue
            selected_bird = "blue"
        
        # pipe selection
        elif mouse_click[0] == 1 and red_pipe_rect.collidepoint(mouse_pos):
            current_pipe_color = "red"  # Set the pipe color to red
            selected_pipe = "red"
            
        elif mouse_click[0] == 1 and green_pipe_rect.collidepoint(mouse_pos):
            current_pipe_color = "green"  # Set the pipe color to green
            selected_pipe = "green"

        # background selection  
        elif mouse_click[0] == 1 and bg_img_day_rect.collidepoint(mouse_pos):
            current_bg_color = "day"  # Set the background color to day
            selected_bg = "day"
        elif mouse_click[0] == 1 and bg_img_night_rect.collidepoint(mouse_pos):
            current_bg_color = "night" # Set the background color to night
            selected_bg = "night"
        
        if mouse_click[0] == 1 and back_rect.collidepoint(mouse_pos):
            return
        
        if selected_bird == "yellow":
            screen.blit(select_text, (yellow_bird_rect.x - select_text.get_width()//3 , yellow_bird_rect.y + 30))
        elif selected_bird == "red":
            screen.blit(select_text, (red_bird_rect.x - select_text.get_width()//3 , red_bird_rect.y + 30))
        elif selected_bird == "blue":
            screen.blit(select_text, (blue_bird_rect.x - select_text.get_width()//3 , blue_bird_rect.y + 30))

        if selected_pipe == "red":
            screen.blit(select_text, (red_pipe_rect.x - select_text.get_width()//3 , red_pipe_rect.y + red_pipe_rect.height + 10))
        elif selected_pipe == "green":
            screen.blit(select_text, (green_pipe_rect.x - select_text.get_width()//3 , green_pipe_rect.y + green_pipe_rect.height + 10))

        if selected_bg == "day":
            screen.blit(select_text, (bg_img_day_rect.x - 10 , bg_img_day_rect.y + bg_img_day_rect.height + 10))
            pygame.draw.rect(screen, (0, 0, 0), bg_img_day_rect, 1) # Draw a border around the selected day background
        elif selected_bg == "night":
            screen.blit(select_text, (bg_img_night_rect.x - 10 , bg_img_night_rect.y + bg_img_night_rect.height + 10))
            pygame.draw.rect(screen, (0, 0, 0), bg_img_night_rect, 1) # Draw a border around the selected night background

        skin_text = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 20).render("Choose Your Skin", True, (255, 255, 255))
        screen.blit(skin_text, (screen_width//2 - skin_text.get_width()//2, 50))

        screen.blit(yellow_bird, yellow_bird_rect)  # Draw the yellow bird image
        screen.blit(red_bird,red_bird_rect)  # Draw the red bird image
        screen.blit(blue_bird, blue_bird_rect)  # Draw the blue bird image

        screen.blit(red_pipe, red_pipe_rect)  # Draw the red pipe image
        screen.blit(green_pipe, green_pipe_rect)  # Draw the green pipe image

        screen.blit(back_button, back_rect)  # Draw the back button

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

    pygame.mixer.music.play(-1)  # Restart the background music

    while True:
        bg_img = background_img(current_bg_color)  # Load the background image
        screen.blit(bg_img, (0, -300))  # Draw the background 
        screen.blit(start_menu_img, (screen_width//2 - start_menu_img.get_width()//2,100))  # Draw the start menu image
        bird_skin.rect.center = (screen_width - bird_skin.rect.width, 20)  # Center the bird image
        bird.bird_imgs = bird_skin.bird_imgs  # Set the bird's images to the selected skin
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
            choose_skin()
            
        bird.animate()
        bird.draw()
        bird_skin.draw()
            
        update_bases()  # Update the base positions

        clock.tick(60)  # Limit the frame rate to 60 FPS
        pygame.display.flip()


def game_over_menu():
    global score_list , score , high_score

    game_over_img = pygame.image.load("UI/gameover.png").convert_alpha()

    bg_img = background_img(current_bg_color)  # Load the background image

    # Update high score if the current score is greater
    if score > high_score:
        high_score = score
        with open("high_score.txt", "w") as file:
            file.write(str(high_score))

    pygame.mixer.music.stop()  # Stop the background music

    while True:
        screen.blit(bg_img, (0, -300))  # Draw the background
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                pygame.mixer.music.play(-1)  # Play the music in a loop
                bird.rect.center = (100, screen_height // 2)  # Reset the bird position
                bird.velocity = 0  # Reset the bird's velocity 
                score_list = [pygame.image.load("UI/Numbers/0.png").convert_alpha()]  # Reset the score list
                score = 0  # Reset the score to 0
                return  # Exit the game over menu and restart the game
            
        for pipe in pipe_list:
            pipe.draw()

        screen.blit(back_button, back_rect)  # Draw the back button
            
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if mouse_click[0] == 1 and back_rect.collidepoint(mouse_pos):
            bird.rect.center = (100, screen_height // 2)
            bird.velocity = 0
            start_menu()  # Go back to the start menu when the image is clicked
            break
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
    bg_img = background_img(current_bg_color)  # Load the background image
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
    total_width = 0 
    for i in range(len(score_list)):
        total_width += score_list[i].get_width()
    x = (screen_width - total_width) // 2  # Center the score on the screen
    for i in range(len(score_list)):
        screen.blit(score_list[i], (x + i * score_list[i].get_width(), 50))

    clock.tick(60)
    pygame.display.flip() 