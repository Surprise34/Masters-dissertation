import heapq
import pygame
import random
import time

from graph import Node, Graph, Grid
from algoritm import initAlgoritm, moveAndRescan, nameToCoords, heuristic_v2

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY1 = (145, 145, 102)
GRAY2 = (77, 77, 51)
BLUE = (0, 0, 80)
ORANGE = (255, 83, 0)
PURPLE = (240, 15, 185)

colors = {
    0: WHITE,
    1: GREEN,
    -1: GRAY1,
    -2: GRAY2
}

#Длина и ширина каждой клетки, а также толщина обводки
WIDTH = 25
HEIGHT = 25
MARGIN = 1

pygame.init()

#Размер сетки
X_DIM = 16
Y_DIM = 16

#Радиус видимости робота
VIEWING_RANGE = 3

WINDOW_SIZE = [(WIDTH + MARGIN) * X_DIM + MARGIN,
               (HEIGHT + MARGIN) * Y_DIM + MARGIN]
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Построение маршрута")
done = False
finalPathDone = False
clock = pygame.time.Clock()

#инициализация программы
if __name__ == "__main__":
    graph = Grid(X_DIM, Y_DIM)
    vertex_start = 'x1y3' #Начальная точка
    vertex_finish = 'x14y9' #Конечная точка
    start_coords = nameToCoords (vertex_start)
    finish_coords = nameToCoords(vertex_finish)
    graph.setStart(vertex_start)
    graph.setFinish(vertex_finish)
    k_m = 0
    vertex_last = vertex_start
    queue = []
    graph, queue, k_m = initAlgoritm(graph, queue, vertex_start, vertex_finish, k_m)
    vertex_current = vertex_start
    pos_coords = nameToCoords(vertex_current)
    basicfont = pygame.font.SysFont('Calibri', 16)

    #Ограничениe1 389
    #for i in range (3000):
        #x_random = random.randint(0,149)
        #y_random = random.randint(0,149)
        #if graph.cells[x_random][y_random] == 0:
            #graph.cells[x_random][y_random] = -1
            
    '''
    #Ограничение2
    for q in range (4):
        for w in range (2):
            if(graph.cells[q+4][w+6] == 0): 
                graph.cells[q+4][w+6] = -1
    #Ограничение3
    for q in range (4):
        for w in range (2):
            if(graph.cells[w+6][q+9] == 0): 
                graph.cells[w+6][q+9] = -1
    #Ограничение4
    for q in range (4):
        for w in range (2):
            if(graph.cells[w+9][q+11] == 0): 
                graph.cells[w+9][q+11] = -1
    #Ограничение5
    for q in range (4):
        for w in range (2):
            if(graph.cells[q+4][w+6] == 0): 
                graph.cells[q+4][w+6] = -1
    '''
    finalPath=[start_coords]
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                vertex_new, k_m = moveAndRescan(
                    graph, queue, vertex_current, VIEWING_RANGE, k_m)
                if vertex_new == 'finish' and finalPathDone==True:
                    done=True
                elif vertex_new == 'finish':
                    finalPathDone=True
                else:
                    vertex_current = vertex_new
                    pos_coords = nameToCoords(vertex_current)
                finalPath+=[pos_coords]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()                    
                    column = pos[0] // (WIDTH + MARGIN)
                    row = pos[1] // (HEIGHT + MARGIN)
                    print (pos)
                    #print('x'+str(column)+'y'+str(row))
                    if(graph.cells[row][column] == 0):
                        graph.cells[row][column] = -1
                elif event.button == 3:
                    pos = pygame.mouse.get_pos()
                    column = pos[0] // (WIDTH + MARGIN)
                    row = pos[1] // (HEIGHT + MARGIN)
                    if(graph.cells[row][column] == -1 or graph.cells[row][column] == -2):
                        graph.cells[row][column] = 0
        screen.fill(BLACK)
        for row in range(Y_DIM):
            for column in range(X_DIM):
                color = WHITE
                pygame.draw.rect(screen, colors[graph.cells[row][column]],
                                 [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])
                node_name = 'x' + str(column) + 'y' + str(row)
                if(graph.graph[node_name].g != float('inf')):
                    '''
                    text = basicfont.render(
                        str(graph.graph[node_name].g), True, (0, 0, 200))
                    textrect = text.get_rect()
                    textrect.centerx = int(
                        column * (WIDTH + MARGIN) + WIDTH / 2) + MARGIN
                    textrect.centery = int(
                        row * (HEIGHT + MARGIN) + HEIGHT / 2) + MARGIN
                    screen.blit(text, textrect)
                    '''

        pygame.draw.rect(screen, ORANGE, [(MARGIN + WIDTH) * start_coords[0] + MARGIN, (MARGIN + HEIGHT) * start_coords[1] + MARGIN, WIDTH, HEIGHT])
        pygame.draw.rect(screen, GREEN, [(MARGIN + WIDTH) * finish_coords[0] + MARGIN,(MARGIN + HEIGHT) * finish_coords[1] + MARGIN, WIDTH, HEIGHT])
        robot_center = [int(pos_coords[0] * (WIDTH + MARGIN) + WIDTH / 2) + MARGIN, int(pos_coords[1] * (HEIGHT + MARGIN) + HEIGHT / 2) + MARGIN]
        pygame.draw.circle(screen, RED, robot_center, int(WIDTH / 2) - 2)
        #pygame.draw.rect(
            #screen, GREEN, [robot_center[0] - VIEWING_RANGE * (WIDTH + MARGIN), robot_center[1] - VIEWING_RANGE * (HEIGHT + MARGIN), 2 * VIEWING_RANGE * (WIDTH + MARGIN), 2 * VIEWING_RANGE * (HEIGHT + MARGIN)], 2)
        if finalPathDone==True:
            for i in range(1,len(finalPath)-2):
                        pygame.draw.rect(screen, PURPLE, [(MARGIN + WIDTH) * finalPath[i][0] + MARGIN,
                                         (MARGIN + HEIGHT) * finalPath[i][1] + MARGIN, WIDTH, HEIGHT])
        clock.tick(20)
        pygame.display.flip()
    pygame.quit()
