import pygame
from config import *

class Game:
    def __init__(self):
        self.state = 'main_game'
        self.gen = 0
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.grids = [[] for i in range(GRID_ROW)]
        for i in range(0, GRID_ROW):
            for j in range(0, GRID_COL):
                if i % 3 == 0 and j % 3 == 0:   # if the grid is the middle one
                    self.grids[i].append(1)
                else:
                    self.grids[i].append(0)

        ...

    def state_manager(self):
        if self.state == 'main_game':
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

    def main_game(self):
        """MAIN GAME STATE"""

        self.screen.fill(BGCOLOR)

        # logic for the grids
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
            
        # draw grids
        for ix, row in enumerate(self.grids):
            for iy, cell in enumerate(row):
                    pygame.draw.rect(self.screen, FGCOLOR if cell else BGCOLOR, (ix*GRID_SIZE, iy*GRID_SIZE, GRID_SIZE, GRID_SIZE))

        pygame.display.update()

        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            else:
                ...

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.state_manager()
        pygame.quit()

def main():
    game = Game()
    game.run()
    
if __name__ == '__main__':
    main()
