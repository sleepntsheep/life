import pygame
from config import *

class Game:
    def __init__(self):
        self.state = 'setup'
        self.gen = 0
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.grids = [[] for i in range(GRID_ROW)]
        self.frame = 0
        for i in range(0, GRID_ROW):
            for j in range(0, GRID_COL):
                self.grids[i].append(0)

        ...

    def state_manager(self):
        if self.state == 'setup':
            self.setup()
        elif self.state == 'main_game':
            self.main_game()

    def get_neighbor(self, x: int, y: int):
        """
        params: x, y - the coordinates of the grid
        return: the number of neighbors of a grid
        """

        neighbors = [(x-1, y+1), (x-1, y), (x-1, y-1), (x, y+1), (x, y-1), (x+1, y+1), (x+1, y), (x+1, y-1)]

        neighbors_count = 0

        for cord in neighbors:
            if cord[0] != -1 and cord[1] != -1 and cord[0] != GRID_ROW and cord[1] != GRID_COL:
                if self.grids[cord[0]][cord[1]]:
                    neighbors_count += 1

        return neighbors_count

    def draw_grid(self):
        for ix, row in enumerate(self.grids):
            for iy, cell in enumerate(row):
                pygame.draw.rect(self.screen, BDCOLOR, (ix*GRID_SIZE, iy*GRID_SIZE, GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(self.screen, FGCOLOR if cell else BGCOLOR, (ix*GRID_SIZE + 1, iy*GRID_SIZE + 1, GRID_SIZE - 2, GRID_SIZE - 2))


    def setup(self):
        """SETUP BEFORE STARTING GAME"""

        self.screen.fill(BGCOLOR)

        self.draw_grid()

        pygame.display.update()

        # handle e >> s[i]vents
        for event in pygame.event.get():


            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print(pos)
                x = pos[0] // GRID_SIZE
                y = pos[1] // GRID_SIZE
                self.grids[x][y] ^= True #invert state
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.state = 'main_game'

    def main_game(self):
        """MAIN GAME STATE"""

        self.screen.fill(BGCOLOR)

        # logic for the grids
        if self.frame % (FPS / GPS) == 0:
            temp = []
            for i in range(0, GRID_ROW):
                temp.append([])
            for ix, row in enumerate(self.grids):
                for iy, cell in enumerate(row):
                    neighbors = self.get_neighbor(ix, iy)
                    if neighbors > 3 or neighbors < 2:
                        temp[ix].append(0)
                    elif neighbors == 3:
                        temp[ix].append(1)
                    else:
                        temp[ix].append(self.grids[ix][iy])

            self.grids = temp

            del temp

        self.draw_grid()

        pygame.display.update()

        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.state = 'setup'

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
