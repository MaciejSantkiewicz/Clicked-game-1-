import random
import pygame



#--------SETTINGS:
pygame.init() #main game function
game_window_width = 1280 #game window width
game_window_height = 720 #game window height

screen = pygame.display.set_mode((game_window_width, game_window_height)) #game window 
pygame.display.set_caption("Coin mine")  #game's name
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
        self.hover_color = hover_color #changes button color when hovered

        self.top_rect = pygame.Rect(pos_x, pos_y, width, heigth) #renders rectangular
        self.top_rect.center = pos_x, pos_y #sets render point of the rectangular 
        self.top_rect_shadow = pygame.Rect(pos_x, pos_y, width, heigth) #renders shadow(clone) uder the main button, with the same parameters
        self.top_rect_shadow.midtop = pos_x, pos_y #sets render point of the rectangular 
        self.top_color = "#3AA5EC" #idle button color




    
    def draw(self):
        self.action = False #return action (used to make button do something when clicked)
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation #place the button a bit higher from original Y position to simulate pushing animation when clicked
        pygame.draw.rect(screen, '#545454', self.top_rect_shadow, border_radius= 10) #renders button on the screen
        pygame.draw.rect(screen, self.color, self.top_rect, border_radius= 10) #renders button's shadow on the screen
        self.check_click() #runs click function



    def check_click(self): #click function
        mouse_pos = pygame.mouse.get_pos() #gets the position of the mouse
        if self.top_rect.collidepoint(mouse_pos): #check if the mouse is hovering over the button
            self.color = self.hover_color #chenges the button color if mouse is hovering over it
            if pygame.mouse.get_pressed()[0]: #checks if LMB is clicked while hovering over the button
                self.dynamic_elevation = 0 #animates button press/changes the Y axis of the button(sets elevation value to 0)
                self.pressed = True #returns "True" value when button is pressed
            else:
                if self.pressed == True: #after clicking retruns the button to unpressed position and state
                    self.action = True #returns action value that can be used later as a function of button
                    self.dynamic_elevation = self.elevation #returns Y axis of the button to previous value
                    self.pressed = False #returns button to unpressed position and value
                
        else: 
            self.dynamic_elevation = self.elevation #while being upressed, button will remain in the elevation Y axis value
            self.color = self.original_color #while being upressed, button will remain in the idle color

        return self.action #returns the value of button (if it has been pressed or not)
    

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


class Coin_Animation(pygame.sprite.Sprite): #renders an image that will move on the vertical exit 
    def __init__(self, path): #value provided by the user
        super().__init__()
        self.image = pygame.image.load(path).convert_alpha() #loads the image from game's folder
        self.image = pygame.transform.scale(self.image, (48,48)) #set the image view and scale
        self.rect = self.image.get_rect(center = ((game_window_width/2),(game_window_height/2))) #places this animation in the middle of the screen

    def update(self): #updates the Y position axis of the images with every frame
        self.rect.y -= 5 #how fast will image move up with every frame

        self.destroy() #runs function that will remove the image if it exceeds over the Y position limit

    
    def destroy(self): #remove image funtion
        if self.rect.y <= 250: #at what Y axis position value image should be removed
            self.kill() #removes the image / stops the function


class Text_gui(pygame.sprite.Sprite): #text sprite
    def __init__(self, text, pos, size, attachpoint): #value provided by the user
        gui_font = pygame.font.Font("font/Pixeltype.ttf", size) #sets the local values of the font being used to render this text
        self.pos = pos #stores the positon value provided by the user
        self.attachpoint = attachpoint #point from which text should render

        self.text_surf = gui_font.render(text, 4, "#1F1F1F") #renders the fond "text = text provided by the user", "4 = antialiasing value", "#1F1F1F = font color"
        if self.attachpoint == "topright": #checks the point from which text should render
            self.text_rect = self.text_surf.get_rect(topright = (self.pos))
        if self.attachpoint == "center":
            self.text_rect = self.text_surf.get_rect(center = (self.pos))
        if self.attachpoint == "topleft":
            self.text_rect = self.text_surf.get_rect(topleft = (self.pos))
    def draw(self):
        screen.blit(self.text_surf, self.text_rect) #renders text on the screen


class Icons(pygame.sprite.Sprite): #render an icon
    def __init__(self, path, pos_x, pox_y, scale_x, scale_y): #value provided by the user
        self.icon_path = path #path of an image
        self.icon_img = pygame.image.load(path).convert_alpha() #loads the image
        self.icon_img = pygame.transform.scale(self.icon_img, (scale_x, scale_y)) #transofrm the image to the values provided 
        self.icon_rect = self.icon_img.get_rect(center=(pos_x, pox_y)) #renders the rectangle (text)

    def draw (self):
        screen.blit(self.icon_img, self.icon_rect) #renders the Icon on the screen


class InfoBox(pygame.sprite.Sprite):   #render the Infomation button that will show a text while being hovered with the mouse
                                       #it uses the functions and logic from previous classes, no extra explanations needed
    def __init__(self, pos_x, pos_y, infotext, textpos, ificon): #values provided by the user
        super().__init__()
        self.infotext = infotext 
        self.ificon = ificon
        self.textpos = textpos
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = pygame.image.load("sprites/info.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (16,16))
        self.image_rect = self.image.get_rect(center=(pos_x, pos_y))
        self.font = pygame.font.Font("font/Pixeltype.ttf", 32)

    def draw(self):
        screen.blit(self.image, self.image_rect)
        self.check_click()
    
    def drawrect(self):
        self.text_surf = self.font.render(self.infotext, 4, "#1F1F1F")
        if self.textpos == "topleft":
            self.text_rect = self.text_surf.get_rect(topleft = (self.pos_x + 40, self.pos_y + 15))
        if self.textpos == "topright":
            self.text_rect = self.text_surf.get_rect(topright = (self.pos_x - 10, self.pos_y))
        screen.blit(self.text_surf, self.text_rect)
        if self.ificon:
            self.icondraw()

    def icondraw(self):
        self.image_intext = pygame.image.load("sprites/gem.png").convert_alpha()
        self.image_intext = pygame.transform.scale(self.image_intext, (32,32))
        self.image_intext_rect = self.image_intext.get_rect(topleft = (self.pos_x + 5, self.pos_y + 5))
        screen.blit(self.image_intext, self.image_intext_rect)


    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.image_rect.collidepoint(mouse_pos):
            self.drawrect()

            
            


animation_group = pygame.sprite.Group() #needed to store more than one coin sprite

button1 = Buttons(150, 150, (game_window_width/2), (game_window_height/2), 8, '#FF6904', "#F3890F") #renders the main click button

button2 = Buttons(100, 100, 100, 100, 5, "#46A146", "#40A9E6") #renders the buy "Click Power" button
button2_2 = Buttons(40, 40, 200, 100, 5, '#46A146', "#40A9E6") #renders the "Buy Max" button for "Click power"


button3 = Buttons(100, 100, (game_window_width - 100), 100, 5, "#7346A1", "#40A9E6") #renders the "Buy worker" button
button3_2 = Buttons(40, 40, (game_window_width - 200), 100, 5, '#7346A1' , "#40A9E6") #renders the "Buy max" button for "Buy Workers" button

button4 = Buttons_image("sprites/coin.png", (400, 300), 64, 64, 5) #not used yet

button5 = Buttons(100, 100, 100, 300, 5, "#46A146", "#40A9E6") #renders the "Buy gem upgrade" button


infoicon1 = InfoBox(170, 280, " =  100x  clickpower", "topleft", True) #renders the info icon for "Buy gem upgrade" button

idle_coins_gain = 1000 # sets the timer for idle coin gain. Counted in miliseconds
coin_timer = pygame.USEREVENT + 1
pygame.time.set_timer(coin_timer,idle_coins_gain)


#-------------GAME:9

active = False #main game state value. Changes to "True" when being played
clock = pygame.time.Clock() #sets tick rate/fps for the game, base value = 60

#----Starting game's values:
coins = 0 
click_power = 1 
click_power_upgrade_cost = 10
auto_clic_power_buyer_cost = 5

idle_gain = 1
idle_gain_upgrade_cost = 50

tool_power = 0
miners_quantity = 1

max_gem_chance = 100
min_gem_chance = 1

gem_chance_cost = 250

tool_gem_chance = 1

idle_coins_gain = 200



def max_buy_coins(x, y): #checks how much you can buy "Click power" upgrades
    max_coins = x
    max_buy_cost = y
    max_buy = 0
    while max_coins >= max_buy_cost:
            max_coins = max_coins - max_buy_cost
            max_buy_cost = (max_buy_cost * 2.5) - 1
            max_buy += 1
    return max_buy
    
def max_buy_workers(x, y): #checks how much you can buy workers at once
    max_coins = x
    max_buy_cost = y
    max_buy = 0
    while max_coins >= max_buy_cost:
            max_coins = max_coins - max_buy_cost
            max_buy_cost = (max_buy_cost * 2.5) - 1
            max_buy += 1
    return max_buy
    









while True: #starts the game

    for event in pygame.event.get(): #stops the game from working when user exits it
        if event.type == pygame.QUIT:
            active = True
            pygame.quit()
            exit()          

        
        if event.type == coin_timer: #adds the coins from idle gain value with every second in the game
            coins += idle_gain



    if not active: #starts the game



        gem_spawn = random.uniform(min_gem_chance, max_gem_chance) #displays gem chance
        tool_gem_chance_overall = (tool_gem_chance  / max_gem_chance) * 100  #calculates the gem chance 

        
        screen.fill("#D7D7D7") #game's background color


        #----------texts 
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

        click_power_max = Text_gui(f"Buy MAX: {max_buy_coins(coins, click_power_upgrade_cost)}", (170, 150), 35, "topleft")
        click_power_max.draw()

        click_tool_text = Text_gui(f"Gem chance: {tool_gem_chance_overall:.2f}%", (10, 420), 35, "topleft")
        click_tool_text.draw()

        cost_upgrade_text = Text_gui(f"Upgrade cost: {gem_chance_cost:.0f}", (10, 445), 35, "topleft")
        cost_upgrade_text.draw()

        #idle_coin_gain text
        idle_coin_gain_text = Text_gui(f"Idle gain:  {idle_gain}/sec", ((game_window_width-10), 30), 35, "topright")
        idle_coin_gain_text.draw()

        idle_power_upgrade_text = Text_gui(f"Upgrade cost: {idle_gain_upgrade_cost:.0f}", ((game_window_width-10), 60), 35, "topright")
        idle_power_upgrade_text.draw()

        click_power_max = Text_gui(f"Buy MAX: {max_buy_workers(coins, idle_gain_upgrade_cost)}", ((game_window_width-170), 150), 35, "topright")
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
            while coins >= idle_gain_upgrade_cost:
                coins = coins - idle_gain_upgrade_cost
                idle_gain += 1
                idle_gain_upgrade_cost = (idle_gain_upgrade_cost * 1.2) - 1
                miners_quantity += 1


        infoicon1.draw() #info icon for Gem upgrade button
    

        pygame.display.update()
        clock.tick(60)
