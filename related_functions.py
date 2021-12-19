"""
Модуль содержит функции, применяющиеся в вычислениях и отрисовке.

Functions
---------
blit_rotate_center(win, image, top_left, angle)
angle_between_two_vectors(angle1, angle2)
angle_by_sin_cos(sin, cos)
"""

import math
import pygame


def blit_rotate_center(win, image, top_left, angle):
    '''функция ЗАИМСТВОВАНА с https://github.com/techwithtim/Pygame-Car-Racer.\n
    Поворачивает изображение на заданный угол относительно центра изображения

    Parameters
    ----------
    win : окно
    image : изображение
    top_left : координата верхнего левого угла изображения
    angle : угол поворта в градусах
    '''
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = top_left).center)
    win.blit(rotated_image, new_rect.topleft)
    # КОНЕЦ ЗАИМСТВОВАНИЯ

def angle_between_two_vectors(angle1, angle2):
    '''Находит угол между двумя векторами по их углам.

    Parameters
    ----------
    angle1 : угол первого вектора в градусах [0 - 360)
    angle2 : угол второго вектора [0 - 360)

    Returns
    -------
    Угол в градусах [0 - 360).
    '''
    if angle1 > angle2:
        dif = angle1 - angle2
    else: 
        dif = angle2 - angle1

    if dif <= 180:
        return dif
    else:
        return (360 - dif)

def angle_by_sin_cos(sin, cos):
    '''Находит угол от по его синусу и косинусу.
    
    Parametres
    ----------
    sin : синус угла
    cos : косинус угла

    Returns
    -------
    Угол в градусах [0 - 360).
    '''
    e  = 0.0000001
    if math.fabs(math.asin(sin) - math.acos(cos)) < e:
        result = math.degrees(math.asin(sin))
    elif math.fabs((math.pi - math.asin(sin)) == math.acos(cos)) < e:
        result = math.degrees(math.pi - math.asin(sin))
    elif math.fabs((math.pi - math.asin(sin)) == -math.acos(cos)) < e:
        result = math.degrees(math.pi - math.asin(sin))
    else:
        result =  math.degrees(math.asin(sin))
    if result < 0:
        result += 360
    return result