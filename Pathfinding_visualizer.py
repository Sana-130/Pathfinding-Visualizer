import pygame
import math
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from collections import deque
from queue import PriorityQueue
import time
import sys



ROW=50
COLUMN=50

pygame.init()
surface=pygame.display.set_mode((650, 650))
pygame.display.set_caption('Pathfinding Visualizer')
done = False

#colors
BLACK = (0, 0, 0)
WHITE=(255,255,255)
#start and end node
red=(222, 49, 99)
purple=(106, 15, 142)
#other nodes
light_blue=(49, 172, 222)
light_orange=(255, 154, 118)
dark_blue=(51, 54, 255 )


y0=0
x1=20
y1=20
spacing=5
x0=0

y=0
n=20

class Spot:
    def __init__(self, x, y, col, row, width):
        self.x=x
        self.y=y
        self.col=col
        self.row=row
        self.width=width
        self.color = WHITE

    def draw(self):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.width))

    def make_start(self):
        self.color=red

    def make_end(self):
        self.color=purple

    def make_barrier(self):
        self.color=BLACK
        
    def visited_cell(self):
        self.color=dark_blue

    def backtrack(self):
        self.color=light_orange

    def edge_color(self):
        self.color=light_blue

    def reset(self):
        self.color=WHITE


def grid_make(width):
    grid=[]
    y0=0
    n=width
    for j in range(1 ,ROW+1):
        gap=width
        x0=0
        grid.append([])
        for i in range(1, ROW+1):
            spot=Spot(x0, y0,math.trunc(x0/13),math.trunc(y0/13), width)
            x0=gap+i
            gap=gap+width
            grid[j-1].append(spot)
        y0=n+j
        n=n+width
    return grid

def draw(win, grid, row):
    win.fill(BLACK)
    for row in grid:
        for spot in row:
            spot.draw()
            
    pygame.display.flip()

'''this will get us the row and column position because
total width is 650. and number of row and column is 50.
650/50=13 .so you can always adjust the number of column and rows by changing
some values like down here. Always keep in mind, if you want
to change the width and height by some number, then multiply it with 13 and 
give the final value as the window size, because 13 is the default size after 
adding the spacing etc of the cell here.'''

def get_position(x, y):
    col=math.trunc(x/13)
    row=math.trunc(y/13)
    return col, row

def construct_path(curr_node, from_list, start):
    r=curr_node
    for i in range(len(from_list)-1):
        t=from_list[r]
        if t==start:
            break
        else:
            t.backtrack()
            r=t
            
window=Tk()
window.title('tutorial window')
t=Text(window, height=30, width=52)
label=Label(window, text="PathFinding Visualizer Tutorial")
label.config(font=("Courier", 14))

text="""-----------------------------------------
 ? node Info:\n
* Red is the Start node
* Purple is the End node
* Black is the Barrier node
* Dark blue is the already visited node
* Light blue is the currently visiting node
* light Orange is the Path node 
-------------------------------------------
 ? how to mark node:\n
* Right click on the cell to mark the node.
* Left click on the cell to unmark the node.
* The order of nodes are:
  1: Start node
  2: End node
  3: Barrier node
-------------------------------------------
 ? How to visualize algorithms:\n
* Algorithms which are currently implemented:
  1: BFS
  2: Dijakstra
  3: A star
  
  To run-
  BFS       : press 'b'
  Dijkstra  : press 'd'
  A* Search : press 'a'
---------------------------------------------
 ? Additional info:\n
* To clear out the board :Press 'c'
* To clear out only the visualization:
  Press the space bar
---------------------------------------------
"""

t.insert(END, text)

skip_button=Button(window, text="Skip",width=10, command=window.destroy)

label.grid(columnspan=4, row=0)
t.grid(columnspan=4, rowspan=7)
skip_button.grid(column=3, row=1)

window.update()
mainloop()

def message_box():
    Tk().wm_withdraw()
    messagebox.showinfo("error", ('oops!! couldn\'t find a path.\n Maybe it is blocked by barriers. '))
    
def dijkstra(draw, grid, start, end):
    rowNum=[-1, 1,0,0]
    colNum=[0 ,0 ,-1 ,1]
    
    col_1=len(grid[1])
    rows_1=len(grid)
    

                
    def isValid(row, col):
        return (row>=0) and (row<=49) and (col>=0) and (col<=49)
    
    distance={col: sys.maxsize for row in grid for col in row}
    distance[start]=0
    visited_set=[]
    distance2={}
    distance2[start]=0
    from_list={}
    vertex=[]

    
    def get_min_distance(grid, distance, visited):
#        mini=min(distance2, key=distance.get)

#        if mini not in visited and mini.color!=BLACK:
#            mini_index=mini
#        else:
#            print("nop")
#        return mini_index
            
       try:
           min = sys.maxsize
           for u in distance:
               if distance[u] < min and u not in visited and u.color!=BLACK:
                   min = distance[u]
                   min_index = u
           return min_index
       except:
           min_index=False     
           return min_index

    total_cells=col_1 * rows_1
    state=len(visited_set)!=total_cells
    while state:
        
        current=get_min_distance(grid, distance, visited_set)
        if current==False:
            message_box()
            state=False
            return False
            
        visited_set.append(current)
        
        
        if current==end:
            end.make_end()
            construct_path(current, from_list, start)
            break
        
        
            
        if current!=start:
            current.visited_cell()

        for i in range(4):
            row=current.row+ rowNum[i]
            col=current.col+ colNum[i]

            if (isValid(row, col) and grid[row][col].color!=BLACK and grid[row][col] not in visited_set ):
                temp_dist=distance[current] + 1

                if temp_dist <  distance[grid[row][col]]:
                    distance[grid[row][col]]=temp_dist
                    
                    from_list[grid[row][col]]=current
                    grid[row][col].edge_color()
                from_list[grid[row][col]]=current
                grid[row][col].edge_color()
            
            
                time.sleep(0.001)
                draw()
                        
    
    return False



def mh(c1, c2):
    start_x, start_y=c1
    end_x, end_y=c2
    return abs(start_x - end_x)+ abs(start_y-end_y)
    

            
def astar(draw, grid, start, end):
    count=0
    rowNum=[-1, 1, 0, 0]
    colNum=[0 ,0 ,-1 ,1]
    
    open_set=PriorityQueue()
   
    parent={}

    g_score={col: sys.maxsize for row in grid for col in row}
    f_score={col: sys.maxsize for row in grid for col in row}
    g_score[start]=0
    f_score[start]=mh((start.row, start.col),(end.row, end.col))

    open_set.put((0, count, start))
    open_set_hash={start}
    
    def isValid(row, col):
        return (row>=0) and (row<=49) and (col>=0) and (col<=49)
    
    
    while not open_set.empty() :
        q=open_set.get()[2]
        open_set_hash.remove(q)
        
        if q==end:
            end.make_end()
            construct_path(q, parent, start)
            return True
            
        
        for i in range(4):
            
            row=q.row+ rowNum[i]
            col=q.col+ colNum[i]

            
            if (isValid(row, col) and grid[row][col].color!=BLACK ):
                node=grid[row][col]
                temp_g_score=g_score[q]+1
                if temp_g_score<g_score[node]:
                    g_score[node]=temp_g_score
                    parent[node]=q
                    f_score[node]=temp_g_score+ mh((node.row, node.col),(end.row, end.col))

                    if node not in open_set_hash:
                        count+=1
                        open_set.put((f_score[node], count, node))
                        open_set_hash.add(node)
                        node.edge_color()
                        
                    time.sleep(0.005)
                    draw()

            if q!=start:
                q.visited_cell()
                
    
    message_box()
    return False  
    
   
def bfs(draw, grid, start, end):
    
    print(end.row, end.col)
    col=len(grid[1])
    rows=len(grid)
    visited=[[False for i in range(col)] for j in range(rows)]
    visited[start.row][start.col]=True

    queue=deque()
    queue.append(start)

    def isValid(row, col):
        return (row>=0) and (row<=49) and (col>=0) and (col<=49) 

    prev={}
    
    rowNum=[-1, 1,0,0]
    colNum=[0 ,0 ,-1 ,1]
    
    while queue:
                    
        curr=queue.popleft()
        
        if curr!=start :
            curr.visited_cell()
                
            
        if curr==end:
            curr.make_end()
            construct_path(curr, prev, start)
            return True

        else:
            for i in range(4):
                row=curr.row+ rowNum[i]
                col=curr.col+ colNum[i]

                if (isValid(row, col) and grid[row][col].color!=BLACK and not visited[row][col]):
                    node=grid[row][col]
                    queue.append(node) 
                    visited[row][col] =True
                    node.edge_color()
                    prev[node]=curr
                time.sleep(0.001) 
                draw()
    message_box()              
    
    


def leave(draw, grid, start, end):
    if start!=None:
        start.make_start()
    if end!=None:
        end.make_end()
    for row in grid:
        for col in row:
            if col.color ==dark_blue or col.color==light_blue or col.color==light_orange:
                col.color=WHITE
    draw()
             
def main():
    run = True

    start=None
    end=None
    
    grid=grid_make(12)

    while run:
        draw(surface,grid, ROW+1)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
                

            if pygame.mouse.get_pressed()[0]:
                x, y=pygame.mouse.get_pos()
                col, row=get_position(x,y)
                node=grid[row][col]
                if not start and node!=end:
                    start=node
                    start.make_start()
                    
                if not end and node!=start:
                    end=node
                    end.make_end()

                elif node!=start and node!=end:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                x,y=pygame.mouse.get_pos()
                col, row=get_position(x, y)
                node=grid[row][col]
                node.reset()
                if node==start:
                    start=None
                elif node==end:
                    end=None
                    
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_b and start and end:
                
                    bfs(lambda: draw(surface, grid, 51), grid, start, end)

                if event.key==pygame.K_c:
                    start=None
                    end=None
                    grid=grid_make(12)

                if event.key==pygame.K_SPACE:
                     leave(lambda: draw(surface, grid, 51),grid, start, end)
                    
                if event.key==pygame.K_d and start and node:
                    dijkstra(lambda: draw(surface, grid, 51),grid, start, end)
                    
                if event.key==pygame.K_a and start and node:
                    astar(lambda: draw(surface, grid, 51),grid, start, end)
    pygame.quit()
    


if __name__=="__main__":
    main()
   
   
