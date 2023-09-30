import pygame
import random
import functools
import itertools
from tkinter import *
from tkinter import ttk, messagebox

root = Tk()
root.title('Настройки')

w, h = 230, 300
ws, hs = root.winfo_screenwidth(), root.winfo_screenheight()
x, y = (ws//2) - (w//2), (hs//2) - (h//2)
root.geometry(f'{w}x{h}+{x}+{y}')

area_x, area_y = IntVar(value=10), IntVar(value=10)
speed = IntVar(value=8)

ttk.Label(text='Размер поля (ширина и высота): ').pack(padx=5, pady=5, anchor=NW)
ttk.Entry(textvariable=area_x).pack(padx=5, pady=1, anchor=NW)
ttk.Entry(textvariable=area_y).pack(padx=5, pady=1, anchor=NW)
ttk.Label(text='Скорость: ').pack(padx=5, pady=5, anchor=NW)
ttk.Entry(textvariable=speed).pack(padx=5, pady=1, anchor=NW)

button = ttk.Button(text='Начать!', command=lambda: root.destroy())
button.pack(padx=30, pady=10, anchor=NW)
button.focus_set()

root.protocol("WM_DELETE_WINDOW", lambda: exit(0))
root.mainloop()

CELL_SIZE = (30, 30)
AREA_SIZE = (area_x.get(), area_y.get())
DISPLAY_SIZE = (CELL_SIZE[0] * AREA_SIZE[0], CELL_SIZE[1] * AREA_SIZE[1])
TICKS_PER_SECOND = speed.get()
RECOURCES_PATH = 'recources.png'
RECOURCES_CELL_COUNT = (5, 4)
BACKGROUND_COLOR = (0, 50, 0)
FONT_COLOR = (100, 100, 0)

snake = [[AREA_SIZE[0] // 2, AREA_SIZE[1] // 2], [AREA_SIZE[0] // 2 - 1, AREA_SIZE[1] // 2]]

directions = {
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_RIGHT: (1, 0),
    pygame.K_LEFT: (-1, 0)
}

recources = pygame.image.load(RECOURCES_PATH)
recources = pygame.transform.scale(recources, (CELL_SIZE[0] * RECOURCES_CELL_COUNT[0], CELL_SIZE[1] * RECOURCES_CELL_COUNT[1]))
RECOURCES_CELL_SIZE = (recources.get_size()[0] / RECOURCES_CELL_COUNT[0], recources.get_size()[1] / RECOURCES_CELL_COUNT[1])

body_images = {
    ((-1, 0), (1, 0)): (1, 0),
    ((1, 0), (-1, 0)): (1, 0),
    ((0, -1), (0, 1)): (2, 1),
    ((0, 1), (0, -1)): (2, 1),
    ((0, 1), (1, 0)): (0, 0),
    ((1, 0), (0, 1)): (0, 0),
    ((0, -1), (1, 0)): (0, 1),
    ((1, 0), (0, -1)): (0, 1),
    ((-1, 0), (0, 1)): (2, 0),
    ((0, 1), (-1, 0)): (2, 0),
    ((0, -1), (-1, 0)): (2, 2),
    ((-1, 0), (0, -1)): (2, 2),
}

head_images = {
    (0, -1): (3, 0),
    (1, 0): (4, 0),
    (-1, 0): (3, 1),
    (0, 1): (4, 1),
}

tail_images = {
    (0, -1): (3, 2),
    (1, 0): (4, 2),
    (-1, 0): (3, 3),
    (0, 1): (4, 3),
}

generate_apple = lambda: apple \
    if (apple := [random.randrange(0, AREA_SIZE[0]), random.randrange(1, AREA_SIZE[1])]) not in snake \
    else generate_apple()

to_cell_rect = lambda left_top, size: (left_top[0] * size[0], left_top[1] * size[1], size[0], size[1])

body_image = lambda start, end, current: body_images[((start[0] - current[0], start[1] - current[1]), (end[0] - current[0], end[1] - current[1]))]
head_image = lambda dir: head_images[dir]
tail_image = lambda: tail_images[(snake[-2][0] - snake[-1][0], snake[-2][1] - snake[-1][1])]
apple_image = lambda: (0, 3)

draw_cell_image = lambda pos, rec_pos: display.blit(recources, to_cell_rect(pos, CELL_SIZE), to_cell_rect(rec_pos, RECOURCES_CELL_SIZE))

handle_event = lambda event, score: print(event) or close_game(score) if event.type == pygame.QUIT \
                             else (directions[event.key] if event.key in directions.keys() else None) if event.type == pygame.KEYDOWN \
                             else None

close_game = lambda score: (print('Выход') or
                      [None for _ in messagebox.showinfo(title='Game over!', message=f'Ваш счёт: {score}')][0] or
                      pygame.quit() or exit(0))


pygame.init()
display = pygame.display.set_mode(DISPLAY_SIZE)
pygame.display.set_caption('Змейка!')

pygame.event.clear()
pygame.event.set_allowed((pygame.KEYDOWN, pygame.QUIT))

font = pygame.font.SysFont('Comic Sans MS', 30)

clock = pygame.time.Clock()

functools.reduce(lambda game, _: (

    handle_event(pygame.event.poll(), game[4][1]) or game[0],
    display.fill(BACKGROUND_COLOR),
    snake.insert(0, [snake[0][0] + game[0][0], snake[0][1] + game[0][1]]),
    close_game(game[4][1]) if snake[0] in snake[1:] or not (0 <= snake[0][0] < AREA_SIZE[0]) or not (0 <= snake[0][1] < AREA_SIZE[1]) else None,
    (generate_apple(), game[4][1] + 1) if snake[0] == game[4][0] else [game[4] for _ in [snake.pop()]][0],
    draw_cell_image(game[4][0], apple_image()),
    [draw_cell_image(current, body_image(start, end, current)) for start, end, current in zip(snake[:-2], snake[2:], snake[1:-1])],
    draw_cell_image(snake[0], head_image(game[0])),
    draw_cell_image(snake[-1], tail_image()),
    display.blit(font.render(f'Ваш счёт: {game[4][1]}', True, FONT_COLOR), (0, 0)),
    pygame.display.update(),
    clock.tick(TICKS_PER_SECOND)
 
), itertools.cycle([0]), (
    (1, 0), None, None,  None,
    (generate_apple(), 0)
))
