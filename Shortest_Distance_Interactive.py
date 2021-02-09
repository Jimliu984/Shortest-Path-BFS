import numpy as np
import pygame
import sys
import collections
import heapq

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('Shortest Distance')

FINDCOL = (255, 200, 200)

class ShortestPath:
    def __init__(self, m, n):
        self.squaresize = 20
        self.m = m
        self.n = n
        self.start = (np.random.randint(0,int(m/4)-1), np.random.randint(0,int(n/4)-1))
        self.end = (np.random.randint(int(m/4),m), np.random.randint(int(n/4),n))
        # self.start = (10,45)
        # self.end = (30, 45)
        self.HEIGHT = self.m * self.squaresize
        self.WIDTH = self.n * self.squaresize
        self.GRID = [[0]*self.n for _ in range(self.m)]
        self.GRID[self.start[0]][self.start[1]] = 2
        self.GRID[self.end[0]][self.end[1]] = 3
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.route = collections.defaultdict(list)

    def drawgrid(self):
        self.screen.fill((0,0,0))
        for x in range(self.m):
            for y in range(self.n):
                if self.GRID[x][y] == 0:
                    pygame.draw.rect(self.screen, (255,255,255), (y*self.squaresize, x*self.squaresize, self.squaresize, self.squaresize))
                elif self.GRID[x][y] == 2:
                    pygame.draw.rect(self.screen, (0,0,255), (y*self.squaresize, x*self.squaresize, self.squaresize, self.squaresize))
                elif self.GRID[x][y] == 3:
                    pygame.draw.rect(self.screen, (0,255,0), (y*self.squaresize, x*self.squaresize, self.squaresize, self.squaresize))
        pygame.display.update()

    def clickdraw(self, position):
        position = [position[0] - position[0] % self.squaresize, position[1] - position[1] % self.squaresize]
        x = int((position[0] - position[0] % self.squaresize)/self.squaresize)
        y = int((position[1] - position[1] % self.squaresize)/self.squaresize)
        if self.GRID[y][x] == 0:
            self.GRID[y][x] = 1
            pygame.draw.rect(self.screen, (0, 0, 0), (position[0], position[1], self.squaresize, self.squaresize))

    def undraw(self, position):
        position = [position[0] - position[0] % self.squaresize, position[1] - position[1] % self.squaresize]
        x = int((position[0] - position[0] % self.squaresize) / self.squaresize)
        y = int((position[1] - position[1] % self.squaresize) / self.squaresize)
        if self.GRID[y][x] == 1:
            self.GRID[y][x] = 0
            pygame.draw.rect(self.screen, (255, 255, 255),
                             (position[0], position[1], self.squaresize, self.squaresize))

    def bfs(self):
        next = queue = [self.start]
        seen = set(next)
        count = 1
        while next:
            temp = len(queue)
            for _ in range(temp):
                x, y = next.pop(0)
                for a, b in (x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y):
                    if self.m > a >= 0 and self.n > b >= 0 and (a, b) not in seen:
                        if self.GRID[a][b] == 0:
                            pygame.draw.rect(self.screen, FINDCOL,
                                             (b * self.squaresize, a * self.squaresize, self.squaresize, self.squaresize))
                            next.append((a, b))
                            seen.add((a, b))
                            self.route[count].append((a, b))
                        elif self.GRID[a][b] == 3:
                            return count
            count += 1
            queue = next
            clock.tick(40)
            pygame.display.update()
        return -1

    def findpath_bfs(self):
        current = self.end
        for x in range(self.distance-1,0,-1):
            if (current[0] - 1, current[1]) in self.route[x]:
                current = (current[0] - 1, current[1])
            elif (current[0], current[1] - 1) in self.route[x]:
                current = (current[0], current[1] - 1)
            elif (current[0] + 1, current[1]) in self.route[x]:
                current = (current[0] + 1, current[1])
            elif (current[0], current[1] + 1) in self.route[x]:
                current = (current[0], current[1] + 1)
            pygame.draw.rect(self.screen, (200, 255, 255),
                             (current[1] * self.squaresize, current[0] * self.squaresize, self.squaresize,
                              self.squaresize))
            pygame.display.update()
        print(self.distance)

    def solve(self):
        self.drawgrid()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if pygame.mouse.get_pressed()[0]:
                    position = pygame.mouse.get_pos()
                    self.clickdraw(position)
                    pygame.display.update()
                elif pygame.mouse.get_pressed()[1]:
                    position = pygame.mouse.get_pos()
                    self.undraw(position)
                    pygame.display.update()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.distance = self.bfs()
                        if self.distance == -1:
                            print("No Path")
                            break
                        else:
                            self.findpath_bfs()
                            break

Short = ShortestPath(40,60)
Short.solve()
