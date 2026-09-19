import sys

from pyamaze import COLOR, agent, maze


def DFS(m):
    start = (m.rows , m.cols)
    explored = [start]
    frontlier = [start]
    searchPath = [start]
    dfsPath = {} 
    while len(frontlier) > 0:
        currCell = frontlier.pop()
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
                dfsPath[childCell] = currCell
                searchPath.append(childCell)

    fwdPath = {}
    cell = (1,1)
    while cell != start:
        fwdPath[dfsPath[cell]] = cell
        cell = dfsPath[cell]

    return searchPath, dfsPath, fwdPath


m = maze(5,5)
m.CreateMaze(loopPercent=30)
searchPath, dfsPath, fwdPath = DFS(m)

a = agent(m, footprints=True, color=COLOR.yellow, shape='square', filled=True)
b = agent(m, 1, 1, footprints=True, color=COLOR.red, goal=(m.rows, m.cols))
c = agent(m, footprints=True, color=COLOR.cyan)

m.tracePath({a: searchPath}, delay=50)
m.tracePath({b: dfsPath}, delay=50)
m.tracePath({c: fwdPath}, delay=100)

m.run()