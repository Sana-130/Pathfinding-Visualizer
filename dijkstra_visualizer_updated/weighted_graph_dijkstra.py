import pygame
import math
import random
import time
import sys

from sqlalchemy import false, true


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

red=(222, 49, 99)
light_purple=(198, 178, 227)
blue=(49, 172, 222)
light_orange=(255, 154, 118)
sky_blue=(160, 203, 222 )
green=(17, 122, 101 )

#loading images
start_img=pygame.image.load('start_img.png')
grass_img=pygame.image.load('grass_new.jpg')
barrier=pygame.image.load('barrier_img.png')
end_img=pygame.image.load('end_img.png')

#adjusting the size
end_image=pygame.transform.scale(end_img, (25,25))
start_image=pygame.transform.scale(start_img, (25,25))
grass_image=pygame.transform.scale(grass_img, (25, 25))
barrier_img=pygame.transform.scale(barrier, (25, 25))
#surface.blit(red_flag, (0,0))
#other variables
y0=0
x1=20
y1=20
x0=0
y=0
n=20

# Spot class
# updated spot class contain new object propert's such as start, end, is_grass, is_barrier and 
# their corresponding functions 
class Spot:
    def __init__(self, x, y, col, row, width, distance):
        self.start=false
        self.end=false
        self.is_grass=false
        self.is_barrier=false
        self.x=x
        self.y=y
        self.col=col
        self.row=row
        self.width=width
        self.color = WHITE
        self.distance=distance
        self.rect_obj=pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.width))
        self.font=pygame.font.SysFont('Arial', 15)
        

    def draw_rect(self):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.width))

    def draw_text(self): 
        text_surface_object = self.font.render(str(self.distance), True, BLACK)
        text_rect = text_surface_object.get_rect(center=self.rect_obj.center)
        surface.blit(text_surface_object, text_rect)

    def undo_grass(self):
        self.is_grass=False
        self.distance=random.randint(1, 5)

    def make_grass(self):
        self.is_grass=True
        self.distance=10
    
    def make_start(self):
        self.start=True

    def make_end(self):
        self.end=True
        
    def make_barrier(self):
        self.is_barrier=True

    def draw_start(self):
        surface.blit(start_image, (self.x, self.y))

    def draw_end(self):
        surface.blit(end_image, (self.x, self.y))

    def green_box(self):
        surface.blit(grass_image, (self.x, self.y))

    def reset_barrier(self):
        self.is_barrier=false

    def draw_barrier(self):
        surface.blit(barrier_img, (self.x, self.y))
        
    def visited_cell(self):
        self.color=sky_blue

    def backtrack(self):
        self.color=light_orange

    def edge_color(self):
        self.color=blue

    def start_reset(self):
        self.start=False

    def end_reset(self):
        self.end=False
    
    # if there is any grass cell in the resolved path it would be ideal to color them
    # the path color to avoid confusion.
    def path_color(self):
        self.is_grass= False
        self.color=light_orange

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

#the new updated draw function
def draw(win, grid):
    win.fill(BLACK)
    for row in grid:
        for spot in row:
            if spot.start == True:
                spot.draw_start()
            elif spot.is_barrier == True:
                spot.draw_barrier()
            elif spot.end == True:
                spot.draw_end()
            elif spot.is_grass == True:
                spot.green_box()
            else:
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
    col=math.trunc(x/26)
    row=math.trunc(y/26)
    return col, row

#updated contruct path function (colouring grass cell the path color)
def construct_path(curr_node, from_list, start):
    r=curr_node
    for i in range(len(from_list)-1):
        t=from_list[r]
        if t==start:
            break
        else:
            if t.is_grass== True:
                t.path_color()
            else:
                t.backtrack()
            r=t

# in the updated function below, we are determining if a cell is barrier or not by checking one of 
# its object property "is_barrier", rather than checking the color.

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
    visited_set=[]
    from_list={}
 
    def get_min_distance(distance, visited):
            
       try:
           min = sys.maxsize
           for u in distance:
               if distance[u] < min and u not in visited and u.is_barrier==false:#u.color!=BLACK:
                   min = distance[u]
                   min_index = u
           return min_index
       except:
           min_index=False     
           return min_index

    total_cells=col_1 * rows_1
    state=len(visited_set)!=total_cells
    while state:
        
        current=get_min_distance(distance, visited_set)
        
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

            if (isValid(row, col) and grid[row][col].is_barrier==false and grid[row][col] not in visited_set ):
                temp_dist=distance[current] + grid[row][col].distance

                if temp_dist <  distance[grid[row][col]]:
                    distance[grid[row][col]]=temp_dist
                    from_list[grid[row][col]]=current
                    if grid[row][col].color!=green:
                        grid[row][col].edge_color()

                #from_list[grid[row][col]]=current
                #grid[row][col].edge_color()
            
            
                time.sleep(0.003)
                draw()
                
        if current!=start and current.color!=green:
            current.visited_cell()
    
    return False

#barrier reset
def reset_barrier(grid):
    for row in grid:
        for col in row:
            if col.is_barrier==True:
                col.reset_barrier()
#grass reset
def grass_reset(grid):
    for row in grid:
        for col in row:
            if col.is_grass== True:
                col.undo_grass()
#all clear

def all_clear(grid, start, end):
    if (start!=None and end!=None):
        start.start_reset()
        end.end_reset()
        start=None
        end=None
                    
    grass_reset(grid)
    reset_barrier(grid)
    visua_reset(grid, start, end)


#visualisation reset
def visua_reset( grid, start, end):
    if start!=None:
        start.make_start()
    if end!=None:
        end.make_end()
    for row in grid:
        for col in row:
            if col.color ==sky_blue or col.color==blue or col.color==light_orange:
                col.reset()
  
                
def main():
    run = True
    grid=grid_make(WIDTH)
    start=None
    end=None
  
    while run:
        draw(surface,grid )
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False

            #marking start node, end node and barreirs  
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
                    
            # marking the grass cells
            elif pygame.mouse.get_pressed()[2]:
                x,y=pygame.mouse.get_pos()
                col, row=get_position(x, y)
                node=grid[row][col]
                node.make_grass()
                        
            if event.type==pygame.KEYDOWN:

                #start and end node reset
                if event.key==pygame.K_s and start and end:
                    start.start_reset()
                    end.end_reset()
                    start=None
                    end=None

                #clearing out the barriers
                if event.key==pygame.K_b :
                    reset_barrier(grid)

                #clearing out the grass cells
                if event.key==pygame.K_g:
                    grass_reset(grid)

                if event.key==pygame.K_c:
                    if (start!=None and end!=None):
                        start.start_reset()
                        end.end_reset()
                        start=None
                        end=None
                    
                    grass_reset(grid)
                    reset_barrier(grid)
                    visua_reset(grid, start, end)
                
                if event.key==pygame.K_d and start and end:
                    print(start, end)
                    dijkstra(lambda: draw(surface, grid),grid, start, end)

                #clearing out the visualisation part
                if event.key==pygame.K_SPACE:
                     visua_reset(grid, start, end)
                    
        
    pygame.quit()


if __name__=="__main__":
    main()
   
