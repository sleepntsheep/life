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
        self.x = MIDWIDTH // GRID_SIZE
        self.y = MIDHEIGHT // GRID_SIZE
        # for i in range(0, GRID_ROW):
        #     for j in range(0, GRID_COL):
        #         self.grids[i].append(0)

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

        neighbors = [(x-1, y+1), (x-1, y), (x-1, y-1), (x, y+1), (x, y-1), (x+1, y+1), (x+1, y), (x+1, y-1)]

        neighbors_count = 0

        for cord in neighbors:
            # if cord[0] != -1 and cord[1] != -1 and cord[0] != GRID_ROW and cord[1] != GRID_COL:
            if cord in self.grids:
                neighbors_count += 1

        return neighbors_count

    def draw_grid(self):
        for cell in self.grids:
            ix = cell[0]
            iy = cell[1]
            posx = (self.x + ix) *GRID_SIZE
            posy = (self.y + iy) *GRID_SIZE
            pygame.draw.rect(self.screen, BDCOLOR, (posx, posy, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(self.screen, FGCOLOR if cell else BGCOLOR, (posx + 1, posy + 1, GRID_SIZE - 2, GRID_SIZE - 2))


    def setup(self):
        """SETUP BEFORE STARTING GAME"""

        self.screen.fill(BGCOLOR)

        self.draw_grid()

        pygame.display.update()

        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                self.toggle_cell(pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.state = 'main_game'

    def toggle_cell(self, pos):
        x = pos[0] // GRID_SIZE - self.x
        y = pos[1] // GRID_SIZE - self.y
        print(pos)
        print(x, y)
        if (x, y) in self.grids:
            del self.grids[(x, y)]
        else: 
            self.grids[(x, y)] = 1

    def new_gen(self):
        ...

    def all_neighbors(self, cell):
        x = cell[0]
        y = cell[1]
        return [(x-1,y-1), (x-1,y), (x-1,y+1), (x,y-1), (x,y+1), (x+1,y+1), (x+1,y), (x+1,y-1), (x, y)]

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
                    elif nc == 3 :
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
