import time
import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import numpy as np

COLOR_BG = (0, 0, 0)
COLOR_GRID = (40, 40, 40)
COLOR_DIE_NEXT = (170, 170, 170)
COLOR_ALIVE_NEXT = (255, 255, 255)
SETTINGS_MENU_SIZE = 100


def update(scren, cells, size, with_progress=False):
    update_cells = np.zeros((cells.shape[0], cells.shape[1]))

    for row, col in np.ndindex(cells.shape):
        alive = np.sum(cells[row-1:row + 2, col - 1 : col + 2]) - cells[row, col]
        color = COLOR_BG if cells[row, col] == 0 else COLOR_ALIVE_NEXT

        if cells[row, col] == 1:
            if alive < 2 or alive > 3:
                if with_progress:
                    color = COLOR_DIE_NEXT
            elif 2 <= alive <= 3:
                update_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT
        else:
            if alive == 3:
                update_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT
        pygame.draw.rect(scren, color, (col * size, row * size + SETTINGS_MENU_SIZE, size - 1, size - 1))

    return update_cells

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    slider = Slider(screen, 50, 50, 100, 15, min=0.001, max=0.1, step=0.001, initial=0.001, handleRadius=12)
    textbox = TextBox(screen, 175, 36, 50, 50, fontSize=20, radius=10)
    clearButton = TextBox(screen, 700, 36, 50, 50, fontSize=20, borderColour=(255, 0, 0), textColour=(255, 0, 0), radius=10)

    textbox.disable()
    clearButton.setText('Clear')
    clearButton.disable()

    cells = np.zeros((60, 80))
    screen.fill(COLOR_GRID)
    update(screen, cells, 10)

    pygame.display.flip()
    pygame.display.update()

    running = False
    init = True

    while True:
        events = pygame.event.get()
        textbox.setText(str(round(slider.getValue(), 3)))
        pygame_widgets.update(events)

        if init:
            pygame.display.update()
            init = False

        for event in events:
            if event.type == pygame.QUIT:
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    update(screen, cells, 10)
                    pygame.display.update()

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                
                if pos[1] < SETTINGS_MENU_SIZE:
                    if 700 <= pos[0] <= 750:
                        cells = np.zeros((60, 80))
                        update(screen, cells, 10)
                    update(screen, cells, 10)
                    pygame.display.update()
                    continue

                cells[(pos[1] - SETTINGS_MENU_SIZE) // 10, pos[0] // 10] = 1
                update(screen, cells, 10)
                pygame.display.update()

        screen.fill(COLOR_GRID)

        if running:
            cells = update(screen, cells, 10, with_progress=True)
            pygame.display.update()

        time.sleep(slider.getValue())

if __name__ == '__main__':
    main()
            
