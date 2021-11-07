import pygame
from config import *

class Game:
    def __init__(self):
        self.state = 'main_game'
        self.gen = 0
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.grids = []
        for i in range(0, GRID_ROW):
            for j in range(0, GRID_COL):
                if i == MID_X and j == MID_Y:   # if the grid is the middle one
                    self.grids.append([i, j, 1])
                else:
                    self.grids.append([i, j, 0])
        ...

    def state_manager(self):
        if self.state == 'main_game':
            self.main_game()

    def get_neighbor(grid: tuple):
        """
        :param grid: grid to get neighbors of
        :return: the number of neighbor of the grid
        """

        
        return 0

    def main_game(self):
        """MAIN GAME STATE"""
        self.screen.fill(BGCOLOR)

        # logic for the grids
        temp = []
        for i in range(0, GRID_ROW):
            for j in range(0, GRID_COL)


        # draw grids
        for grid in self.grids:
            pygame.draw.rect(self.screen, FGCOLOR if grid[2] else BGCOLOR, (grid[0]*GRID_SIZE, grid[1]*GRID_SIZE, GRID_SIZE, GRID_SIZE))

        pygame.display.update()

        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            else:
                ...

    def run(self):
        while self.running:
            self.state_manager()
            self.clock.tick(FPS)
        pygame.quit()

def main():
    game = Game()
    game.run()
    
if __name__ == '__main__':
    main()
