import pygame
import math

import random
import time
import sys



ROW=25
COLUMN=25
WIDTH=25

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

x0=0

y=0
n=20

class Spot:
    def __init__(self, x, y, col, row, width, distance):
        self.x=x
        self.y=y
        self.col=col
        self.row=row
        self.width=width
        self.color = WHITE
        self.distance=distance
        self.rect_obj=pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.width))
        

    def draw_rect(self):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.width))

    def draw_text(self):
        
        text_surface_object = pygame.font.SysFont('Arial', 15).render(str(self.distance), True, (255,0,0))
        text_rect = text_surface_object.get_rect(center=self.rect_obj.center)
        surface.blit(text_surface_object, text_rect)

    def make_start(self):
        self.color=red

    def make_end(self):
        self.color=purple

        
    def visited_cell(self):
        self.color=dark_blue

    def backtrack(self):
        self.color=light_orange

    def edge_color(self):
        self.color=light_blue

    def reset(self):
        self.color=WHITE


def grid_make(width):
    w=width+1
    grid=[]
    y0=0
    n=width
    for j in range(1 ,ROW+1):
        gap=width
        x0=0
        grid.append([])
        for i in range(1, ROW+1):
            spot=Spot(x0, y0,math.trunc(x0/w),math.trunc(y0/w), width, random.randint(1, 5))
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
            spot.draw_rect()
            spot.draw_text()            
    pygame.display.flip()

'''this will get us the row and column position because
total width is 650. and number of row and column is 50.
650/50=13 .so you can always adjust the number of column and rows by changing
some values like down here. Always keep in mind, if you want
to change the width and height by some number, then multiply it with 13 and 
give the final value as the window size, because 13 is the default size after 
adding the spacing etc of the cell here.'''

def get_position(x, y):
    w=WIDTH+1
    col=math.trunc(x/w)
    row=math.trunc(y/w)
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

def dijkstra(draw, grid, start, end):
    rowNum=[-1, 1,0,0]
    colNum=[0 ,0 ,-1 ,1]
    
    col_1=len(grid[1])
    rows_1=len(grid)
    

                
    def isValid(row, col):
        return (row>=0) and (row<=ROW-1) and (col>=0) and (col<=ROW-1)
    
    distance={col: sys.maxsize for row in grid for col in row}
    
    #distance2={col: random.randint(1, 20) for row in grid for col in row }
    distance[start]=0
    grid[0][0].distance=0
    visited_set=[]
    
    from_list={}
    

    
    def get_min_distance(grid, distance, visited):
            
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
        #print(current.distance, current.row, current.col)
        
        if current==False:
            state=False
            return False
            
        visited_set.append(current)
        
        
        if current==end:
            end.make_end()
            construct_path(current, from_list, start)
            break
    

        for i in range(4):
            row=current.row+ rowNum[i]
            col=current.col+ colNum[i]

            if (isValid(row, col) and grid[row][col].color!=BLACK and grid[row][col] not in visited_set ):
                temp_dist=distance[current] + grid[row][col].distance

                if temp_dist <  distance[grid[row][col]]:
                    distance[grid[row][col]]=temp_dist
                    from_list[grid[row][col]]=current
                    grid[row][col].edge_color()
                
                #from_list[grid[row][col]]=current
                grid[row][col].edge_color()
            
            
                time.sleep(0.001)
                draw()
                
        if current!=start:
            current.visited_cell()
            
    
    return False
def main():
    run = True

    
    grid=grid_make(WIDTH)

    start=grid[0][0]
    end=grid[5][5]

    while run:
        draw(surface,grid, ROW+1)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
                
                    
            if event.type==pygame.KEYDOWN:


                if event.key==pygame.K_c:
                    start=None
                    end=None
                    grid=grid_make(12)

                if event.key==pygame.K_SPACE:
                     leave(lambda: draw(surface, grid, 51),grid, start, end)
                    
                if event.key==pygame.K_d and start:
                    dijkstra(lambda: draw(surface, grid, 51),grid, start, end)
                    
        
    pygame.quit()
    



if __name__=="__main__":
    main()
   
