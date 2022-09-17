
import pygame


#-------------SETTINGS:

    

#-----
pygame.init()
screen = pygame.display.set_mode((800,400)) 
pygame.display.set_caption("Coin mine") 
font = pygame.font.Font("font/Pixeltype.ttf", 40)

#-----Sprites
    
class Buttons(pygame.sprite.Sprite):
    def __init__(self, width, heigth, pos, elevation, color):
        super().__init__()
        self.action = False
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_pos = pos[1]
        self.color = color
        self.original_color = color

        self.top_rect = pygame.Rect(pos, (width, heigth))
        self.top_rect_shadow = pygame.Rect(pos, (width, heigth))
        self.top_color = "#3AA5EC"



    
    def draw(self):
        self.action = False
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        pygame.draw.rect(screen, '#545454', self.top_rect_shadow, border_radius= 10)
        pygame.draw.rect(screen, self.color, self.top_rect, border_radius= 10)
        self.check_click()



    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.color = "#25D2CD"
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.pressed = True
            else:
                if self.pressed == True:
                    self.action = True
                    self.dynamic_elevation = self.elevation
                    self.pressed = False
                
        else: 
            self.dynamic_elevation = self.elevation
            self.color = self.original_color

        return self.action
    


class Text_gui(pygame.sprite.Sprite):
    def __init__(self, text, pos, size, attachpoint):
        gui_font = pygame.font.Font("font/Pixeltype.ttf", size)
        self.pos = pos
        self.attachpoint = attachpoint

        self.text_surf = gui_font.render(text, True, "#1F1F1F")
        if self.attachpoint == "topright":
            self.text_rect = self.text_surf.get_rect(topright = (self.pos))
        if self.attachpoint == "center":
            self.text_rect = self.text_surf.get_rect(center = (self.pos))
        if self.attachpoint == "topleft":
            self.text_rect = self.text_surf.get_rect(topleft = (self.pos))
    def draw(self):
        screen.blit(self.text_surf, self.text_rect)


class Icons(pygame.sprite.Sprite):
    def __init__(self, path, pos_x, pox_y, scale_x, scale_y):
        self.icon_path = path
        self.icon_img = pygame.image.load(path).convert_alpha()
        self.icon_img = pygame.transform.scale(self.icon_img, (scale_x, scale_y))
        self.icon_rect = self.icon_img.get_rect(center=(pos_x, pox_y))

    def draw (self):
        screen.blit(self.icon_img, self.icon_rect)


button1 = Buttons(100, 100, (350, 100), 5, '#737371')
button2 = Buttons(100, 100, (50, 100), 5, "#737371")
button3 = Buttons(100, 100, (650, 100), 5, "#737371")







#-------------GAME:9

active = False
clock = pygame.time.Clock()
coins = 0
click_power = 1
click_power_upgrade_cost = 10
auto_clic_power_buyer_cost = 5

idle_gain = 1
idle_gain_upgrade_cost = 50

idle_coins_gain = 1000
coin_timer = pygame.USEREVENT + 1
pygame.time.set_timer(coin_timer,idle_coins_gain)

while not active:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = True            
        if event.type == coin_timer:
            coins += idle_gain


    screen.fill("lightblue")

    #texts 
    #coins text
    coin_text = Text_gui(f"Coins: {coins}", (350, 30), 40, "topleft")
    coin_text.draw()
    
    icon_coin = Icons("sprites/coin.png", 320, 40, 32, 32)
    icon_coin.draw()

    #click_power text
    click_power_text = Text_gui(f"Click power: {click_power}", (10, 30), 35, "topleft")
    click_power_text.draw()

    click_power_upgrade_text = Text_gui(f"Upgrade cost: {click_power_upgrade_cost}", (10, 60), 35, "topleft")
    click_power_upgrade_text.draw()

    #idle_coin_gain text
    idle_coin_gain_text = Text_gui(f"Idle gain:  {idle_gain}/sec", (790, 30), 35, "topright")
    idle_coin_gain_text.draw()

    idle_power_upgrade_text = Text_gui(f"Upgrade cost: {idle_gain_upgrade_cost}", (790, 60), 35, "topright")
    idle_power_upgrade_text.draw()

    #buttons

    button1.draw() #click button
    if button1.check_click():
        coins += click_power


    button2.draw() #click power button
    if button2.check_click():
        if coins >= click_power_upgrade_cost:
            coins = coins - click_power_upgrade_cost
            click_power += 1
            click_power_upgrade_cost = click_power_upgrade_cost + 15

    button3.draw() #idle power button
    if button3.check_click():
        if coins >= idle_gain_upgrade_cost:
            coins = coins - idle_gain_upgrade_cost
            idle_gain += 1
            idle_gain_upgrade_cost = idle_gain_upgrade_cost + 50




    pygame.display.update()
    clock.tick(60)
pygame.quit()