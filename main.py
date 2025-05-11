import pygame as pg
import numpy as np
# from world_generator import *
import time, random

start_time = time.time()

pg.init()
screen = pg.display.set_mode((600, 600))
pg.display.set_caption("My Game")
clock = pg.time.Clock()

water = 0
land = 1
shore = 2

horizontal_block_length = 30
vertical_block_length = 30
sketch_size = (20, 20)
horizontal_world_length = sketch_size[0]
vertical_world_length = sketch_size[1]
l_w_ratio = 1
land_water_ratio_erosion = [land, water]
max_eroding_possi = 0.7
min_eroding_possi = 0.3

land_block = np.full(horizontal_block_length, land)
water_block = np.full(horizontal_block_length, water)

sketch_world = np.random.randint(0, 2, size=sketch_size, dtype=np.uint8)
shores_list = []


def making_base_world():

    temp_layers = np.array([])
    temporary_world = None

    for horizontal_line in sketch_world:
        for node in horizontal_line:

            if node == land:
                temp_layers = np.concatenate((temp_layers, land_block), axis=None)

            if node == water:
                temp_layers = np.concatenate((temp_layers, water_block), axis=None)

            temp_layers = np.hstack((temp_layers))

        temp_layers = np.tile(temp_layers, (vertical_block_length, 1))
        
        if temporary_world is None:
            temporary_world = temp_layers
        else:
            temporary_world = np.vstack((temporary_world, temp_layers))
        temp_layers = np.array([])
    return temporary_world


def gathering_shores(terrain_layer, eroding_possi_layer):
    
    for vertical_pos in range(sketch_size[0]):
        for horizontal_pos in range(sketch_size[1]):    
                    
            if sketch_world[vertical_pos, horizontal_pos] == water:
                try:
                    if sketch_world[vertical_pos, horizontal_pos+1] == land and horizontal_pos+1 < sketch_size[1]:
                        for i in range(vertical_pos*vertical_block_length, (vertical_pos+1)*vertical_block_length-1):
                            terrain_layer[i, (horizontal_pos+1)*horizontal_block_length] = shore
                            eroding_possi_layer[i, (horizontal_pos+1)*horizontal_block_length] = max_eroding_possi
                            shores_list.append([i, (horizontal_pos+1)*horizontal_block_length])
                except IndexError:  
                    pass
                
                try:              
                    if sketch_world[vertical_pos+1, horizontal_pos] == land and vertical_pos+1 < sketch_size[0]:
                        for i in range(horizontal_pos*horizontal_block_length, (horizontal_pos+1)*horizontal_block_length-1):
                            terrain_layer[(vertical_pos+1)*vertical_block_length, i] = shore
                            eroding_possi_layer[(vertical_pos+1)*vertical_block_length, i] = max_eroding_possi
                            shores_list.append([(vertical_pos+1)*vertical_block_length, i])
                except IndexError:
                    pass

                    
            elif sketch_world[vertical_pos, horizontal_pos] == land:
                
                try:
                    if sketch_world[vertical_pos, horizontal_pos+1] == water and horizontal_pos+1 < sketch_size[1]:
                        for i in range(vertical_pos*vertical_block_length, (vertical_pos+1)*vertical_block_length-1):
                            terrain_layer[i, (horizontal_pos+1)*horizontal_block_length-1] = shore
                            eroding_possi_layer[i, (horizontal_pos+1)*horizontal_block_length-1] = max_eroding_possi
                            shores_list.append([i, (horizontal_pos+1)*horizontal_block_length-1]) 
                except IndexError:
                    pass
                
                try:
                    if sketch_world[vertical_pos+1, horizontal_pos] == water and vertical_pos+1 < sketch_size[0]:
                        for i in range(horizontal_pos*horizontal_block_length, (horizontal_pos+1)*horizontal_block_length-1):
                            terrain_layer[(vertical_pos+1)*vertical_block_length-1, i] = shore
                            eroding_possi_layer[(vertical_pos+1)*vertical_block_length-1, i] = max_eroding_possi
                            shores_list.append([(vertical_pos+1)*vertical_block_length-1, i])
                except IndexError:
                    pass
                        
    return terrain_layer, eroding_possi_layer
  
  
def making_possi_layer(terrain_layer):
    eroding_possi_layer = terrain_layer.copy()
    eroding_possi_layer.fill(0)
    return eroding_possi_layer


def eroding_land(terrain_layer): #this function is super slow
    for i in range(l_w_ratio):  

        for vertical_position in range(vertical_world_length * vertical_block_length - 1):
            for horizontal_position in range(horizontal_world_length * horizontal_block_length - 1):

                if terrain_layer[vertical_position, horizontal_position] == water:

                    if terrain_layer[vertical_position + 1, horizontal_position] != water:
                        terrain_layer[vertical_position + 1, horizontal_position] = random.choice(land_water_ratio_erosion)

                    if terrain_layer[vertical_position, horizontal_position + 1] != water:
                        terrain_layer[vertical_position, horizontal_position + 1] = random.choice(land_water_ratio_erosion)

                if terrain_layer[vertical_position, horizontal_position] != water:

                    if terrain_layer[vertical_position, horizontal_position + 1] == water or \
                            terrain_layer[vertical_position + 1, horizontal_position] == water:
                        terrain_layer[vertical_position, horizontal_position] = random.choice(land_water_ratio_erosion)

        for vertical_position in range((vertical_world_length * vertical_block_length) - 1, 0, -1):
            for horizontal_position in range(horizontal_world_length * horizontal_block_length - 1, 0, -1):

                if terrain_layer[vertical_position, horizontal_position] == water:

                    if terrain_layer[vertical_position, horizontal_position - 1] != water:
                        terrain_layer[vertical_position, horizontal_position - 1] = random.choice(land_water_ratio_erosion)

                    if terrain_layer[vertical_position - 1, horizontal_position] != water:
                        terrain_layer[vertical_position - 1, horizontal_position] = random.choice(land_water_ratio_erosion)

                if terrain_layer[vertical_position, horizontal_position] != water:

                    if terrain_layer[vertical_position, horizontal_position - 1] == water or \
                            terrain_layer[vertical_position - 1, horizontal_position] == water:
                        terrain_layer[vertical_position, horizontal_position] = random.choice(land_water_ratio_erosion)

        for horizontal_position in range(horizontal_world_length * horizontal_block_length - 1):
            for vertical_position in range(vertical_world_length * vertical_block_length - 1):

                if terrain_layer[vertical_position, horizontal_position] == water:

                    if terrain_layer[vertical_position, horizontal_position + 1] != water:
                        terrain_layer[vertical_position, horizontal_position + 1] = random.choice(land_water_ratio_erosion)

                    if terrain_layer[vertical_position + 1, horizontal_position] != water:
                        terrain_layer[vertical_position + 1, horizontal_position] = random.choice(land_water_ratio_erosion)

                if terrain_layer[vertical_position, horizontal_position] != water:

                    if terrain_layer[vertical_position, horizontal_position + 1] == water or \
                            terrain_layer[vertical_position + 1, horizontal_position] == water:
                        terrain_layer[vertical_position, horizontal_position] = random.choice(land_water_ratio_erosion)

        for horizontal_position in range(horizontal_world_length * horizontal_block_length - 1, 0, -1):
            for vertical_position in range(vertical_world_length * vertical_block_length - 1, 0, -1):

                if terrain_layer[vertical_position, horizontal_position] == water:

                    if terrain_layer[vertical_position, horizontal_position - 1] != water:
                        terrain_layer[vertical_position, horizontal_position - 1] = random.choice(land_water_ratio_erosion)

                    if terrain_layer[vertical_position - 1, horizontal_position] != water:
                        terrain_layer[vertical_position - 1, horizontal_position] = random.choice(land_water_ratio_erosion)

                if terrain_layer[vertical_position, horizontal_position] != water:

                    if terrain_layer[vertical_position, horizontal_position - 1] == water or \
                            terrain_layer[vertical_position - 1, horizontal_position] == water:
                        terrain_layer[vertical_position, horizontal_position] = random.choice(land_water_ratio_erosion)
    return terrain_layer


def eroding_land_v2(terrain_layer, eroding_possi_layer, shores_list):
    
    for i in range(30):
        new_shores_list = []
        
        for coor in shores_list:
            eroding_chance = random.random()
            
            if eroding_possi_layer[coor[0], coor[1]] >= eroding_chance and eroding_possi_layer[coor[0], coor[1]] >= min_eroding_possi:
                eroding_possi_layer[coor[0], coor[1]] -= 0.1
                
            else:
                
                eroding_possi_layer[coor[0], coor[1]] = 0
                terrain_layer[coor[0], coor[1]] = water
                try:
                    for di in [[-1, 0], [0, 1], [1, 0], [0, -1]]:
                        if terrain_layer[coor[0]+di[0], coor[1]+di[1]] == land:
                            terrain_layer[coor[0]+di[0], coor[1]+di[1]] = shore
                            eroding_possi_layer[coor[0]+di[0], coor[1]+di[1]] = max_eroding_possi
                            new_shores_list.append([coor[0]+di[0], coor[1]+di[1]])
                except IndexError:
                    pass
                shores_list.remove(coor)
        shores_list += new_shores_list
        print(len(shores_list))
        print(f'remaining loops {30-i}')
        
    return terrain_layer, eroding_possi_layer, shores_list
            

def drawing_world():
    for vertical_pos in range(sketch_size[0]*vertical_block_length):
        for horizontal_pos in range(sketch_size[1]*horizontal_block_length):
            
            if terrain_layer[vertical_pos, horizontal_pos] == land:
                block = pg.Rect(horizontal_pos, vertical_pos, 1, 1)
                pg.draw.rect(screen, (8, 99, 35), block)
                
            elif terrain_layer[vertical_pos, horizontal_pos] == water:
                block = pg.Rect(horizontal_pos, vertical_pos, 1, 1)
                pg.draw.rect(screen, (7, 17, 92), block)
                
            elif terrain_layer[vertical_pos, horizontal_pos] == shore:
                block = pg.Rect(horizontal_pos, vertical_pos, 1, 1)
                pg.draw.rect(screen, (255, 252, 94), block)
            

terrain_layer = making_base_world()

eroding_possi_layer = making_possi_layer(terrain_layer)

terrain_layer, eroding_possi_layer = gathering_shores(terrain_layer, eroding_possi_layer)

# terrain_layer = eroding_land(terrain_layer)

terrain_layer, eroding_possi_layer, shores_list = eroding_land_v2(terrain_layer, eroding_possi_layer, shores_list)

drawing_world()


end_time = time.time()
print("Execution time:", end_time - start_time, "seconds")

while True:
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

    pg.display.flip()
    clock.tick(60)
    
