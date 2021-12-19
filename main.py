# HAPPY SAILS 
# PROJECT BY BOROZDNA M D 2021 БИБ213

import pygame
import math
import time
from related_functions import blit_rotate_center, angle_between_two_vectors, angle_by_sin_cos
from data import sail_force_by_angle # Словарь с эксперементальными данными для разныых углов атаки паруса
from textures import WATER, WIND_ARROW, BOAT_0, BOAT_LEFT_5, BOAT_LEFT_15, BOAT_LEFT_30, BOAT_LEFT_45, BOAT_LEFT_60, BOAT_LEFT_75, BOAT_LEFT_90, BOAT_RIGHT_5, BOAT_RIGHT_15, BOAT_RIGHT_30, BOAT_RIGHT_45, BOAT_RIGHT_60, BOAT_RIGHT_75, BOAT_RIGHT_90

WIDTH, HEIGHT = WATER.get_width(), WATER.get_height()
if __name__ == '__main__':
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    """Экран по размеру фона (WATER)."""
pygame.display.set_caption("GO SAILING!") #заголовок окна

#WIND_SPEED = 5 # скорость ветра в метрах в секунду
WIND_ANGLE = 0 # Угол, под которым дует ветер.
MAX_FORCE = 150 # Ньютонов. К сожалению, не нашёл подходящей научной базы, так что значение подставляются наугад.
# Используется для расчета коэф. трения 
WIND_COEFFICIENT = MAX_FORCE / 1.2  # подобрал подходящие коэффициенты

FPS = 60

class Boat:
    '''
    Класс Boat используется для создания лодки.

    Attributes
    ----------
    length : длина ватерлинии в метрах
    mass : cнаряженная масса в кг
    rotation_speed : коэффициент скорости поворота румпелем. Подбирается методом тыка
    course : угол направления лодки относительно экрана в градусах [0, 360)
    texture : изображение лодки
    start_position : начальное положение лодки
    max_speed : вычисляется максимальная скорость лодки в водоизмещающем режиме м/с = 1.707*1.34/3.6*(длина в футах)^1/2
    friction_coefficient : коэффициент сопротивления воды
    x, y : координаты начального положения лодки (верхний левый угол)
    speed : скорость лодки
    mainsheet : угол отклонения паруса отнсительно лодки [0-90]

    Methods
    -------
    __init__(self, length, mass, rotation_speed, course = 90, texture = BOAT_0, start_position = (WIDTH/2, HEIGHT/2)) : 
    
        Длина, масса, скорость поворота задаются при создании объекта.\n
        Начальный курс (0), картинка лодки(BOAT_0), её позиция(WIDTH/2, HEIGHT/2),\n\t скорость(0), положение паруса(0) по умолчанию заданы.\n
        Максимальная скорость, коэффициент сопротивления воды вычисляются на основании входных данных.

    rudder_operate(self, speed, left = False, right = False)
        Метод осуществляет поворот руля. Изменяет значение self.course, учитывая направление поворота и скорость.
    
    mainsheet_operate(self, tighten = False, loosen = False)
        Метод осуществялет управлением гика шкотом. Принимает значение выбрать или травить. 
        Изменяет угол паруса относительно лодки(self.mainsheet).
    
    sail_angle_to_wind(self)
        Метод возвращает значение угла атаки паруса(относительно ветра) в градусах [0, 180]

    sail_force_longitudinal(self)
        Возвращает продольную составляющую силы относительно корпуса, действующую на парус.
        Дрейф не учитывается, и перпендикулярная компонента не используется.

    acceleration(self, sail_force_longtitudinal)
        Возвращает ускорение, основываясь на силах, действующих на лодку, по 2 зну Ньютона. a = F/m
    
    move(self)
        Метод перемещает лодку, основываясь на положении, курсе, скорости и ускорении.
        В случае выхода за границы экрана смещает к противоположному краю.
        
    draw(self, win)
        Метод отрисовывает лодку с парусом, в зависимости от его положения, положения и курса лодки.

    
    
    '''
    def __init__(self, length, mass, rotation_speed, course = 90, texture = BOAT_0, start_position = (WIDTH/2, HEIGHT/2)):
        self.texture = texture 
        self.length = length
        self.mass = mass
        self.max_speed = 1.71 / 3.6 * 1.34 * math.sqrt(3.281 * length) 
        self.friction_coefficient = MAX_FORCE/(self.max_speed**2) 
        self.x, self.y = start_position
        self.speed = 0
        self.rotation_speed = rotation_speed
        self.course = course
        self.mainsheet = 0

    def rudder_operate(self, speed, left = False, right = False):
        '''
        Метод осуществляет поворот руля. Изменяет значение self.course, учитывая направление поворота и скорость.

            Parameters
            ----------
            speed : скорость лодки
            left : bool, поворот влево
            right : bool, поворот вправо
        '''
        if left:
            self.course += self.rotation_speed * speed
        elif right:
            self.course -= self.rotation_speed * speed
        
        if self.course < 0: # проверка, что курс остается в интерале [0; 2*Pi]
            self.course += 360
        if self.course >= 360:
            self.course -= 360
    
    def mainsheet_operate(self, tighten = False, loosen = False):
        '''
        Метод осуществялет управлением гика шкотом. Принимает значение выбрать или травить. 
        Изменяет угол паруса относительно лодки(self.mainsheet).
        
        Parameters
        ----------
        tighten : bool, выбрать
        loosen : bool, травить
        '''
        if tighten and (self.mainsheet > 0):
            self.mainsheet -= 1
        elif loosen and (self.mainsheet < 90):
            self.mainsheet += 1

    def sail_angle_to_wind(self):
        """
        Метод возвращает значение угла атаки паруса(относительно ветра).

        Returns
        -------
        Угол атаки паруса в градусах [0, 180].
        """
        if self.course <= 180:
            sail_angle = self.course - self.mainsheet
        elif self.course <= 270:
            sail_angle = self.course + self.mainsheet
        else:
            sail_angle = 360 - self.course - self.mainsheet
        return angle_between_two_vectors(sail_angle, WIND_ANGLE)
        
    def sail_force_longitudinal(self):
        """
        Возвращает продольную составляющую силы относительно корпуса, действующую на парус.
        Дрейф не учитывается, и перпендикулярная компонента не используется.

        Returns
        -------
        Значение силы, относительно оси движения лодки. Если сила направлена вперёд, то с +, иначе с -.
        """
        (force_x, force_y) = sail_force_by_angle[self.sail_angle_to_wind() // 5 * 5] # Берет из словаря значения для подъёмной и толкающей составляющих силы, действующей на парус
        if self.course < 180: # При движении вверх значения по y будут обратными
            force_y = -force_y
        force_x = -force_x

        force_x *= WIND_COEFFICIENT
        force_y *= WIND_COEFFICIENT

        len_force = math.sqrt(force_x**2 + force_y**2)

        angle_force_to_wind = angle_by_sin_cos(-force_y/len_force, force_x/len_force)

        return math.cos(math.radians(angle_between_two_vectors(angle_force_to_wind, self.course)))*len_force

    def acceleration(self, sail_force_longtitudinal):
        '''
        Возвращает ускорение, основываясь на силах, действующих на лодку, по 2 зну Ньютона. a = F/m
        
        Parameters
        ----------
        sail_force_longtitudinal : продольная составляющая силы относительно корпуса

        Returns
        -------
        Ускорение в м/с^2
        '''
        print(sail_force_longtitudinal)
        friction_force = self.friction_coefficient * (self.speed**2) # сила споротевления воды прямо пропорциональна квадрату скорости
        if self.speed >= 0:
            result_force = sail_force_longtitudinal - friction_force
        else:
            result_force = sail_force_longtitudinal + friction_force
        
        return result_force/self.mass 

    def move(self):
        """
        Метод перемещает лодку, основываясь на положении, курсе, скорости и ускорении.
        В случае выхода за границы экрана смещает к противоположному краю.
        """
        self.speed += self.acceleration(self.sail_force_longitudinal())/60 # Скорость изменяется под воздействием ускорения

        self.x += math.cos(math.radians(self.course)) * self.speed # Координаты меняются в соответствии со скоростью
        self.y -= math.sin(math.radians(self.course)) * self.speed

        if self.x < 0:
            self.x += WIDTH
        if self.x > WIDTH:
            self.x -= WIDTH
        if self.y < 0:
            self.y += HEIGHT
        if self.y > HEIGHT:
            self.y -= HEIGHT

    def draw(self, win):
        """ 
        Метод отрисовывает лодку с парусом, в зависимости от его положения, положения и курса лодки.
        """
        
        angle = self.sail_angle_to_wind()
        
        if ((angle < 1) and ((self.course < 1) or (self.course > 359))) or ((angle > 179) and (self.course < 181) and (self.course > 179)):
            texture = BOAT_0
        elif self.course <= 180:        # Несколько картинок лодки с разным изображенным положением паруса
            if self.mainsheet <= 5:    # Правый галс
                texture = BOAT_RIGHT_5
            elif self.mainsheet <= 15:    # Правый галс
                texture = BOAT_RIGHT_15
            elif self.mainsheet <= 30:
                texture = BOAT_RIGHT_30
            elif self.mainsheet <= 45:
                texture = BOAT_RIGHT_45
            elif self.mainsheet <= 60:
                texture = BOAT_RIGHT_60
            elif self.mainsheet <= 75:
                texture = BOAT_RIGHT_75
            else:
                texture = BOAT_RIGHT_90
        else:
            if self.mainsheet <= 5:    # Левый галс
                texture = BOAT_LEFT_5
            elif self.mainsheet <= 15:    # Левый галс
                texture = BOAT_LEFT_15
            elif self.mainsheet <= 30:
                texture = BOAT_LEFT_30
            elif self.mainsheet <= 45:
                texture = BOAT_LEFT_45
            elif self.mainsheet <= 60:
                texture = BOAT_LEFT_60
            elif self.mainsheet <= 75:
                texture = BOAT_LEFT_75
            else:
                texture = BOAT_LEFT_90

        blit_rotate_center(win, texture, (self.x, self.y), self.course) 

def draw(win, textures, boat1):
    """
    Функция отрисовывает всё.

    Parameters
    ----------
    win : окно
    textures : массив кортежей изображений статичных элементов и их координат
    boat1 : объект класса Boat
    """
    
    for picture, position in textures:
        win.blit(picture, position)
    
    boat1.draw(win)

    pygame.display.update()


if __name__ == '__main__':
    run = True
else:
    run = False

clock = pygame.time.Clock()

static_textures = [(WATER, (0, 0)), (WIND_ARROW, (WIDTH - 200, 50))]
"""Статические объекты"""

boat1 = Boat(3.34, 170, 1)
"""Объект класса Boat с параметрами, близкими к олимпийскому классу Finn"""

while run:
    clock.tick(FPS)
    for event in pygame.event.get(): #Проверка на выход
        if event.type == pygame.QUIT:
            run = False
            break

    draw(WIN, static_textures, boat1) # отрисовка объектов
    pressed_keys = pygame.key.get_pressed() # считывание нажатых клавиш
    
    if pressed_keys[pygame.K_a]: # клавиши a и d отвечают за поворот руля
        boat1.rudder_operate(boat1.speed, left = True)  
    elif pressed_keys[pygame.K_d]:
        boat1.rudder_operate(boat1.speed, right = True)
    if pressed_keys[pygame.K_w]: # клавиши w и s отвечают за длину гика шкота
        boat1.mainsheet_operate(loosen = True)
    elif pressed_keys[pygame.K_s]:
        boat1.mainsheet_operate(tighten = True)
    boat1.move() #перемещение лодки

pygame.quit()