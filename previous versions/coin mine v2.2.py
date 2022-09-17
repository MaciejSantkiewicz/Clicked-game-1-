import random
from pygame.locals import *
import pygame


#-------------SETTINGS:

    

#-----
pygame.init() #main game function
game_window_width = 1280
game_window_height = 720

screen = pygame.display.set_mode((game_window_width, game_window_height)) #game window 
pygame.display.set_caption("Coin mine")  #game name
font = pygame.font.Font("font/Pixeltype.ttf", 40) #main font

#-----Sprites
    
class Buttons(pygame.sprite.Sprite):   #main button, rectangular shape sprite generator
    def __init__(self, width, heigth, pos_x, pos_y, elevation, color, hover_color): #values provided by the user
        super().__init__()
        self.action = False #stored value that will be returned/will make buttons works only one with every click. Prevents from clicking button more than once with every click
        self.pressed = False #checks if the button is pressed
        self.elevation = elevation #how high should be the main button from the original coordinance
        self.dynamic_elevation = elevation #to store original elevention. elevation will change with every button press to give it that button press animation
        self.original_y_pos = pos_y #stores original position
        self.color = color #button color
        self.original_color = color #store original button color. Color will change when use hovers the mouse over the this button
        self.hover_color = hover_color

        self.top_rect = pygame.Rect(pos_x, pos_y, width, heigth)
        self.top_rect.center = pos_x, pos_y
        self.top_rect_shadow = pygame.Rect(pos_x, pos_y, width, heigth)
        self.top_rect_shadow.midtop = pos_x, pos_y
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
            self.color = self.hover_color
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
    

class Buttons_image(pygame.sprite.Sprite): #same as Button class, but instead of rectangles it can render a image as button
    def __init__(self, path, pos, scale_x, scale_y, elevation): 
        super().__init__()
        self.action = False
        self.pressed = False
        self.path = path
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_pos = pos[1]
        self.image = pygame.image.load(self.path).convert_alpha()
        self.image= pygame.transform.scale(self.image, (scale_x, scale_y))
        self.image_rect = self.image.get_rect(center=(pos))


    
    def draw(self):
        self.action = False
        self.image_rect.y = self.original_y_pos - self.dynamic_elevation
        screen.blit(self.image, self.image_rect)
        self.check_click()
        



    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.image_rect.collidepoint(mouse_pos):
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

        return self.action


class Coin_Animation(pygame.sprite.Sprite):
    def __init__(self, path):
        super().__init__()
        self.alphavalue = 255
        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (32,32))
        self.rect = self.image.get_rect(center = ((game_window_width/2),(game_window_height/2)))

    def update(self):
        self.rect.y -= 5

        self.destroy()

    
    def destroy(self):
        if self.rect.y <= 250:
            self.kill()


class Text_gui(pygame.sprite.Sprite):
    def __init__(self, text, pos, size, attachpoint):
        gui_font = pygame.font.Font("font/Pixeltype.ttf", size)
        self.pos = pos
        self.attachpoint = attachpoint

        self.text_surf = gui_font.render(text, 4, "#1F1F1F")
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




animation_group = pygame.sprite.Group()

button1 = Buttons(100, 100, (game_window_width/2), (game_window_height/2), 8, '#FF6904', "#F3890F")

button2 = Buttons(100, 100, 100, 100, 5, "#46A146", "#40A9E6")
button2_2 = Buttons(40, 40, 200, 100, 5, '#46A146', "#40A9E6")


button3 = Buttons(100, 100, (game_window_width - 100), 100, 5, "#7346A1", "#40A9E6")
button3_2 = Buttons(40, 40, (game_window_width - 200), 100, 5, '#7346A1' , "#40A9E6")

button4 = Buttons_image("sprites/coin.png", (400, 300), 64, 64, 5) #not used yet

button5 = Buttons(100, 100, 100, 300, 5, "#46A146", "#40A9E6")


idle_coins_gain = 1000
coin_timer = pygame.USEREVENT + 1
pygame.time.set_timer(coin_timer,idle_coins_gain)

animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(animation_timer,2000)


#-------------GAME:9

active = False
clock = pygame.time.Clock()
coins = 0
click_power = 1
click_power_upgrade_cost = 10
auto_clic_power_buyer_cost = 5

idle_gain = 1
idle_gain_upgrade_cost = 50

tool_list = ["Iron Pickaxe", "Gold Pickaxe", "Diamond pickaxe"]
max_tool = len(tool_list) - 1
current_tool = 0

tool_power = 0
miners_quantity = 1

max_gem_chance = 100
min_gem_chance = 1

gem_chance_cost = 1000

tool_gem_chance = 1

idle_coins_gain = 200

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = True
            pygame.quit()
            exit()          

        
        if event.type == coin_timer:
            coins += idle_gain

        
    


    if not active:


        gem_spawn = random.uniform(min_gem_chance, max_gem_chance)
        tool_gem_chance_overall = (tool_gem_chance  / max_gem_chance) * 100 

        
        screen.fill("#D7D7D7")


        #texts 
        #coins text
        coin_text = Text_gui(f"Coins: {coins:.0f}", ((game_window_width/2), 40), 40, "center")
        coin_text.draw()
     
        
        icon_coin = Icons("sprites/coin.png", (game_window_width/2), 80, 32, 32)
        icon_coin.draw()

        #click_power text
        click_power_text = Text_gui(f"Click power: {click_power}", (10, 30), 35, "topleft")
        click_power_text.draw()

        click_power_upgrade_text = Text_gui(f"Upgrade cost: {click_power_upgrade_cost:.0f}", (10, 60), 35, "topleft")
        click_power_upgrade_text.draw()

        click_power_max = Text_gui(f"Buy MAX", (170, 150), 30, "topleft")
        click_power_max.draw()

        click_tool_text = Text_gui(f"Tool: {tool_list[current_tool]}" + f"  +{tool_power}", (10, 215), 35, "topleft")
        click_tool_text.draw()

        click_tool_text = Text_gui(f"Gem chance: {tool_gem_chance_overall:.2f}%", (10, 420), 35, "topleft")
        click_tool_text.draw()

        cost_upgrade_text = Text_gui(f"Upgrade cost: {gem_chance_cost:.0f}", (10, 445), 35, "topleft")
        cost_upgrade_text.draw()

        #idle_coin_gain text
        idle_coin_gain_text = Text_gui(f"Idle gain:  {idle_gain}/sec", ((game_window_width-10), 30), 35, "topright")
        idle_coin_gain_text.draw()

        idle_power_upgrade_text = Text_gui(f"Upgrade cost: {idle_gain_upgrade_cost:.0f}", ((game_window_width-10), 60), 35, "topright")
        idle_power_upgrade_text.draw()

        click_power_max = Text_gui(f"Buy MAX", ((game_window_width-170), 150), 30, "topright")
        click_power_max.draw()

        click_tool_text = Text_gui(f"Workers: {miners_quantity}", ((game_window_width-10), 215), 35, "topright")
        click_tool_text.draw()

        #buttons

        button1.draw() #click button
        if button1.check_click():
            coins += click_power
            animation_group.add(Coin_Animation("sprites/coin.png"))

            if gem_spawn <= tool_gem_chance_overall:
                animation_group.add(Coin_Animation("sprites/gem.png"))
                coins += click_power * 100
        
        animation_group.draw(screen)
        animation_group.update()



        button2.draw() #click power button
        if button2.check_click():
            if coins >= click_power_upgrade_cost:
                coins = coins - click_power_upgrade_cost
                click_power += 1
                click_power_upgrade_cost = (click_power_upgrade_cost * 2.5) - 1
                tool_power +=1



        button2_2.draw()
        if button2_2.check_click():
            while coins >= click_power_upgrade_cost:
                coins = coins - click_power_upgrade_cost
                click_power += 1
                click_power_upgrade_cost = (click_power_upgrade_cost * 2.5) - 1
                tool_power +=1


        button5.draw()
        if button5.check_click():
            if coins >= gem_chance_cost:
                coins = coins - gem_chance_cost
                gem_chance_cost = (gem_chance_cost * 1.5) - 1
                if tool_gem_chance_overall <= 100:
                        tool_gem_chance += 0.25

                if tool_gem_chance_overall >= 100:
                    tool_gem_chance -= 100
            


        button3.draw() #idle power button
        if button3.check_click():
            if coins >= idle_gain_upgrade_cost:
                coins = coins - idle_gain_upgrade_cost
                idle_gain += 1
                idle_gain_upgrade_cost = (idle_gain_upgrade_cost * 1.2) - 1
                miners_quantity += 1


        button3_2.draw()
        if button3_2.check_click():
            if coins >= idle_gain_upgrade_cost:
                coins = coins - idle_gain_upgrade_cost
                idle_gain += 1
                idle_gain_upgrade_cost = (idle_gain_upgrade_cost * 1.2) - 1
                miners_quantity += 1

    

        pygame.display.update()
        clock.tick(60)
