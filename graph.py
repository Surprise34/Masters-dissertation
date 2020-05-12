class Node:
    def __init__(self, id):
        self.id = id
        self.parents = {}
        self.children = {}
        self.g = float('inf')
        self.g_aware = float('inf')

class Graph:
    def __init__(self):
        self.graph = {}
        
    def setStart(self, id):
        if(self.graph[id]):
            self.start = id
        else:
            raise ValueError('start id not in graph')

    def setFinish(self, id):
        if(self.graph[id]):
            self.finish = id
        else:
            raise ValueError('finish id not in graph')

class Grid(Graph):
    def __init__(self, x_dim, y_dim):
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.cells = [0] * y_dim
        for i in range(y_dim):
            self.cells[i] = [0] * x_dim
        self.graph = {}
        self.generateGraphFromGrid()
    
    # У каждой клетки 4 соседа
    '''
    def generateGraphFromGrid(self):
        edge = 1
        for i in range(len(self.cells)):
            row = self.cells[i]
            for j in range(len(row)):
                # print('graph node ' + str(i) + ',' + str(j))
                node = Node('x' + str(i) + 'y' + str(j))
                if i > 0:  
                    node.parents['x' + str(i - 1) + 'y' + str(j)] = edge
                    node.children['x' + str(i - 1) + 'y' + str(j)] = edge
                if i + 1 < self.y_dim: 
                    node.parents['x' + str(i + 1) + 'y' + str(j)] = edge
                    node.children['x' + str(i + 1) + 'y' + str(j)] = edge
                if j > 0:  
                    node.parents['x' + str(i) + 'y' + str(j - 1)] = edge
                    node.children['x' + str(i) + 'y' + str(j - 1)] = edge
                if j + 1 < self.x_dim:
                    node.parents['x' + str(i) + 'y' + str(j + 1)] = edge
                    node.children['x' + str(i) + 'y' + str(j + 1)] = edge
                self.graph['x' + str(i) + 'y' + str(j)] = node
    '''

    '''
    i=@|012|
    ________
    j=0|000|
    j=1|000|
    j=2|000|
    '''

    # У каждой клетки 8 соседей
    def generateGraphFromGrid(self):
        edge = 1
        for i in range(len(self.cells)):
            row = self.cells[i]
            for j in range(len(row)):
                # print('graph node ' + str(i) + ',' + str(j))
                node = Node('x' + str(i) + 'y' + str(j))
                if i > 0:  
                    node.parents['x' + str(i - 1) + 'y' + str(j)] = edge
                    node.children['x' + str(i - 1) + 'y' + str(j)] = edge
                    if j > 0:
                        node.parents['x' + str(i - 1) + 'y' + str(j - 1)] = edge
                        node.children['x' + str(i - 1) + 'y' + str(j - 1)] = edge
                if i + 1 < self.y_dim: 
                    node.parents['x' + str(i + 1) + 'y' + str(j)] = edge
                    node.children['x' + str(i + 1) + 'y' + str(j)] = edge
                    if j + 1 < self.x_dim:
                        node.parents['x' + str(i + 1) + 'y' + str(j + 1)] = edge
                        node.children['x' + str(i + 1) + 'y' + str(j + 1)] = edge                        
                if j > 0:  
                    node.parents['x' + str(i) + 'y' + str(j - 1)] = edge
                    node.children['x' + str(i) + 'y' + str(j - 1)] = edge
                    if i + 1 < self.y_dim:
                        node.parents['x' + str(i + 1) + 'y' + str(j - 1)] = edge
                        node.children['x' + str(i + 1) + 'y' + str(j - 1)] = edge                        
                if j + 1 < self.x_dim:
                    node.parents['x' + str(i) + 'y' + str(j + 1)] = edge
                    node.children['x' + str(i) + 'y' + str(j + 1)] = edge
                    if i > 0:
                        node.parents['x' + str(i - 1) + 'y' + str(j + 1)] = edge
                        node.children['x' + str(i - 1) + 'y' + str(j + 1)] = edge                        
                self.graph['x' + str(i) + 'y' + str(j)] = node
    
