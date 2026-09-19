from pyamaze import maze , textLabel , COLOR , agent
def BFS(m):
    start = (m.rows , m.cols)
    frontlier = [start]
    explored = [start]
    bfsPath = {}
    while len(frontlier) > 0:
        currCell = frontlier.pop(0)
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
                if childCell in explored:
                    continue
                frontlier.append(childCell)
                explored.append(childCell)
                bfsPath[childCell] = currCell
    fwdPath = {}
    cell = (1,1)
    while cell != start:
        fwdPath[bfsPath[cell]] = cell
        cell = bfsPath[cell]
    return bfsPath, fwdPath
if __name__ == "__main__":
    m = maze(5,5)
    m.CreateMaze(loopPercent=100)
    bfsPath, fwdPath = BFS(m)
    a = agent(m , footprints=True, color=COLOR.yellow, shape='square', filled=True)
    m.tracePath({a: fwdPath})
    l = textLabel(m, 'BFS Path Length', len(fwdPath)+1)
    m.run()

