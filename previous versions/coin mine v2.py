from pickle import FALSE
import pygame


#-------------SETTINGS:

    

#-----
pygame.init()
screen = pygame.display.set_mode((800,400)) 
pygame.display.set_caption("Coin mine") 
font = pygame.font.Font("font/Pixeltype.ttf", 35)
coin_font = pygame.font.Font("font/Pixeltype.ttf", 50)


#-------------GAME:9

def Game():
    clock = pygame.time.Clock()

    coins = 0
    multipler = 1
    upgrade_cost = 50
    upgrade_cost_idle = 10

    idle_gain = 1

    button_coins = pygame.Rect(350, 100, 100, 100)
    button_upgrade_click = pygame.Rect(50, 100, 100, 100)
    button_upgrade_coin = pygame.Rect(650, 100, 100, 100)

    gain_coins = 1000
    coin_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(coin_timer,gain_coins)

    coin_img = pygame.image.load('sprites/coin.png').convert_alpha()
    coin_img_rect = coin_img.get_rect(midright=(320,20))
    coin_img = pygame.transform.scale(coin_img, (32, 32))

        


    active = False
    while not active:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = True

            if event.type == coin_timer:
                coins += idle_gain


            #-------Coin button---------

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == True:
                    if button_coins.collidepoint(event.pos):
                        button_coins.y += 3
                        coins += multipler
            
            if event.type == pygame.MOUSEBUTTONUP:
                if button_coins.collidepoint(event.pos):
                    button_coins.y -= 3

            #-------Click power button---------

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == True:
                    if button_upgrade_click.collidepoint(event.pos):
                        button_upgrade_click.y += 3
                        if coins >= upgrade_cost:
                            coins = coins - upgrade_cost
                            upgrade_cost = upgrade_cost + 10

            if event.type == pygame.MOUSEBUTTONUP:
                if button_upgrade_click.collidepoint(event.pos):
                    button_upgrade_click.y -= 3

            #-------Idle power button---------

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == True:
                    if button_upgrade_coin.collidepoint(event.pos):
                        button_upgrade_coin.y += 3
                        if coins >= upgrade_cost_idle:
                            coins = coins - upgrade_cost_idle
                            upgrade_cost_idle = upgrade_cost_idle + 50
                            idle_gain = idle_gain + 1



            if event.type == pygame.MOUSEBUTTONUP:
                if button_upgrade_coin.collidepoint(event.pos):
                    button_upgrade_coin.y -= 3


        #-------Graphics---------                
        screen.fill("lightblue")



        pygame.draw.rect(screen, "purple", button_coins)
        pygame.draw.rect(screen, "BLUE", button_upgrade_click)
        pygame.draw.rect(screen, "RED", button_upgrade_coin)


        screen.blit(coin_img, coin_img_rect)

        score_surf = coin_font.render(f'Coins: {coins}', False, "BLACK")
        score_rect = score_surf.get_rect(midleft=(340, 32))
        screen.blit(score_surf, score_rect)

       

        upgrade_surf = font.render(f'Click power: +{multipler}', False, "BLACK")
        upgrade_rect = upgrade_surf.get_rect(midleft=(10,70))
        screen.blit(upgrade_surf, upgrade_rect)

        


        upgrade_cost_surf = font.render(f'Upgrade cost: {upgrade_cost}', False, "BLACK")
        upgrade_cost__rect = upgrade_cost_surf.get_rect(midleft=(10, 230))
        screen.blit(upgrade_cost_surf, upgrade_cost__rect)

        upgrade_surf = font.render(f'Idle power: {idle_gain}/sec', False, "BLACK")
        upgrade_rect = upgrade_surf.get_rect(midright=(780, 70))
        screen.blit(upgrade_surf, upgrade_rect)

        upgrade_cost_idle_surf = font.render(f'Upgrade cost: {upgrade_cost_idle}', False, "BLACK")
        upgrade_cost_idle__rect = upgrade_cost_idle_surf.get_rect(midright=(780, 230))
        screen.blit(upgrade_cost_idle_surf, upgrade_cost_idle__rect)




        pygame.display.update()
        clock.tick(30)

Game()
pygame.quit()