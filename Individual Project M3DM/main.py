import pygame
import time
import random
pygame.font.init()

#adjustable screen window sizes
Width = 1280
Height = 1024

#player
Player_width = 37
Player_height = 15
Player_speed = 6

#enemy bullet
Bullet_width = 15
Bullet_height = 20
Bullet_speed = 4

font = pygame.font.SysFont("Bauhaus 93", 30) #font used in the game

WIN = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Game individual project Kian")

BG = pygame.transform.scale(pygame.image.load("skybackground.png"), (Width, Height)) #this does not preserve aspect ratio 16:9

player_model = pygame.image.load("playership.png")
player_model = pygame.transform.scale(player_model, (80, 120)) #values for scaling the player model


def draw(player, survived_time, bullets):
    WIN.blit(BG, (0, 0)) #blit is a method for drawing an image or surface on the screen in python
    
    time_text = font.render(f"Time: {round(survived_time)}s", 1, "black")
    WIN.blit(time_text, (10, 10)) #this values moves the text around on the screen, set to 10,10 to make the text appear in the topleft corner

    player_model_center = player_model.get_rect(center=player.center)
    
    pygame.draw.rect(WIN, (0, 255, 255), player)
    
    WIN.blit(player_model, (player_model_center.topleft))
    
     #RGB colour code.

    for bullet in bullets:
        pygame.draw.rect(WIN, "red", bullet)
    
    pygame.display.update()



def play():

    player = pygame.Rect(200, Height - Player_height, Player_width, Player_height)

    clock = pygame.time.Clock()

    start_time = time.time()
    survived_time = 0

    bullet_add_increment = 2000 #the time between bullet barrages
    bullet_timer = 0

    bullets = []
    hit = False

    run = True

    while run: #this is the main game loop
        
        bullet_timer += clock.tick(60) #this makes sure the gamespeed isnt bound to how fast your computer can run through this loop
        survived_time = time.time() - start_time
        
        if bullet_timer > bullet_add_increment:
            for _ in range(4):  #the 4 is the amount of bullets, change this to change difficulty
                bullet_x = random.randint(0, Width - Bullet_width)
                bullet = pygame.Rect(bullet_x, -Bullet_height, Bullet_width, Bullet_height) #the -Bullet height makes it so that it looks like the bullets fade in from the top of the screen
                bullets.append(bullet) 

            bullet_add_increment = max(200, bullet_add_increment - 50) #the 50 is the amount of milliseconds the time between barrages decreases each time higher value means faster difficulty ramping.
            bullet_timer = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                

        keys = pygame.key.get_pressed() #playermovement script
        if keys[pygame.K_LEFT] and player.x - Player_speed >= 0:
            player.x -= Player_speed
        if keys[pygame.K_RIGHT] and player.x + Player_speed + Player_width <= Width:
            player.x += Player_speed
        if keys[pygame.K_DOWN] and player.y + Player_speed + Player_height <= Height:
            player.y += Player_speed
        if keys[pygame.K_UP] and player.y - Player_speed >= 0:
            player.y -= Player_speed


        for bullet in bullets[:]:
            bullet.y += Bullet_speed
            if bullet.y > Height:
                bullets.remove(bullet)
            elif bullet.y + Bullet_height >= player.y and bullet.colliderect(player):
                bullets.remove(bullet)
                hit = True
                break

        if hit:
            lost_text = font.render("Game over", 1, "red")
            WIN.blit(lost_text, (Width/2 - lost_text.get_width()/2, Height/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(3000)
            run = False
        

        draw(player, survived_time, bullets)

    main_menu()


def options():
    
    while True:

        Options_mouse_pos = pygame.mouse.get_pos()

        WIN.fill("white")

        Options_text = font.render("You can move the player using the arrow keys!", True, "Black")   #add difficulty sliders for bullet settings or amounts of bullets here
        Options_rect = Options_text.get_rect(center=(640, 260))
        WIN.blit(Options_text, Options_rect)

        Options_back = Button(image=None, pos=(640, 460),
                            text_input="BACK", font=font, base_color="Black")
        
        Options_back.update(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Options_back.check_for_input(Options_mouse_pos):
                    main_menu()

        pygame.display.update()



class Button(): #defines what buttons are
    def __init__(self, image, pos, text_input, font, base_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.text_input = text_input
        self.base_color = base_color
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def check_for_input(self, position):    #checks if a button is pressed
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False


def main_menu():
    while True:
        WIN.blit(BG, (0, 0))

        Menu_mouse_pos = pygame.mouse.get_pos()

        Menu_text = font.render("MAIN MENU", True, "#34d2eb")   #hexcolor code
        Menu_rect = Menu_text.get_rect(center=(640, 100))

        Play_button = Button(image=pygame.image.load("GreenButton.png"), pos=(640, 250),
                             text_input="PLAY", font=font, base_color="#d7fcd4")
        
        Options_button = Button(image=pygame.image.load("BlackButton.png"), pos=(640, 400),
                             text_input="Controls", font=font, base_color="#d7fcd4")
        
        Quit_button = Button(image=pygame.image.load("RedButton.png"), pos=(640, 550),
                             text_input="QUIT", font=font, base_color="#d7fcd4")
        
        WIN.blit(Menu_text, Menu_rect)

        for button in [Play_button, Options_button, Quit_button]:
            button.update(WIN)

        for event in pygame.event.get():    #if you press the X on the top right of the window the program also closes
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:    #checks if the cursor was over a button when pressed down
                if Play_button.check_for_input(Menu_mouse_pos):
                    play()
                if Options_button.check_for_input(Menu_mouse_pos):
                    options()
                if Quit_button.check_for_input(Menu_mouse_pos):
                    pygame.quit()

            pygame.display.update()


if __name__ == "__main__":
    main_menu()