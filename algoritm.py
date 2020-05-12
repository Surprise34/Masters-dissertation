import heapq
import random
import math

def nameToCoords(name):
    return [int(name.split('x')[1].split('y')[0]), int(name.split('x')[1].split('y')[1])]

def getElement(queue):
    queue.sort()
    if len(queue) > 0:
        return queue[0][:2]
    else:
        return (float('inf'), float('inf'))

def heuristic(graph, id, vertex):
    x_distance = abs(int(id.split('y')[0].split('x')[1]) - int(vertex.split('y')[0].split('x')[1]))
    y_distance = abs(int(id.split('y')[1]) - int(vertex.split('y')[1]))
    return max(x_distance, y_distance)

def heuristic_v2(graph, id, vertex):
    x_distance = abs(int(id.split('y')[0].split('x')[1]) - int(vertex.split('y')[0].split('x')[1]))
    y_distance = abs(int(id.split('y')[1]) - int(vertex.split('y')[1]))
    return x_distance + y_distance


def calculation_of_element(graph, id, vertex_current, k_m):
    return (min(graph.graph[id].g, graph.graph[id].g_aware) + heuristic(graph, id, vertex_current) + k_m, min(graph.graph[id].g, graph.graph[id].g_aware))

#Вычисление значения ячейки
def calculation_of_cell(graph, queue, id, vertex_current, k_m):
    vertex_finish = graph.finish
    if id != vertex_finish:
        min_g_aware = float('inf')
        for i in graph.graph[id].children:
            min_g_aware = min(
                min_g_aware, graph.graph[i].g + graph.graph[id].children[i])
        graph.graph[id].g_aware = min_g_aware
    id_in_queue = [item for item in queue if id in item]
    if id_in_queue != []:
        if len(id_in_queue) != 1:
            raise ValueError('В очереди больше, чем один ' + id)
        queue.remove(id_in_queue[0])
    if graph.graph[id].g_aware != graph.graph[id].g:
        heapq.heappush(queue, calculation_of_element(graph, id, vertex_current, k_m) + (id,))

#Вычисление значений всей сетки
def calculation_of_path(graph, queue, vertex_start, k_m):
    while (graph.graph[vertex_start].g_aware != graph.graph[vertex_start].g) or (getElement(queue) < calculation_of_element(graph, vertex_start, vertex_start, k_m)):
        k_old = getElement(queue)
        u = heapq.heappop(queue)[2]
        if k_old < calculation_of_element(graph, u, vertex_start, k_m):
            heapq.heappush(queue, calculation_of_element(graph, u, vertex_start, k_m) + (u,))
        elif graph.graph[u].g > graph.graph[u].g_aware:
            graph.graph[u].g = graph.graph[u].g_aware
            for i in graph.graph[u].parents:
                calculation_of_cell(graph, queue, i, vertex_start, k_m)
        else:
            graph.graph[u].g = float('inf')
            calculation_of_cell(graph, queue, u, vertex_start, k_m)
            for i in graph.graph[u].parents:
                calculation_of_cell(graph, queue, i, vertex_start, k_m)

#Функция выбора следующего шага
def next_step_in_path(graph, vertex_current):
    min_g_aware = float('inf')
    vertex_next = None
    array_of_vertex_next=[]
    if graph.graph[vertex_current].g_aware == float('inf'):
        print('Заблудились')
    else:
        for i in graph.graph[vertex_current].children:
            child_cost = graph.graph[i].g + graph.graph[vertex_current].children[i]
            if (child_cost) < min_g_aware:
                min_g_aware = child_cost
                #vertex_next = i
        for j in graph.graph[vertex_current].children:
            child_cost = graph.graph[j].g + graph.graph[vertex_current].children[j]
            if child_cost == min_g_aware:
                array_of_vertex_next += [j]
        #vertex_next = random.choice(array_of_vertex_next)
        min_heuristic_value=float('inf')
        for v in array_of_vertex_next:
            v_v = heuristic_v2(graph, v, graph.finish)
            #print (v+' '+str(v_v)+' '+str(min_heuristic_value))
            if v_v < min_heuristic_value:
                min_heuristic_value = v_v 
                vertex_next = v    
        if vertex_next:
            return vertex_next
        else:
            raise ValueError('Некуда двигаться')

#Сканирование вокруг робота на наличие препятствий
def scanning_for_constraints(graph, queue, vertex_current, scan_range, k_m):
    states_to_update = {}
    range_checked = 0
    if scan_range >= 1:
        for neighbor in graph.graph[vertex_current].children:
            neighbor_coords = nameToCoords(neighbor)
            states_to_update[neighbor] = graph.cells[neighbor_coords[1]][neighbor_coords[0]]
        range_checked = 1
    while range_checked < scan_range:
        new_set = {}
        for state in states_to_update:
            new_set[state] = states_to_update[state]
            for neighbor in graph.graph[state].children:
                if neighbor not in new_set:
                    neighbor_coords = nameToCoords(neighbor)
                    new_set[neighbor] = graph.cells[neighbor_coords[1]][neighbor_coords[0]]
        range_checked += 1
        states_to_update = new_set
    new_constraint = False
    for state in states_to_update:
        if states_to_update[state] < 0:  
            for neighbor in graph.graph[state].children:
                if(graph.graph[state].children[neighbor] != float('inf')):
                    neighbor_coords = nameToCoords(state)
                    graph.cells[neighbor_coords[1]][neighbor_coords[0]] = -2
                    graph.graph[neighbor].children[state] = float('inf')
                    graph.graph[state].children[neighbor] = float('inf')
                    calculation_of_cell(graph, queue, state, vertex_current, k_m)
                    new_constraint = True
    return new_constraint

#Движение и проверка на ограничения
def moveAndRescan(graph, queue, vertex_current, scan_range, k_m):
    if(vertex_current == graph.finish):
        return 'finish', k_m
    else:
        vertex_last = vertex_current
        vertex_new = next_step_in_path(graph, vertex_current)
        new_coords = nameToCoords(vertex_new)
        if(graph.cells[new_coords[1]][new_coords[0]] == -1): 
            vertex_new = vertex_current
        results = scanning_for_constraints(graph, queue, vertex_new, scan_range, k_m)
        k_m += heuristic(graph, vertex_last, vertex_new)
        calculation_of_path(graph, queue, vertex_current, k_m)
        return vertex_new, k_m

def initAlgoritm(graph, queue, vertex_start, vertex_finish, k_m):
    graph.graph[vertex_finish].g_aware = 0
    heapq.heappush(queue, calculation_of_element(
        graph, vertex_finish, vertex_start, k_m) + (vertex_finish,))
    calculation_of_path(graph, queue, vertex_start, k_m)
    return (graph, queue, k_m)

