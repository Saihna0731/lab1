from queue import PriorityQueue

from pyamaze import COLOR, maze , agent , textLabel
def h(cell1 , cell2):
    x1 , y1 = cell1
    x2 , y2 = cell2
    
    return abs(x1-x2) + abs(y1-y2)

def AStar(m):
    start = (m.rows , m.cols)
    g_score = {cell: float('inf') for cell in m.grid}
    g_score[start] = 0
    f_score = {cell: float('inf') for cell in m.grid}
    f_score[start] = h(start, (1,1))
    
    aPath = {}
    open = PriorityQueue()
    open.put((h(start , (1,1)) , h(start , (1,1)) , start))
    
    while not open.empty():
        currCell = open.get()[2]
        if currCell == (1,1):
            break
        for d in 'ESNW':
            if m.maze_map[currCell][d] == True:
                if d == 'E':
                    childCell = (currCell[0], currCell[1]+1)
                elif d == 'W':
                    childCell = (currCell[0], currCell[1]-1)
                elif d == 'N':
                    childCell = (currCell[0]-1, currCell[1])   
                elif d == 'S':
                    childCell = (currCell[0]+1, currCell[1])  
                temp_g_score = g_score[currCell] + 1
                if temp_g_score < g_score[childCell]:
                    g_score[childCell] = temp_g_score
                    f_score[childCell] = temp_g_score + h(childCell , (1,1))
                    open.put((f_score[childCell] , h(childCell , (1,1)) , childCell))
                    aPath[childCell] = currCell
    fwdPath={}
    cell = (1,1)
    while cell != start:
        fwdPath[aPath[cell]] = cell
        cell = aPath[cell]
    return  fwdPath

if __name__ == "__main__":
    m=maze(10,10)
    m.CreateMaze()
    path = AStar(m)
    
    a = agent(m , footprints=True, color=COLOR.yellow, shape='square', filled=True)
    m.tracePath({a:path})
    l=textLabel(m,'A* Path Length',len(path)+1)

    m.run()