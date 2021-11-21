import pygame
from config import *


class Game:
    def __init__(self):
        self.state = 'setup'
        self.gen = 0
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.grids = {}
        self.frame = 0
        self.cell_size = GRID_SIZE
        self.x = MIDWIDTH // self.cell_size
        self.y = MIDHEIGHT // self.cell_size
        self.borderwidth = self.cell_size / 16

    def state_manager(self):
        if self.state == 'setup':
            self.setup()
        elif self.state == 'main_game':
            self.main_game()

    def get_neighbor(self, cell):
        """
        params: x, y - the coordinates of the grid
        return: the number of neighbors of a grid
        """
        x = cell[0]
        y = cell[1]

        neighbors = [(x-1, y+1), (x-1, y), (x-1, y-1), (x, y+1),
                     (x, y-1), (x+1, y+1), (x+1, y), (x+1, y-1)]

        neighbors_count = 0

        for cord in neighbors:
            # if cord[0] != -1 and cord[1] != -1 and cord[0] != GRID_ROW and cord[1] != GRID_COL:
            if cord in self.grids:
                neighbors_count += 1

        return neighbors_count

    def draw_grid(self, borderall=False):
        cellsize = self.cell_size - 2 * self.borderwidth
        if borderall:
            self.screen.fill(BDCOLOR)

            for x in range(GRID_ROW):
                for y in range(GRID_COL):
                    pygame.draw.rect(self.screen, BGCOLOR, (x * self.cell_size + self.borderwidth, y * self.cell_size+self.borderwidth, cellsize, cellsize))
        for cell in self.grids:
            ix = cell[0]
            iy = cell[1]
            posx = (self.x + ix) * self.cell_size
            posy = (self.y + iy) * self.cell_size
            pygame.draw.rect(self.screen, BDCOLOR,
                             (posx, posy, self.cell_size, self.cell_size))
            pygame.draw.rect(self.screen, FGCOLOR if cell else BGCOLOR,
                             (posx + self.borderwidth, posy + self.borderwidth, cellsize, cellsize))

    def setup(self):
        """SETUP BEFORE STARTING GAME"""

        self.screen.fill(BGCOLOR)

        self.draw_grid(borderall=True)

        pygame.display.update()

        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                self.toggle_cell(pos)
            elif event.type == pygame.KEYDOWN:
                self.handlekey(event.key)

    def handlekey(self, key):
        if key == pygame.K_SPACE:
            self.state = 'main_game' if self.state == 'setup' else 'setup'
        elif key == ord('j'):
            self.move(3)
        elif key == ord('k'):
            self.move(1)
        elif key == ord('h'):
            self.move(2)
        elif key == ord('l'):
            self.move(4)
        elif key == ord('-'):
            self.zoom(1)
        elif key == ord('='):
            self.zoom(0)

    def move(self, direction: int):
        if direction == 1:
            self.y += 1
        elif direction == 2:
            self.x += 1
        elif direction == 3:
            self.y -= 1
        elif direction == 4:
            self.x -= 1

    def zoom(self, out: int):
        if out:
            self.cell_size -= 1
        else:
            self.cell_size += 1
        self.borderwidth = self.cell_size // 16

    def toggle_cell(self, pos):
        x = pos[0] // self.cell_size - self.x
        y = pos[1] // self.cell_size - self.y
        if (x, y) in self.grids:
            del self.grids[(x, y)]
        else:
            self.grids[(x, y)] = 1

    def all_neighbors(self, cell):
        x = cell[0]
        y = cell[1]
        return [(x-1, y-1), (x-1, y), (x-1, y+1), (x, y-1), (x, y+1), (x+1, y+1), (x+1, y), (x+1, y-1), (x, y)]

    def main_game(self):
        """MAIN GAME STATE"""

        self.screen.fill(BGCOLOR)

        # logic for the grids
        if self.frame % (FPS / GPS) == 0:
            temp = {}
            for cell in self.grids:
                nei_count = self.all_neighbors(cell)
                for nei in self.all_neighbors(cell):
                    nc = (self.get_neighbor(nei))
                    if nc < 2 or nc > 3:
                        continue
                    elif nc == 3:
                        temp[nei] = 1
                    elif nei in self.grids and nc == 2:
                        temp[nei] = 1

            self.grids = temp
            del temp

        self.draw_grid()

        pygame.display.update()

        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.handlekey(event.key)

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.state_manager()
            self.frame += 1
        pygame.quit()


def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
