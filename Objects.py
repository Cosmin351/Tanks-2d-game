import pygame
import numpy as np

Green = (0, 255, 0)
Red = (255, 0, 0)
Blue = (0, 0, 255)
Light_blue = (0, 128, 255)
Purple = (127, 0, 255)
Black = (0, 0, 0)
Grey = (105, 105, 105)
Yellow = (225, 225, 0)
White = (255, 255 ,255)

Tank_colors = [Green, Red, Blue, Yellow, Grey]

class Player:
    def __init__(self, number, Map_points, players):
        self.number = number
        self.Tank = Tank(number, 900, 600, Map_points, players)
        self.money = 1450
        self.kills = 0
        self.win_number = 0
        self.dead = False
        self.players = players

class Tank:

    def __init__(self, number, Width, Height, map_points, nr_players):
        self.health = 10
        self.fuel   = 250
        self.fuel_capacity = 250
        self.number = number
        self.angle = 0
        self.speed = 2
        self.projectile = 1
        self.projectile_dmg = 1
        self.armour = 1
        self.map_points = map_points
        self.Turretx2 = 0
        self.Turrety2 = 0
        self.Tank_Width  = Width / 15
        self.Tank_Height = Height / 15
        Image_raw = pygame.image.load("assets/tank" + str(number%2) + ".png")
        self.Image = pygame.transform.scale(Image_raw, (self.Tank_Width, self.Tank_Height))
        self.posx = int(np.linspace(30, 830, nr_players)[number - 1])
        self.posy = map_points[self.posx + int(self.Tank_Width/2), 1] - self.Tank_Height
        self.Turetx = self.posx + self.Tank_Width / 2
        self.Turety = self.posy + self.Tank_Height / 5
        self.initialposx = self.posx
        self.initalposy = self.posy

    def reset(self):
        self.fuel = self.fuel_capacity
        self.health = 100
        self.Turretx2 = 0
        self.Turrety2 = 0
        self.angle = 0
        self.posx = self.initialposx
        self.posy = self.initalposy
        self.Turetx = self.posx + self.Tank_Width / 2
        self.Turety = self.posy + self.Tank_Height / 5

    def move(self, dir):
        if self.fuel > 0:
            self.fuel -= 1
        if self.fuel > 0:
            if dir == 0:
                self.posx -= 1
            elif dir == 1:
                self.posx += 1
            self.posy = self.map_points[self.posx + int(self.Tank_Width/2), 1] - self.Tank_Height
            self.Turetx = self.posx + self.Tank_Width / 2
            self.Turety = self.posy + self.Tank_Height / 5
    
    def turretmove(self, dir):
        if dir == 1 and self.angle <= 180:
            self.angle += 1
        elif self.angle > 0:
            self.angle -= 1

    def draw(self, Screen):
        self.Turrety2 = self.Turety - np.sin(self.angle * (np.pi / 180)) * 45
        self.Turretx2 = self.Turetx + np.cos(self.angle * (np.pi / 180)) * 45
        pygame.draw.line(Screen, Tank_colors[self.number - 1], [self.Turetx, self.Turety], [self.Turretx2, self.Turrety2], 4)
        Screen.blit(self.Image, (self.posx, self.posy))

class Projectile:
    def __init__(self, direction, power, angle, posx, posy, player):
        self.direction = direction
        self.power  = power / 12.5
        if angle == 0:
            self.angle  = 1
        else:
            self.angle = angle
        self.posx   = posx
        self.player = player
        self.Height = 600
        self.Width  = 900
        self.posy   = posy
        self.speed  = 0.25
        self.vel    = 0.05

    def move(self):
        self.posx += self.power * np.cos(self.angle * (np.pi / 180))
        self.posy -= (self.power *  np.sin(self.angle * (np.pi / 180)))/1.5 + self.speed
        self.speed -= self.vel

    def draw(self, Screen):
        pygame.draw.circle(Screen, Black, [self.posx, self.posy], 4, 0)
        self.move()

class Hud:
    def __init__(self):
        self.posx   = 0
        self.posy   = 0
        self.width  = 900
        self.height = 65
        self.sheight = 600
        self.font = pygame.font.Font('freesansbold.ttf', 14)

    def draw(self, Screen, TPRS, T1h, T1f, T1a, Turn):
        pygame.draw.rect(Screen, Grey, [self.posx, self.posy, self.width, self.height], 0, 1)

        #Health bar t1
        Health_text = self.font.render("Health", True, Black)
        Screen.blit(Health_text, (3 * self.width / 100, 0.9 * self.sheight / 100))
        pygame.draw.rect(Screen, Red,  [3 * self.width / 100, 3 * self.sheight / 100, 100, 10], 0, 15)
        pygame.draw.rect(Screen, Green,  [3 * self.width / 100, 3 * self.sheight / 100, T1h, 10], 0, 15)

        #Power bar universal
        Power_txt = self.font.render("Power", True, Black)
        Screen.blit(Power_txt, ((50 * self.width / 100), 2.5 * self.sheight / 100 ))
        pygame.draw.rect(Screen, White,  [(50 * self.width / 100) - 25, 5 * self.sheight / 100, 100, 10], 0, 15)
        pygame.draw.rect(Screen, Yellow,  [(50 * self.width / 100) - 25, 5 * self.sheight / 100, TPRS, 10], 0, 15)

        #Text fuel t1 & t2
        Fuel_t1 = self.font.render("Fuel: " + str(T1f), True, Black)
        Screen.blit(Fuel_t1, (3 * self.width / 100, 5 * self.sheight / 100))
        #Text angle t1 & t2
        Angle_t1 = self.font.render("Angle: " + str(T1a), True, Black)
        Screen.blit(Angle_t1, (3 * self.width / 100, 8 * self.sheight / 100))
        
        Player_turn = self.font.render("Player " + str(Turn) +" turn", True, Black)
        Screen.blit(Player_turn ,((49 * self.width / 100) - 10, 8 * self.sheight / 100))

class Button:
    def __init__(self, posx, posy, text, size, number = -1, blocked = -1):
        self.Text = Text(posx, posy, text, size)
        self.number = number
        self.blocked = blocked
    
    def check_interaction(self, mouse_pos):
        if self.Text.posx - 35 < mouse_pos[0] < self.Text.posx - 35 + 8 * self.Text.size and self.Text.posy - self.Text.size/3 < mouse_pos[1] < self.Text.posy - self.Text.size/3 + 3.5 * self.Text.size/2:
            return 1
        else:
            return 0
        
    def draw(self, Screen, mouse_pos):
        if self.check_interaction(mouse_pos) and self.blocked == -1:
            pygame.draw.rect(Screen, Light_blue, [self.Text.posx - self.Text.size * (len(self.Text.text)/ 5), self.Text.posy - self.Text.size/3, self.Text.size * (len(self.Text.text) / 1.085) , 3.5 * self.Text.size/2], 0, 15)
        elif self.blocked == -1:
            pygame.draw.rect(Screen, Blue, [self.Text.posx - self.Text.size * (len(self.Text.text)/ 5), self.Text.posy - self.Text.size/3, self.Text.size * (len(self.Text.text) / 1.085) , 3.5 * self.Text.size/2], 0, 15)
        elif self.blocked == 1:
            pygame.draw.rect(Screen, Red, [self.Text.posx - self.Text.size * (len(self.Text.text)/ 5), self.Text.posy - self.Text.size/3, self.Text.size * (len(self.Text.text) / 1.085) , 3.5 * self.Text.size/2], 0, 15)
        elif self.blocked == 2:
            pygame.draw.rect(Screen, Yellow, [self.Text.posx - self.Text.size * (len(self.Text.text)/ 5), self.Text.posy - self.Text.size/3, self.Text.size * (len(self.Text.text) / 1.085) , 3.5 * self.Text.size/2], 0, 15)
        pygame.draw.rect(Screen, Purple,  [self.Text.posx - self.Text.size * (len(self.Text.text)/ 5), self.Text.posy - self.Text.size/3, self.Text.size * (len(self.Text.text) / 1.085), 3.5 * self.Text.size/2], 4, 15)
        self.Text.draw(Screen)

class Text:
    def __init__(self, posx, posy, text, size, number = -1):
        self.number = number
        self.size = size
        self.posx  = posx
        self.posy  = posy
        self.text = text
        self.font = pygame.font.Font('freesansbold.ttf', size)
        self.text_display = self.font.render(text, True, Black)

    def change_text(self, new_text):
        self.text = new_text
        self.text_display = self.font.render(new_text, True, Black)

    def draw(self, Screen):
        Screen.blit(self.text_display, (self.posx, self.posy))