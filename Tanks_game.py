import pygame
import pygame.gfxdraw
from pygame import mixer
import numpy as np
from numpy import random as rnd
import Objects

Green = (0, 255, 0)
Red = (255, 0, 0)
Grey = (105, 105, 105)
White = (255, 255, 255)

pygame.init()
pygame.font.init()
mixer.init()

# Screen
Width =  900
Height = 600
Screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption('Tanks')

# Imgs load and scale
Dirt_texture = pygame.image.load("assets/dirt.jpg")
Dirt_texture = pygame.transform.scale(Dirt_texture, (Width, 360))

Background_IMG = pygame.image.load("assets/sky.jpg")
Background = pygame.transform.scale(Background_IMG, (Width, Height))

Main_Background_IMG = pygame.image.load("assets/main_background.jpg")
Main_Background = pygame.transform.scale(Main_Background_IMG, (Width, Height))

def GenerateMap():
    Points_number = rnd.randint(20, 30)
    Map_points = np.hstack((np.reshape(np.linspace(0, Width, Points_number), [Points_number, 1]), rnd.randint(Height/2, Height/2 + Height/30, [Points_number, 1])))
    Map_points[0][1] = Height/2 + Height/16
    Map_points[Points_number - 1][1] = Height/2 + Height/16

    for i in range(1, Points_number):
        Lenght_Dif = int(Map_points[i, 0] - Map_points[i-1, 0])
        Height_Dif = (Map_points[i, 1] - Map_points[i-1, 1]) / Lenght_Dif
        if i == 1:
            if not Height_Dif:
                Map_line_pointsX = np.hstack((np.reshape(np.linspace(Map_points[i - 1, 0], Map_points[i, 0], Lenght_Dif), [Lenght_Dif, 1]), np.reshape(np.ones(Lenght_Dif) * Map_points[i, 1], [Lenght_Dif, 1])))
            else:
                Map_line_pointsX = np.hstack((np.reshape(np.linspace(Map_points[i - 1, 0], Map_points[i, 0], Lenght_Dif), [Lenght_Dif, 1]), np.reshape(np.flip(np.linspace(Map_points[i, 1], Map_points[i - 1, 1], Lenght_Dif)), [Lenght_Dif, 1])))
        else:
            if not Height_Dif:
                Map_line_pointsX = np.vstack((Map_line_pointsX, np.hstack((np.reshape(np.linspace(Map_points[i - 1, 0], Map_points[i, 0], Lenght_Dif), [Lenght_Dif, 1]), np.reshape(np.ones(Lenght_Dif) * Map_points[i, 1], [Lenght_Dif, 1])))))
            else:
                Map_line_pointsX = np.vstack((Map_line_pointsX, np.hstack((np.reshape(np.linspace(Map_points[i - 1, 0], Map_points[i, 0], Lenght_Dif), [Lenght_Dif, 1]), np.reshape(np.flip(np.linspace(Map_points[i, 1], Map_points[i - 1, 1], Lenght_Dif)), [Lenght_Dif, 1])))))
    Map_line_pointsX = np.floor(Map_line_pointsX)
    Map_line_pointsX = np.vstack((np.vstack((np.array(([-1, 600], [-2, 300])), Map_line_pointsX)), np.array([901, 600])))
    return Map_line_pointsX

def GenerateObjects():
    global Buttons_main, Main_Title, Texts_shop, Players, Hud, Button_controls_exit, Texts_controls, Buttons_shop, Text_shop1, Text_shop2, Text_shop3, Loading_text

    Buttons_main = []
    Buttons_shop = []
    Texts_controls = []
    Texts_shop = []
    Temp_val = 35

    for i in range(4):
        Buttons_main.append(Objects.Button(43 * Width/100, Temp_val * Height / 100, str(i + 2) + " Players", 20, i + 2))
        Temp_val += 10
    Buttons_main.append(Objects.Button(43 * Width/100, Temp_val * Height / 100, "Controls", 20, -2))
    Buttons_main.append(Objects.Button(43 * Width/100, (Temp_val + 10) * Height / 100, "Exit", 20))
    Main_Title = Objects.Text(41.5 * Width/100, 15 * Height/100, "Tanks", 40)
    
    Temp_val = 35

    Texts_controls.append(Objects.Text(33 * Width/100, Temp_val * Height / 100, "A - Move left || Move right - D", 20))
    Texts_controls.append(Objects.Text(29 * Width/100, (Temp_val + 10) * Height / 100, "W - Turret to right || Turret to left - S", 20))
    Texts_controls.append(Objects.Text(20 * Width/100, (Temp_val + 20) * Height / 100, "Hold Space - Increase shot power || Shoot - Unhold space", 20))
    Button_controls_exit = Objects.Button(43 * Width/100, (Temp_val + 35) * Height / 100, "    Exit", 20)

    Buttons_shop.append(Objects.Button(43 * Width/100, (Temp_val + 45) * Height / 100, "Continue", 20, -2))
    Buttons_shop.append(Objects.Button(43 * Width/100, (Temp_val + 55) * Height / 100, "Exit", 20, -3))
    Buttons_shop.append(Objects.Button(10 * Width/100, Temp_val * Height / 100, "Bullet damage", 20, 1, 1))
    Buttons_shop.append(Objects.Button(6 * Width/100, (Temp_val + 10) * Height / 100, "Armour", 20, 2, 1))
    Buttons_shop.append(Objects.Button(7 * Width/100, (Temp_val + 20) * Height / 100, "Projectile type", 20, 4, 1))
    Buttons_shop.append(Objects.Button(10 * Width/100, (Temp_val + 30) * Height / 100, "Fuel tank", 20, 3, 1))
    Texts_shop.append(Objects.Text(42 * Width/100, 5 * Height/100, "Shop", 35))
    Texts_shop.append(Objects.Text(30 * Width/100, 15 * Height/100, "Player " + " " + "won the round." , 30, 5))
    Texts_shop.append(Objects.Text(38 * Width/100, 25 * Height/100, "Money: " , 30, 6))
    Texts_shop.append(Objects.Text(80 * Width/100, (Temp_val) * Height / 100, "Rounds won: ", 20, 1))
    Texts_shop.append(Objects.Text(80 * Width/100, (Temp_val + 10) * Height / 100, "Kills: ", 20, 2))
    
    Loading_text = Objects.Text(41.5 * Width/100, 45 * Height/100, "Loading...", 40)

    Hud = Objects.Hud()

def GeneratePlayers(number):
    global Players
    Players = []    
    for i in range(number):
        Players.append(Objects.Player(i + 1, Map_line_points, number))

def CheckAlive():
    global Players, Last_player
    Alive = 0
    for Player in Players:
        if Player.dead == False:
            Alive += 1
            Last_player = Player.number
    if Alive == 0:
        return 0
    elif Alive == 1:
        return Last_player
    else:
        return -1

def remake():
    global Players, Player_turn, Map_line_points
    Map_line_points = GenerateMap()
    for Player in Players:
        Player.dead = False
        Player.Tank.map_points = Map_line_points
        Player.Tank.reset()
        Player_turn = 1

def update():
    global Players, Map_line_points
    for Player in Players:
        Player.Tank.map_points = Map_line_points
        Player.Tank.move(-1)

def sounds_init():
    global Fire_sound, Hit_sound, Move_sound
    Fire_sound = mixer.Sound('assets/Fire.mp3')
    Hit_sound = mixer.Sound('assets/Hit.mp3')
    Move_sound = mixer.Sound('assets/Move.mp3')

    Fire_sound.set_volume(0.5)
    Hit_sound.set_volume(0.5)
    Move_sound.set_volume(0.25)

Map_line_points = GenerateMap()
GenerateObjects()
sounds_init()

# Var init
Player_turn = 1
RePlayer_turn = Player_turn
Last_player = -1
Projectiles = []
Time_pressed = 0
start_ticks_move = 0

Clock = pygame.time.Clock()

# Bools
Playing = False
Exit = False
Shoot = False
Main = True
Controls = False
Exit = False
Started = False
Shop = False
Loading = False

while not Exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Exit = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE and not Shoot and Started:
                Shoot = True
                Fire_sound.play()
                Projectiles.append(Objects.Projectile(1, Time_pressed, Players[Player_turn - 1].Tank.angle, Players[Player_turn - 1].Tank.Turretx2, Players[Player_turn - 1].Tank.Turrety2, Player_turn))
            if event.key == pygame.K_a or event.key == pygame.K_d and Started:
                Move_sound.stop()
                Playing = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not Shoot and Started:
                Time_pressed = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            if Main:
                for button in Buttons_main:
                    if button.check_interaction(pygame.mouse.get_pos()) and button.number != -1 and button.number != -2:
                        Players_number = button.number
                        GeneratePlayers(Players_number)
                        Main = False
                        Started = True
                    elif button.check_interaction(pygame.mouse.get_pos()) and button.number == -2:
                        Main = False
                        Controls = True
                    elif button.check_interaction(pygame.mouse.get_pos()) and button.number == -1:
                        Main = False
                        Exit = True
            if Controls:
                if Button_controls_exit.check_interaction(pygame.mouse.get_pos()):
                    Main = True
                    Controls = False
            if Shop:
                for button in Buttons_shop:
                    if button.check_interaction(pygame.mouse.get_pos()) and button.number == -2:
                        Started = True
                        Shop = False
                    elif button.check_interaction(pygame.mouse.get_pos()) and button.number == -3:
                        Exit = True
                        Shop = False
                    elif button.check_interaction(pygame.mouse.get_pos()) and button.number == 1 and button.blocked == -1 and Players[Last_player - 1].Tank.projectile_dmg < 5:
                        Players[Last_player - 1].Tank.projectile_dmg +=1 
                        Players[Last_player - 1].money -= (Players[Last_player - 1].Tank.projectile_dmg - 1) * 100
                    elif button.check_interaction(pygame.mouse.get_pos()) and button.number == 2 and button.blocked == -1 and Players[Last_player - 1].Tank.armour < 5:
                        Players[Last_player - 1].Tank.armour +=1 
                        Players[Last_player - 1].money -= (Players[Last_player - 1].Tank.armour - 1) * 100
                    elif button.check_interaction(pygame.mouse.get_pos()) and button.number == 3 and button.blocked == -1 and Players[Last_player - 1].Tank.fuel_capacity < 500:
                        Players[Last_player - 1].Tank.fuel_capacity += 50
                        Players[Last_player - 1].money -= ((Players[Last_player - 1].Tank.fuel_capacity - 250)/50) * 100
                    elif button.check_interaction(pygame.mouse.get_pos()) and button.number == 4 and button.blocked == -1 and Players[Last_player - 1].Tank.projectile < 3:
                        Players[Last_player - 1].Tank.projectile += 1
                        Players[Last_player - 1].money -= (Players[Last_player - 1].Tank.projectile - 1) * 200

    if Started:
        keys = pygame.key.get_pressed()
        if not Shoot:
            if keys[pygame.K_a]:
                    if not Playing and Players[Player_turn - 1].Tank.fuel > 0:
                        Playing = True
                        Move_sound.play(999)
                    elif Playing and Players[Player_turn - 1].Tank.fuel <= 0:
                        Playing = False
                        Move_sound.stop()
                    if Players[Player_turn - 1].Tank.posx >= 0:
                        Players[Player_turn - 1].Tank.move(0)
            if keys[pygame.K_d]:
                    if not Playing and Players[Player_turn - 1].Tank.fuel > 0:
                        Playing = True
                        Move_sound.play()
                    elif Playing and Players[Player_turn - 1].Tank.fuel <= 0:
                        Playing = False
                        Move_sound.stop() 
                    if Players[Player_turn - 1].Tank.posx + Players[Player_turn - 1].Tank.Tank_Width <= Width:
                        Players[Player_turn - 1].Tank.move(1)
            if keys[pygame.K_w]:
                    Players[Player_turn - 1].Tank.turretmove(1)
            if keys[pygame.K_s]:
                    Players[Player_turn - 1].Tank.turretmove(0)
            if keys[pygame.K_SPACE]:
                if Time_pressed < 99.5:
                    Time_pressed += 1.25
        Screen.blit(Background, (0, 0))
        pygame.gfxdraw.textured_polygon(Screen, Map_line_points, Dirt_texture, 0, 0)
        for Player in Players:
            if not Player.dead:
                Player.Tank.draw(Screen)
        if Projectiles:
            for Projectile in Projectiles:
                Projectile.draw(Screen)
                # Verifica daca iese din fundal
                if Projectile.posx > 900 or Projectile.posx < 0:
                    Projectiles.remove(Projectile)
                    start_ticks=pygame.time.get_ticks()
                    break
                Search = Map_line_points[np.where(Map_line_points[:, 0] == int(Projectile.posx))[0], 1]
                if np.size(Search) > 1:
                    Search = int(Search[0])
                # Verifica daca loveste pamantul
                if Search < Projectile.posy:
                    for Player in Players:
                        if abs(Player.Tank.posy - Projectile.posy) + abs(Player.Tank.posx - Projectile.posx) < 60 and not Player.dead:
                            Player.Tank.health -= 3 * ((Players[RePlayer_turn - 1].Tank.projectile * Players[RePlayer_turn - 1].Tank.projectile_dmg) / Player.Tank.armour) * (10 - ((abs(Player.Tank.posy - Projectile.posy) + abs(Player.Tank.posx - Projectile.posx)) / 10))
                    try:
                        Map_line_points[int(Projectile.posx) - 40:int(Projectile.posx) + 40, 1] += (30 * np.sin(np.linspace(0, np.pi, 80)))
                    except:
                        print("exception")

                    Projectiles.remove(Projectile)
                    start_ticks=pygame.time.get_ticks()
                for Player in Players:
                    if Player.Tank.posx < Projectile.posx < Player.Tank.posx + Player.Tank.Tank_Width and Player.Tank.posy < Projectile.posy < Player.Tank.posy + Player.Tank.Tank_Height and not Player.dead:
                        Player.Tank.health -= 30 * ((Players[RePlayer_turn - 1].Tank.projectile * Players[RePlayer_turn - 1].Tank.projectile_dmg) / Player.Tank.armour)
                        Projectiles.remove(Projectile)
                        Hit_sound.play()
                        start_ticks=pygame.time.get_ticks()
                for Player in Players:
                    if Player.Tank.health <= 0 and not Player.dead:
                        Player.dead = True
                        Players[RePlayer_turn - 1].money += 250
                        Players[RePlayer_turn - 1].kills += 1
        Hud.draw(Screen, Time_pressed, Players[Player_turn - 1].Tank.health, Players[Player_turn - 1].Tank.fuel, Players[Player_turn - 1].Tank.angle, Player_turn)
        if not Projectiles and Shoot:
            seconds=(pygame.time.get_ticks() - start_ticks)/1000
            if seconds > 1.5:
                Shoot = False
                Not_dead = True
                RePlayer_turn = Player_turn
                while Not_dead:
                    if Player_turn < Players_number:
                        Player_turn += 1
                    else:
                        Player_turn = 1
                    if Players[Player_turn - 1].dead == False:
                        Not_dead = False
            answer = CheckAlive()
            if answer != -1 and answer != 0:
                remake()
                Started = False
                Shop = True
                Players[Last_player - 1].win_number += 1
                for Text in Texts_shop:
                    if Text.number == 5:
                        Text.change_text("Player " + str(Last_player) + " won the round.")
            elif answer == 0:
                Loading = True
                Started = False
                remake()
                start_ticks2 = pygame.time.get_ticks()
    if Main:
        Screen.blit(Main_Background, (0, 0))
        for Button in Buttons_main:
            Button.draw(Screen, pygame.mouse.get_pos())
        Main_Title.draw(Screen)
    if Controls:
        Screen.fill(Grey)
        for Text in Texts_controls:
            Text.draw(Screen)
        Button_controls_exit.draw(Screen, pygame.mouse.get_pos())
    if Shop:
        for Text in Texts_shop:
            if Text.number == 6:
                Text.change_text("Money: " + str(Players[Last_player - 1].money))
        for button in Buttons_shop:
            if button.number > 0:
                if button.number == 1:
                    button.Text.change_text("Bullet damage: " + str(Players[Last_player - 1].Tank.projectile_dmg))
                elif button.number == 2:
                    button.Text.change_text("Amour: " + str(Players[Last_player - 1].Tank.armour))
                elif button.number == 3:
                    button.Text.change_text("Fuel capacity: " + str(Players[Last_player- 1].Tank.fuel_capacity))
                elif button.number == 4:
                    button.Text.change_text("Projectile: " + str(Players[Last_player- 1].Tank.projectile))
                if button.number == 1:
                    if Players[Last_player - 1].money < (Players[Last_player - 1].Tank.projectile_dmg) * 100 and Players[Last_player - 1].Tank.projectile_dmg < 5:
                        button.blocked = 1
                    elif Players[Last_player - 1].Tank.projectile_dmg == 5:
                        button.blocked = 2
                    else:
                        button.blocked = -1
                if button.number == 2:
                    if Players[Last_player - 1].money < ((Players[Last_player - 1].Tank.armour) * 100) and Players[Last_player - 1].Tank.armour < 5:
                        button.blocked = 1
                    elif Players[Last_player - 1].Tank.armour == 5:
                        button.blocked = 2
                    else:
                        button.blocked = -1
                if button.number == 3:
                    if Players[Last_player - 1].money < ((Players[Last_player - 1].Tank.fuel_capacity - 200)/50) * 100 and Players[Last_player - 1].Tank.fuel_capacity < 500:
                        button.blocked = 1
                    elif Players[Last_player - 1].Tank.fuel_capacity == 500:
                        button.blocked = 2
                    else:
                        button.blocked = -1
                if button.number == 4:
                    if Players[Last_player - 1].money < (Players[Last_player - 1].Tank.projectile) * 200 and Players[Last_player - 1].Tank.projectile < 5:
                        button.blocked = 1
                    elif Players[Last_player - 1].Tank.projectile == 5:
                        button.blocked = 2
                    else:
                        button.blocked = -1

        Screen.fill(Grey)
        for button in Buttons_shop:
            button.draw(Screen, pygame.mouse.get_pos())
        for Text in Texts_shop:
            if Text.number == 1:
                Text.change_text("Rounds won: " + str(Players[Last_player - 1].win_number))
            elif Text.number == 2:
                Text.change_text("Kills: " + str(Players[Last_player - 1].kills))
            Text.draw(Screen)
    if Loading:
        Screen.fill(White)
        Loading_text.draw(Screen)
        if (pygame.time.get_ticks() - start_ticks2) / 1000 > 2:
            Loading = False
            Started = True
    #Screen update
    pygame.display.update()
    #Fps
    Clock.tick(60)

pygame.quit()