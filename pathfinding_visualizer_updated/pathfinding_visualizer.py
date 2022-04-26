#from shutil import move
from pickle import TRUE
import pygame
import math
import random
import time
import sys
from queue import PriorityQueue
from collections import deque
from tkinter import *
from tkinter import messagebox

from sqlalchemy import column, false, true

pygame.init()

'''
ROW=18
COLUMN=28
WIDTH=35

surface=pygame.display.set_mode((1008, 648))

'''
WIDTH=35
TOTAL_WIDTH=1200
TOTAL_HEIGHT=600
actual_height=(round(TOTAL_HEIGHT/(WIDTH+1)))*(WIDTH+1)
actual_width=(round(TOTAL_WIDTH/(WIDTH+1)))*(WIDTH+1)
surface=pygame.display.set_mode((actual_width, actual_height))


COLUMN=round(TOTAL_WIDTH/(WIDTH+1))
ROW=round(TOTAL_HEIGHT/(WIDTH+1))


pygame.display.set_caption('Pathfinding Visualizer')

done = False

weighted=False
#colors

start=None

BLACK = (0, 0, 0)
WHITE=(255,255,255)

red=(222, 49, 99)
light_purple=(198, 178, 227)
blue=(49, 172, 222)
light_orange=(255, 154, 118)
sky_blue=(160, 203, 222 )
green=(17, 122, 101 )

#loading images
start_img=pygame.image.load('pathfinding_visualizer_updated\start_img.png')
grass_img=pygame.image.load('pathfinding_visualizer_updated\grass_new.jpg')
barrier=pygame.image.load('pathfinding_visualizer_updated\\barrier_img.png')
end_img=pygame.image.load('pathfinding_visualizer_updated\end_img.png')
#road=pygame.image.load('pathfinding_visualizer_updated\\road.png')
car=pygame.image.load('pathfinding_visualizer_updated\\red-car.png')
road_img=pygame.image.load('pathfinding_visualizer_updated\\road_img.jpg')

#adjusting the size
end_image=pygame.transform.scale(end_img, (WIDTH,WIDTH))
start_image=pygame.transform.scale(start_img, (WIDTH,WIDTH))
grass_image=pygame.transform.scale(grass_img, (WIDTH,WIDTH))
barrier_img=pygame.transform.scale(barrier, (WIDTH,WIDTH))
road=pygame.transform.scale(road_img, (WIDTH,WIDTH))
#road_img=pygame.transform.scale(road, (WIDTH,WIDTH))
red_car_img=pygame.transform.scale(car, (23, 23))


#other variables
y0=0
x1=20
y1=20
x0=0
y=0
n=20

# Spot class - The parent class

class Spot (object):
    def __init__(self, x, y, col, row, width ):
        self.start=false
        self.end=false
        self.is_barrier=false
        self.is_path=false
        self.x=x
        self.y=y
        self.col=col
        self.row=row
        self.width=width
        self.color = WHITE
        self.car=None
        self.is_car=False
        self.car_stop=False

    def draw_rect(self):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.width))
    
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

    def reset_barrier(self):
        self.is_barrier=false

    def draw_barrier(self):
        surface.blit(barrier_img, (self.x, self.y))
        
    def visited_cell(self):
        self.color=sky_blue

    def make_path(self):
        self.is_path=True

    def backtrack(self):
        self.color=light_orange

    def edge_color(self):
        self.color=blue

    def start_reset(self):
        self.start=False

    def end_reset(self):
        self.end=False
    
    def car_draw(self):
        surface.blit(red_car_img, (self.x, self.y))

    def path_color(self):
        self.is_grass= False
        self.color=light_orange

    def reset(self):
        self.color=WHITE


class W_Nodes(Spot):            #Weighted Nodes
    def __init__(self, x ,y , col, row, width, distance ):
        self.distance= distance
        self.is_grass=false

        Spot.__init__(self, x , y, col, row, width)

        self.rect_obj= pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.width))
        self.font=pygame.font.SysFont('Arial', 15)  

    def path_draw(self):
        surface.blit(road, (self.x, self.y))

    def draw_text(self):
        text_surface_object = self.font.render(str(self.distance), True, BLACK)
        text_rect = text_surface_object.get_rect(center=self.rect_obj.center)
        surface.blit(text_surface_object, text_rect)

    def undo_grass(self):
        self.is_grass=False
        self.distance=random.randint(1,5)

    def make_grass(self):
        self.is_grass=True
        self.distance=10

    def green_box(self):
        surface.blit(grass_image, (self.x, self.y))


class NW_Nodes(Spot):               #Not-Weighted-Nodes
    def __init__(self, x, y, col, row, width):
        super().__init__(x, y, col, row, width)


#rotating the car
def blit_rotate_center( image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft=top_left).center)
    surface.blit(rotated_image, new_rect.topleft)

class Car:   
    def __init__(self, x, y, col, row):
        self.x=x
        self.y=y
        self.col=col
        self.row=row
        self.is_move=0
        self.is_rotate=0
        self.angle=270
        self.rotation_vel=3
        self.movement_array=[]
        self.is_draw=None
        self.x_value=1.7
        self.accelerate=0
        self.limit=0
        self.pos=None
        self.state=0
        self.prev_state=-1
        self.direction=[]
        self.prev_move=None
       
        
    def draw(self):
        surface.blit(red_car_img, (self.x+3, self.y+3))
    
    def move(self, n, pos):
        global state

        if self.is_move < n: #30 and 5
            if pos=="x":
                self.x= self.x + self.x_value
            if pos=="y":
                self.y= self.y + self.x_value
            self.is_move +=1
            self.rotate_draw()

        elif (self.is_move == n):        
            self.state=self.state+1
            

    def rotate_draw(self):
        blit_rotate_center(red_car_img, (self.x, self.y), self.angle)

    def rotate(self, limit):
        global state
        
        if self.is_rotate < limit:
            self.angle += self.rotation_vel
            self.is_rotate += 1
            self.rotate_draw()
        elif (self.is_rotate == limit):
            time.sleep(0.003)
            self.state=self.state+1
            
                        

def grid_make(width):           #Non-weighted grid
    w=width+1
    grid=[]
    y0=0
    n=width
    for j in range(1 ,ROW+1):
        gap=width
        x0=0
        grid.append([])     
        for i in range(1, COLUMN+1):
            spot=NW_Nodes(x0, y0,math.trunc(x0/w),math.trunc(y0/w), width)
            x0=gap+i
            gap=gap+width
            grid[j-1].append(spot)
        y0=n+j
        n=n+width
    return grid

def W_grid_make(width): #weighted_grid_make
    w=width+1
    grid=[]
    y0=0
    n=width
    for j in range(1 ,ROW+1):
        gap=width
        x0=0
        grid.append([])     
        for i in range(1, COLUMN+1):
            spot=W_Nodes(x0, y0,math.trunc(x0/w),math.trunc(y0/w), width, random.randint(1, 5))
            x0=gap+i
            gap=gap+width
            grid[j-1].append(spot)
        y0=n+j
        n=n+width
    return grid

#the new updated draw function


def reset_car_var():
    global car
    global path_array

    car=None
    path_array=[]


def on_run(car):
    car.accelerate, car.limit= engine(car.state, car)
    if car.accelerate!=0:
        car.prev_move=0   
        car.move(car.accelerate, car.pos)
            
    if car.limit!=0:
        car.prev_move=1
        car.rotate(car.limit)

def main_run():
    if start!=None and start.car_stop==True:
        start.car.rotate_draw()

    if start!=None and start.is_car==True:
        n=0
        car=start.car
      
        car.rotate_draw()
        on_run(car)

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
            elif spot.is_path == True:
                pass
            else:
                spot.draw_rect()

    time.sleep(0.003)
    main_run()
      
    pygame.display.flip()



def W_draw(win, grid):
    global is_car
    global start 

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
            elif spot.is_path == True:
                pass
                #spot.path_draw()
            else:
                spot.draw_rect()
                spot.draw_text()

   
    main_run()
        

    ''' if car.is_draw==False:
            for i in range(len(car.movement_array)):
                if car.movement_array[i+1]==0:
                    if n>1:
                        car.is_move=0
                        n-=1
                    car.move()
                    #car.rotate_draw()
                    n+=1
                if car.movement_array[i+1]!=0:
                    car.is_draw=False '''
                 
    pygame.display.flip()



window=Tk()
window.title('tutorial window')
t=Text(window, height=30, width=52)
label=Label(window, text="PathFinding Visualizer Tutorial")
label.config(font=("Courier", 14))

text="""-----------------------------------------
 ? node Info:\n
* Red is the Start node
* Purple is the End node
* Cross Box is the Barrier node
* Light blue is the already visited node
* Blue is the currently visiting node
* Black is the Path node , it may contain grass \n at some point
-------------------------------------------
 ? how to mark node:\n
* Right click on the cell to mark the node.
* Left click on for grass cells (for weighted graph)
* The order of nodes are:
  1: Start node
  2: End node
  3: Barrier node
* To unmark:
  1: Barrier nodes - 'x'
  2: Start and end - 's'
  3: grass cells   - 'g'
  4: visualisatiion part -'space bar'
  5: clear everything - 'c'

-------------------------------------------
 ? how to switch between weighted and non weighted \n graph:\n
* press - 'w'
-------------------------------------------
 
 ? How to visualize algorithms:\n
* Algorithms which are currently implemented:
  1: BFS      - Not in weighted graph
  2: Dijakstra
  3: A star
  
  To run-
  BFS       : press 'b'
  Dijkstra  : press 'd'
  A* Search : press 'a'

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

def engine(state, car):

    global is_car
    global car_stop

    x=25
    y=1.45

    down_y=1.5
   

    if state!=car.prev_state:
        if state < len(car.movement_array):
            if car.movement_array[state]==0:
                car.limit=0
                if car.direction[state]==6:  # right
                    car.pos="x"
                    car.x_value=y
                    car.accelerate +=x
                   
                elif car.direction[state]==8: #left
                    car.pos="x"
                    car.x_value=-y
                    car.accelerate +=x
                    
                elif car.direction[state]==2: #up
                    car.pos="y"
                    car.x_value=-y
                    car.accelerate+=x
                   
                elif car.direction[state]==5: #down
                    car.pos="y"
                    car.x_value=down_y
                    car.accelerate+=x
                    
                
             
    
            elif car.movement_array[state]==-4 : #up-right
                car.accelerate=0
                car.rotation_vel=-3 
                car.limit+=30
         
            elif car.movement_array[state]==-6 :#up-left
                car.accelerate=0
                car.rotation_vel= 3
                car.limit+=30 #up-left
                pass
            elif car.movement_array[state]==-1 :#down-right
                #car.y+=5
                car.accelerate=0
                car.rotation_vel= 3
                car.limit+=30

            elif car.movement_array[state]==-3 : #down-left
                #car.y+=5
                car.accelerate=0
                car.rotation_vel=-3
                car.limit+=30

            elif car.movement_array[state]== 4:#right-up
                #car.x+=5
                car.accelerate=0
                car.rotation_vel=3
                car.limit+=30

            elif car.movement_array[state]== 1 : #right-down
                #car.x+=5
                car.accelerate=0
                car.rotation_vel=-3
                car.limit+=30

            elif car.movement_array[state]== 6:  #left-up
                #car.x-=5
                car.accelerate=0
                car.rotation_vel= -3
                car.limit+=30

            elif car.movement_array[state]== 3 :#left-down
                #car.x-=5
                car.accelerate=0
                car.rotation_vel=3
                car.limit+=30

            car.prev_state+=1
            if car.accelerate!=0:
                if car.prev_move==1:
                    car.is_move=0
            if car.limit!=0:
                if car.prev_move==0:
                    car.is_rotate=0


            return car.accelerate, car.limit
        else:
            car.prev_state+=1
            start.is_car=False
            start.car_stop=True
            car.accelerate=0
            car.limit=0
    
            return car.accelerate, car.limit
    else:
        return car.accelerate, car.limit
    
'''this will get us the row and column position because
total width is 650. and number of row and column is 50.
650/50=13 .so you can always adjust the number of column and rows by changing
some values like down here. Always keep in mind, if you want
to change the width and height by some number, then multiply it with 13 and 
give the final value as the window size, because 13 is the default size after 
adding the spacing etc of the cell here.'''

def get_position(x, y):   
    col=math.trunc(x/(WIDTH+1))
    row=math.trunc(y/(WIDTH+1))
    return col, row

def detect_pos(x1, y1, x2, y2):
    col_diff= x1-x2
    row_diff= y1-y2
    direct=0
    if col_diff==-1:
        direct= 6    #right
    if col_diff == 1:
        direct= 8    #left
    if row_diff == -1:
        direct= 5    #down
    if row_diff == 1:
        direct= 2    #up
 
    return direct

def detect_direct(prev_elem):
    m=None
    d=None
    if prev_elem == -4: #and prev_elem==1 or prev_elem==4:
        m=0
        d=6
    if prev_elem == -6: #and prev_elem==6 or prev_elem==3:
        m=0
        d=8
    if prev_elem == -1 :#and prev_elem==4 or prev_elem==1:
        m=0
        d=6
    if prev_elem== -3: #and prev_elem==6 or prev_elem==3:
        m=0
        d=8
    if prev_elem == 4 :#and prev_elem==-4 or prev_elem==-6:
        m=0
        d=2
    if prev_elem == 1 : #and prev_elem==-3 or prev_elem==-1:
        m=0
        d=5
    if prev_elem == 6 :#and prev_elem==-4 or prev_elem==-6:
        m=0
        d=2
    if prev_elem == 3 :#and prev_elem==-1 or prev_elem==-3: 
        m=0
        d=5

    return m, d

def check_start(list_m):
    run=False
    for i in range(len(list_m)):
        if list_m[i]!=0:
            run=True
            break
    return run      



def car_move(path_array, first):

    new_direct=[]

    n=len(path_array)-1
    new_direct.append(detect_pos(first.col, first.row, path_array[-1].col , path_array[-1].row))
    for i in range(n+1):
        
        direct=detect_pos(path_array[n-i].col, path_array[n-i].row, path_array[n-i-1].col, path_array[n-i-1].row)
        new_direct.append(direct)
    new_direct[-1]=detect_pos(path_array[1].col, path_array[1].row, path_array[0].col, path_array[0].row)
    #print("end", path_array[0].row, path_array[0].col)
    start=path_array[-1]
    
    
    first.car = Car(start.x, start.y , start.col, start.row)
    
    if new_direct[0]== 5: #down
        first.car.angle=270
    if new_direct[0]== 2: #up
        first.car.angle=90
    if new_direct[0]== 6: #right
        first.car.angle=360
    if new_direct[0]== 8: #left
        first.car.angle=180

    prev_elem=None
    rotate_elems=[-4, -6, -1, -3, 4, 1, 6, 3]

    for i in range(len(new_direct)):
        first.car.direction.append(new_direct[i])

   

    ''' when the car is rotating, it is staying on one cell so the calculation we are doing necessarily dont
    add an acceleration between two adjacent roatations which will mess up the movement ,so for that, in the below 
    function it will loop through the movement array and look for two adjacent rotations by keeping track of 
    the variable called "prev_elem" , when the prev_elem is not zero , which is in case like [3, -3] , it will
    add a 0 in between , now the direction array should also be changed accordingly , which is to add the
    corresponding direction in the specified index which the function "detect_direct" will do. Now the second 
    case to consider here is when the previous element is in fact 0, well this may seems to not to be changed 
    but we have to add an additional zero to it to make up the correct acceleration. But there is one condition,
    if the array already starts with 0 and followes up to some rotation , for eg: [0,0,-3], in this case 0 
    should not be added , because the 0 is already added (look at the above calculation of direction array ),
    "check_start" function will detect this  '''
    
    for i in range(len(new_direct)-1):
        r=new_direct[i]- new_direct[i+1]
        if r in rotate_elems and prev_elem!=0 and prev_elem!=None:

            movement_elem, direction_elem=detect_direct(prev_elem)
            first.car.movement_array.append(movement_elem)  
            first.car.direction.insert(len(first.car.movement_array), direction_elem)
            #direction[len(car.movement_array)]=direction_elem
            #print(direction, new_direct, len(car.movement_array) , len(direction))
            first.car.movement_array.append(r)
            prev_elem=r

        elif r in rotate_elems and prev_elem==0 and len(first.car.movement_array)!=1:
            #print("-----------------", direction[len(car.movement_array)], len(car.movement_array))
            q=check_start(first.car.movement_array)
            if q==True:
                first.car.movement_array.append(0)
                first.car.direction.insert(len(first.car.movement_array), first.car.direction[len(first.car.movement_array)-1])
                first.car.movement_array.append(r)
                prev_elem=r
            else:
                first.car.movement_array.append(r)
                prev_elem=r
        else:
            first.car.movement_array.append(r)
            prev_elem=r

    #if len(direction)!=len(car.movement_array):
    #    direction.append(8)
    #print("new direct", new_direct , "direction", direction,  "angle", car.angle, "length", len(direction), len(car.movement_array))
   
    
    first.is_car=True
    

path_array=[]
#updated contruct path function (colouring grass cell the path color)
def construct_path(curr_node, from_list, start):
    global is_car
    global path_array
    
    r=curr_node
    for i in range(len(from_list)-1):
        t=from_list[r]
        if t==start:
            #is_car=True
            car_move(path_array, start)
            break
        else:
            t.is_path=True
            path_array.append(t)

            r=t 
    
    
    
    
# in the updated function below, we are determining if a cell is barrier or not by checking one of 
# its object property "is_barrier", rather than checking the color.

def dijkstra(draw, grid, start, end):
    rowNum=[-1, 1,0,0]
    colNum=[0 ,0 ,-1 ,1]
    
    col_1=len(grid[1])
    rows_1=len(grid)


    def isValid(row, col):
        return (row>=0) and (row<=ROW-1) and (col>=0) and (col<=COLUMN-1)
    
    distance={col: sys.maxsize for row in grid for col in row}
    distance[start]=0
    visited_set=[]
    from_list={}
    
    
    def get_min_distance(distance, visited):            
       try:
           min = sys.maxsize
           for u in distance:
               if distance[u] < min and u not in visited and u.is_barrier==false:
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
            
            
                time.sleep(0.003)
                draw()
                        
    
    return False


def weighted_dijkstra(draw, grid, start, end):
    rowNum=[-1, 1,0,0]
    colNum=[0 ,0 ,-1 ,1]
    
    col_1=len(grid[1])
    rows_1=len(grid)
    

                
    def isValid(row, col):
        return (row>=0) and (row<=ROW-1) and (col>=0) and (col<=COLUMN-1)
    
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
            message_box()
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
        return (row>=0) and (row<=ROW-1) and (col>=0) and (col<=COLUMN-1)
    
    
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

            
            if (isValid(row, col) and grid[row][col].is_barrier==false ):
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
                        
                    time.sleep(0.009)
                    draw()

            if q!=start:
                q.visited_cell()
                
    
    message_box()
    return False  


def weighted_mh(c1, c2):
    start_x, start_y, dist=c1
    end_x, end_y=c2
    return abs(start_x - end_x)+ abs(start_y-end_y) + dist

def weighted_astar(draw, grid, start, end):
    count=0
    rowNum=[-1, 1, 0, 0]
    colNum=[0 ,0 ,-1 ,1]
    
    open_set=PriorityQueue()
   
    parent={}

    g_score={col: sys.maxsize for row in grid for col in row}
    f_score={col: sys.maxsize for row in grid for col in row}
    g_score[start]=0
    f_score[start]=weighted_mh((start.row, start.col, start.distance),(end.row, end.col))

    open_set.put((0, count, start))
    open_set_hash={start}
    
    def isValid(row, col):
        return (row>=0) and (row<=ROW-1) and (col>=0) and (col<=COLUMN-1)
    
    
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

            
            if (isValid(row, col) and grid[row][col].is_barrier==false):
                node=grid[row][col]
                temp_g_score=g_score[q]+1
                if temp_g_score<g_score[node]:
                    g_score[node]=temp_g_score
                    parent[node]=q
                    f_score[node]=temp_g_score+ weighted_mh((node.row, node.col, node.distance),(end.row, end.col))

                    if node not in open_set_hash:
                        count+=1
                        open_set.put((f_score[node], count, node))
                        open_set_hash.add(node)
                        node.edge_color()

                        
                    time.sleep(0.02)
                    draw()

            if q!=start:
                q.visited_cell()
                
    message_box()
    return False  

def bfs(draw, grid, start, end):
    
    col=len(grid[1])
    rows=len(grid)
    visited=[[False for i in range(col)] for j in range(rows)]
    visited[start.row][start.col]=True

    queue=deque()
    queue.append(start)

    def isValid(row, col):
        return (row>=0) and (row<=ROW-1) and (col>=0) and (col<=COLUMN-1) 

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

                if (isValid(row, col) and grid[row][col].is_barrier==false and not visited[row][col]):
                    node=grid[row][col]
                    queue.append(node) 
                    visited[row][col] =True
                    node.edge_color()
                    prev[node]=curr
                time.sleep(0.001) 
                draw()
    message_box() 

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

def search_clear(grid):
    for row in grid:
        for col in row:
            if col.color ==sky_blue or col.color==blue or col.color==light_orange:
                col.reset()

def car_reset(grid):
    global car_stop
    start.car_stop=False
    reset_car_var()
    for row in grid:
        for col in row:
            if col.is_path==True:
                col.is_path=False

def reboot(grid, end):
    global start

    if start!=None and end!=None:
        start.start_reset()
        end.end_reset()
        car_reset(grid)

    if weighted:
        grass_reset(grid)

    reset_barrier(grid)
    search_clear(grid)
    


def main():
    global start
    global weighted
    run = True

    if weighted:
        grid=W_grid_make(WIDTH)
    else:
        grid=grid_make(WIDTH)

    end=None
  
    while run:
        if weighted:
            W_draw(surface,grid)
        else:
            draw(surface, grid)

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
                if weighted:
                    x,y=pygame.mouse.get_pos()
                    col, row=get_position(x, y)
                    node=grid[row][col]
                    if node!=start and node!=end:  
                        node.make_grass()
                        
            if event.type==pygame.KEYDOWN:

                #start and end node reset
                if event.key==pygame.K_s and start and end:
                    start.start_reset()
                    end.end_reset()
                    start=None
                    end=None

                #clearing out the barriers
                if event.key==pygame.K_x :
                    reset_barrier(grid)

                #clearing out the grass cells
                if event.key==pygame.K_g:
                    if weighted:
                        grass_reset(grid)

                #clearing out everything
                if event.key==pygame.K_c :              
                    reboot(grid, end)
                    if start!=None and end!=None:
                        start=None
                        end=None

                #switching between weighted and non-weighted
                if event.key==pygame.K_w:
                    start=None
                    end=None
                    if weighted:
                        
                        reboot(grid, end)
                        weighted=False
                        grid=grid_make(WIDTH)
   
                    else:
                        
                        reboot(grid, end)
                        grid=W_grid_make(WIDTH)
                        weighted=true

                #bfs
                if event.key==pygame.K_b and start and end:
                    if not weighted:
                        bfs(lambda: draw(surface, grid),grid, start, end)

                #dijkstra
                if event.key==pygame.K_d and start and end:
                    if weighted: 
                        weighted_dijkstra(lambda: W_draw(surface, grid),grid, start, end)
                    else:
                        dijkstra(lambda: draw(surface, grid),grid, start, end)
                    
                #astar algorithm
                if event.key==pygame.K_a and start and end:
                    if weighted:
                        weighted_astar(lambda: W_draw(surface, grid), grid, start, end)
                    else:
                        astar(lambda: draw(surface, grid), grid, start, end)

                #clearing out the visualisation part
                if event.key==pygame.K_SPACE:
                     visua_reset(grid, start, end)
                    
        
    pygame.quit()


if __name__=="__main__":
    main()
   
