"""
Модуль содержит словарь sail_force_by_angle с эксперементальными данными для разныых углов атаки паруса
ПРИМЕЧАНИЕ: данные для значений (90 - 180] я не нашёл в литературе, так как в таком режиме(задняя шкаторина смотрит на ветер) парус
может использоваться c пользой только для заднего хода, что не являлось предметом исследований, на которые я опирался.
Для заполнения пробела я просто взял обратные значения с коэфициентом 0.7 (Значительно подкорректироанные),
так как они почти не влияют на игровой процесс.
"""

sail_force_by_angle = {
0:(0.1, 0), 5:(0.1, 0.6), 
10:(0.15, 0.8), 15:(0.25, 0.9), 
20:(0.35, 1), 25:(0.45, 1.1), 
30:(0.51, 1.2), 35:(0.63, 1.1), 
40:(0.7, 1), 45:(0.75, 0.8), 
50:(0.81, 0.7), 55:(0.85, 0.6), 
60:(0.9, 0.55), 65:(0.95, 0.5), 
70:(1.05, 0.42), 75:(1.1, 0.35), 
80:(1.15, 0.3), 85:(1.18, 0.1), 
90:(1.2, 0), 95:(1.2, 0),
100:(0.8, 0.2), 105:(0.8, 0.2),
110:(0.73, 0.29), 115:(0.73, 0.29),
120:(0.63, 0.38), 125:(0.63, 0.38),
130:(0.57, 0.45), 135:(0.57, 0.45),
140:(0.49, 0.52), 145:(0.49, 0.52),
150:(0.35, 0.61), 155:(0.35, 0.61),
160:(0.24, 0.57), 165:(0.24, 0.57),
170:(0.1, 0.49), 175:(0.1, 0),
180:(0.1, 0)}