import pygame
import sys
import os
import main as main1
import sqlite3


def terminate():
    pygame.quit()
    # sys.exit()


def start_main_wnd():
    if __name__ == '__main__':
        app = main1.QApplication(sys.argv)
        ex1 = main1.MainWindow()
        ex1.show()
        sys.exit(app.exec())


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Board:
    def __init__(self, width, height, surface, enemy, nick):
        self.screen = surface
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.nick = nick
        self.top = 10
        self.left = 10
        self.cell_size = 30

        self.enemy = enemy
        self.move_now = 1
        self.cell_dict = {}
        empty_cell = 0

        if self.nick == '':
            self.nick = 'Anonim'

        for i in range(self.width):
            for j in range(self.height):
                cell_temp = i, j
                self.cell_dict[cell_temp] = empty_cell

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        self.x = self.left
        self.y = self.top
        count_cube = int(self.width) * int(self.height)
        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(screen, (255, 255, 255, 100), (self.x, self.y, self.cell_size,
                                                                self.cell_size), width=1)
                self.y += self.cell_size
            self.y = self.top
            self.x += self.cell_size

    def get_cell(self, mouse_pos):
        self.x1, self.y1 = mouse_pos
        self.x1 -= self.left
        self.y1 -= self.top
        self.cell_x = self.x1 // self.cell_size
        self.cell_y = self.y1 // self.cell_size
        cell_coords = self.cell_x, self.cell_y
        if self.cell_x >= self.width or self.cell_x < 0:
            cell_coords = 'None'
        if self.cell_y >= self.height or self.cell_y < 0:
            cell_coords = 'None'
        # print(cell_coords)
        return cell_coords

    def on_click(self, cell):
        self.color_red = pygame.Color('Red')
        self.color_blue = pygame.Color('Blue')
        self.cell_pressed = cell

        self.x_top_cell_pressed = self.left + self.cell_size * self.cell_x + self.width * 10
        self.y_top_cell_pressed = self.top + self.cell_size * self.cell_y + self.height * 10
        self.x_low_cell_pressed = self.left + self.cell_size * (self.cell_x) \
                                  + self.cell_size - self.width * 10
        self.y_low_cell_pressed = self.top + self.cell_size * (self.cell_y) \
                                  + self.cell_size - self.height * 10

        self.x_top_cell_pressed1 = self.left + self.cell_size * (self.cell_x) \
                                   + self.cell_size - self.width * 10
        self.y_top_cell_pressed1 = self.top + self.cell_size * self.cell_y + self.height * 10
        self.x_low_cell_pressed1 = self.left + self.cell_size * (self.cell_x) \
                                   + self.width * 10
        self.y_low_cell_pressed1 = self.top + self.cell_size * (self.cell_y) \
                                   + self.cell_size - self.height * 10

        self.x_center = self.left + (self.cell_size * self.cell_x) + self.cell_size // 2
        self.y_center = self.top + (self.cell_size * self.cell_y) + self.cell_size // 2

        print(self.cell_pressed)
        if self.cell_pressed != 'None':
            if self.cell_dict[self.cell_pressed] == 0:
                self.move_now += 1
                if self.move_now % 2 == 0:
                    self.draw_crest()
                if self.move_now % 2 == 1:
                    self.draw_circ()
        self.side_win = self.check_win()

    def draw_crest(self):
        pygame.draw.line(self.screen, self.color_red, (self.x_top_cell_pressed, self.y_top_cell_pressed),
                         (self.x_low_cell_pressed, self.y_low_cell_pressed), width=5)

        pygame.draw.line(self.screen, self.color_red, (self.x_top_cell_pressed1, self.y_top_cell_pressed1),
                         (self.x_low_cell_pressed1, self.y_low_cell_pressed1), width=5)
        self.cell_dict[self.cell_pressed] = 1

    def draw_circ(self):
        pygame.draw.circle(self.screen, self.color_blue, (self.x_center, self.y_center), 50, width=5)
        self.cell_dict[self.cell_pressed] = 2

    def check_win(self):
        win_side = 0
        if (self.cell_dict[0, 0] == self.cell_dict[1, 0] == self.cell_dict[2, 0] == 1) \
                or (self.cell_dict[0, 0] == self.cell_dict[0, 1] == self.cell_dict[0, 2] == 1) \
                or (self.cell_dict[0, 0] == self.cell_dict[1, 1] == self.cell_dict[2, 2] == 1) \
                or (self.cell_dict[0, 2] == self.cell_dict[1, 1] == self.cell_dict[2, 0] == 1) \
                or (self.cell_dict[0, 2] == self.cell_dict[1, 2] == self.cell_dict[2, 2] == 1) \
                or (self.cell_dict[2, 2] == self.cell_dict[2, 1] == self.cell_dict[2, 0] == 1) \
                or (self.cell_dict[0, 1] == self.cell_dict[1, 1] == self.cell_dict[2, 1] == 1) \
                or (self.cell_dict[1, 0] == self.cell_dict[1, 1] == self.cell_dict[1, 2] == 1):
            print('ПОБЕДА')
            self.win_side = 1
            self.base_event()
            draw_status(self.win_side, self.width, self.height, self.screen)

        if (self.cell_dict[0, 0] == self.cell_dict[1, 0] == self.cell_dict[2, 0] == 2) \
                or (self.cell_dict[0, 0] == self.cell_dict[0, 1] == self.cell_dict[0, 2] == 2) \
                or (self.cell_dict[0, 0] == self.cell_dict[1, 1] == self.cell_dict[2, 2] == 2) \
                or (self.cell_dict[0, 2] == self.cell_dict[1, 1] == self.cell_dict[2, 0] == 2) \
                or (self.cell_dict[0, 2] == self.cell_dict[1, 2] == self.cell_dict[2, 2] == 2) \
                or (self.cell_dict[2, 2] == self.cell_dict[2, 1] == self.cell_dict[2, 0] == 2) \
                or (self.cell_dict[0, 1] == self.cell_dict[1, 1] == self.cell_dict[2, 1] == 2) \
                or (self.cell_dict[1, 0] == self.cell_dict[1, 1] == self.cell_dict[1, 2] == 2):
            print('ПОРАЖЕНИЕ')
            self.win_side = 2
            self.base_event()
            draw_status(self.win_side, self.width, self.height, self.screen)

        if self.cell_dict[0, 1] != 0 and self.cell_dict[0, 2] != 0 and self.cell_dict[0, 0] != 0 \
                and self.cell_dict[1, 0] != 0 and self.cell_dict[2, 2] != 0 \
                and self.cell_dict[1, 1] != 0 and self.cell_dict[1, 2] != 0 \
                and self.cell_dict[2, 0] != 0 and self.cell_dict[2, 1] != 0:
            print('НИЧЬЯ')
            self.win_side = 3
            self.base_event()
            draw_status(self.win_side, self.width, self.height, self.screen)

    def base_event(self):
        con = sqlite3.connect("data\\bd.sqlite")
        cur = con.cursor()

        result = cur.execute("""SELECT *
                            FROM Base""").fetchall()

        print(self.nick)
        for i in result:
            if i[1] == self.nick:
                if self.win_side == 1:
                    win = int(i[2])
                    win += 1
                    cur.execute("""UPDATE Base
                                SET Win = ?
                                WHERE Nickname = ?""", (win, self.nick))
                    con.commit()
                if self.win_side == 2:
                    lose = int(i[3])
                    lose += 1
                    cur.execute("""UPDATE Base
                                SET Lose = ?
                                WHERE Nickname = ?""", (lose, self.nick))
                    con.commit()
                if self.win_side == 3:
                    draw = int(i[4])
                    draw += 1
                    cur.execute("""UPDATE Base
                                SET Draw = ?
                                WHERE Nickname = ?""", (draw, self.nick))
                    con.commit()
                    print(draw)


    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)


def draw_status(win_side, width, height, screen):
    if win_side == 1:
        intro_text = ["Крестики выиграли",
                      "Нажмите любую клавишу,",
                      "чтобы выйти в меню."]
    if win_side == 2:
        intro_text = ["Нолики выиграли",
                      "Нажмите любую клавишу,",
                      "чтобы выйти в меню"]
    if win_side == 3:
        intro_text = ["Ничья",
                      "Нажмите любую клавишу,",
                      "чтобы выйти в меню"]
    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 40)
    text_coord = height * 40
    for line in intro_text:
        if win_side == 1:
            string_rendered = font.render(line, 1, pygame.Color('green'))
        if win_side == 2:
            string_rendered = font.render(line, 1, pygame.Color('red'))
        if win_side == 2:
            string_rendered = font.render(line, 1, pygame.Color('blue'))
        intro_rect = string_rendered.get_rect()
        text_coord += 20
        intro_rect.top = text_coord
        intro_rect.x = width * 180
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        ev = 0
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                start_main_wnd()
            pygame.display.flip()


        # start_main_wnd()
