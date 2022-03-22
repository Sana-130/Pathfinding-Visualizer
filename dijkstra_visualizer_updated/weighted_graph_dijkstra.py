#from shutil import move
import pygame
import math
import random
import time
import sys

from sqlalchemy import false, true


ROW=18
COLUMN=18
WIDTH=35

pygame.init()
surface=pygame.display.set_mode((648, 648))
pygame.display.set_caption('Pathfinding Visualizer')
done = False

#colors
is_car=False
car_stop=False
car=None
BLACK = (0, 0, 0)
WHITE=(255,255,255)

red=(222, 49, 99)
light_purple=(198, 178, 227)
blue=(49, 172, 222)
light_orange=(255, 154, 118)
sky_blue=(160, 203, 222 )
green=(17, 122, 101 )

#loading images
start_img=pygame.image.load('dijkstra_visualizer_updated\start_img.png')
grass_img=pygame.image.load('dijkstra_visualizer_updated\grass_new.jpg')
barrier=pygame.image.load('dijkstra_visualizer_updated\\barrier_img.png')
end_img=pygame.image.load('dijkstra_visualizer_updated\end_img.png')
#road=pygame.image.load('dijkstra_visualizer_updated\\road.png')
car=pygame.image.load('dijkstra_visualizer_updated\\red-car.png')

#adjusting the size
end_image=pygame.transform.scale(end_img, (WIDTH,WIDTH))
start_image=pygame.transform.scale(start_img, (WIDTH,WIDTH))
grass_image=pygame.transform.scale(grass_img, (WIDTH,WIDTH))
barrier_img=pygame.transform.scale(barrier, (WIDTH,WIDTH))
#road_img=pygame.transform.scale(road, (WIDTH,WIDTH))
red_car_img=pygame.transform.scale(car, (23, 23))
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
        self.is_path=false
        self.is_blit=false
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

    def make_path(self):
        self.is_path=True

    def draw_border(self):
        self.color=BLACK
        self.draw_rect()

    def backtrack(self):
        self.color=light_orange

    def edge_color(self):
        self.color=blue

    def start_reset(self):
        self.start=False

    def end_reset(self):
        self.end=False
    
    def car_draw(self):
        #self.is_path=False
        #self.color=BLACK
        surface.blit(red_car_img, (self.x, self.y))
    # if there is any grass cell in the resolved path it would be ideal to color them
    # the path color to avoid confusion.
    def path_color(self):
        self.is_grass= False
        self.color=light_orange

    def reset(self):
        self.color=WHITE


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
        self.finished=False
        self.angle=270
        self.rotation_vel=3
        self.movement_array=[]
        self.called=3
        self.is_draw=None
        self.x_value=1.7
        
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
            state=state+1
            
            #func()

    #def rotate(self, left=False, right=False):
    #    if left:
    #        self.angle += self.rotation_vel
    #    elif right:
    #        self.angle -= self.rotation_vel

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
            state=state+1
            
    #def movement(self):

       
    
    def done(self):
        pass

    pass


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
accelarate=0
limit=0
pos=None
state=0
prev_state=-1
direction=[]
#new_direct=[]
prev_move=None

def reset_car_var():
    global car
    global accelarate
    global limit
    global pos
    global state
    global prev_state
    global direction
    global prev_move
    global path_array

    car=None
    accelarate=0
    limit=0
    pos=None
    state=0
    prev_state=-1
    direction=[]
    #new_direct=[]
    prev_move=None
    path_array=[]

def draw(win, grid):
    global is_car
    global state
    global prev_move

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
            else:
                spot.draw_rect()
                spot.draw_text()
    
    if car_stop==True:
        car.rotate_draw()            
    
    if is_car==True:
    
        n=0
      
        car.rotate_draw()
        
        accelarate, limit= engine(state)
        if accelarate!=0:
            prev_move=0   
            car.move(accelarate, pos)
        if limit!=0:
            prev_move=1
            car.rotate(limit)
       

        if car.is_draw==False:
            for i in range(len(car.movement_array)):
                if car.movement_array[i+1]==0:
                    if n>1:
                        car.is_move=0
                        n-=1
                    car.move()
                    #car.rotate_draw()
                    n+=1
                if car.movement_array[i+1]!=0:
                    print(i)
                    car.is_draw=False
                    break

        pass              
    pygame.display.flip()

#def car_action(car):
#    surface.blit(red_car_img, (car.x, car.y))
def engine(state):
    global pos
    global accelarate
    global limit
    global is_car
    global car_stop
    global prev_state

    x=25
    y=1.4
   # print("state", state, "previous_state", prev_state, "prev_move", prev_move)

    if state!=prev_state:
        if state < len(car.movement_array):
            if car.movement_array[state]==0:
                limit=0
                if direction[state]==6: 
                    pos="x"
                    car.x_value=y
                    accelarate +=x
                   
                elif direction[state]==8:
                    pos="x"
                    car.x_value=-y
                    accelarate +=x
                    
                elif direction[state]==2:
                    pos="y"
                    car.x_value=-y
                    accelarate+=x
                   
                elif direction[state]==5:
                    pos="y"
                    car.x_value=y
                    accelarate+=x
                    
                #print("yeah", car.angle, accelarate, limit) 
             
    
            elif car.movement_array[state]==-4 : #up-right
                accelarate=0
                car.rotation_vel=-3 
                limit+=30
         
            elif car.movement_array[state]==-6 :#up-left
                accelarate=0
                car.rotation_vel= 3
                limit+=30 #up-left
                pass
            elif car.movement_array[state]==-1 :#down-right
                car.y+=5
                accelarate=0
                car.rotation_vel= 3
                limit+=30

            elif car.movement_array[state]==-3 : #down-left
                car.y+=5
                accelarate=0
                car.rotation_vel=-3
                limit+=30

            elif car.movement_array[state]== 4:#right-up
                car.x+=5
                accelarate=0
                car.rotation_vel=3
                limit+=30

            elif car.movement_array[state]== 1 : #right-down
                car.x+=5
                accelarate=0
                car.rotation_vel=-3
                limit+=30

            elif car.movement_array[state]== 6:  #left-up
                car.x-=5
                accelarate=0
                car.rotation_vel= -3
                limit+=30

            elif car.movement_array[state]== 3 :#left-down
                car.x-=5
                accelarate=0
                car.rotation_vel=3
                limit+=30

            prev_state+=1
            if accelarate!=0:
                if prev_move==1:
                    car.is_move=0
            if limit!=0:
                if prev_move==0:
                    car.is_rotate=0


            return accelarate, limit
        else:
            prev_state+=1
            is_car=False
            car_stop=True
            accelarate=0
            limit=0
    
            return accelarate, limit
    else:
        return accelarate, limit
    
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
    global is_car
    global car
    
    global direction
    #direction=[]
    new_direct=[]

    n=len(path_array)-1
    new_direct.append(detect_pos(first.col, first.row, path_array[-1].col , path_array[-1].row))
    for i in range(n+1):
        print("i", i, n)
        direct=detect_pos(path_array[n-i].col, path_array[n-i].row, path_array[n-i-1].col, path_array[n-i-1].row)
        new_direct.append(direct)
    new_direct[-1]=detect_pos(path_array[1].col, path_array[1].row, path_array[0].col, path_array[0].row)
    #print("end", path_array[0].row, path_array[0].col)
    start=path_array[-1]
    
    car = Car(start.x, start.y , start.col, start.row)
    
    if new_direct[0]== 5: #down
        car.angle=270
    if new_direct[0]== 2: #up
        car.angle=90
    if new_direct[0]== 6: #right
        car.angle=360
    if new_direct[0]== 8: #left
        car.angle=180

    prev_elem=None
    rotate_elems=[-4, -6, -1, -3, 4, 1, 6, 3]

    for i in range(len(new_direct)):
        direction.append(new_direct[i])

    #print("newdirect", new_direct)

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
            car.movement_array.append(movement_elem)  
            direction.insert(len(car.movement_array), direction_elem)
            #direction[len(car.movement_array)]=direction_elem
            #print(direction, new_direct, len(car.movement_array) , len(direction))
            car.movement_array.append(r)
            prev_elem=r

        elif r in rotate_elems and prev_elem==0 and len(car.movement_array)!=1:
            #print("-----------------", direction[len(car.movement_array)], len(car.movement_array))
            q=check_start(car.movement_array)
            if q==True:
                car.movement_array.append(0)
                direction.insert(len(car.movement_array), direction[len(car.movement_array)-1])
                car.movement_array.append(r)
                prev_elem=r
            else:
                car.movement_array.append(r)
                prev_elem=r
        else:
            car.movement_array.append(r)
            prev_elem=r

    #if len(direction)!=len(car.movement_array):
    #    direction.append(8)
    #print("new direct", new_direct , "direction", direction,  "angle", car.angle, "length", len(direction), len(car.movement_array))
   
    is_car=True

path_array=[] 
#updated contruct path function (colouring grass cell the path color)
def construct_path(curr_node, from_list, start):
    global is_car
    
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
          #  if t.is_grass== True:
          #      t.path_color()
          #  else:
          #      t.backtrack()
            r=t 
    #path_array[0].is_blit= True
    
    
    
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
  

def car_reset(grid):
    global car_stop
    car_stop=False
    reset_car_var()
    for row in grid:
        for col in row:
            if col.is_path==True:
                col.is_path=False

def main():
    run = True
    grid=grid_make(WIDTH)
    start=None
    end=None
    
  
    while run:
        draw(surface,grid)

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
                    car_reset(grid)
                
                if event.key==pygame.K_d and start and end:
                    print(start, end)
                    dijkstra(lambda: draw(surface, grid),grid, start, end)

                #clearing out the visualisation part
                if event.key==pygame.K_SPACE:
                     visua_reset(grid, start, end)
                    
        
    pygame.quit()


if __name__=="__main__":
    main()
   
