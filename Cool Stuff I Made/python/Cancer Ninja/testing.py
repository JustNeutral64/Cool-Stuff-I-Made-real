def make_level_grid_indexes():
    #TODO THIS IS THE WORST CODE I'VE WRITTEN. PLEASE FIX THIS
    scanner_x = 100
    scanner_y = player.y
    scanner_width = 300
    scanner_height = 300
    level_grid_indexes = []
    for x in range(100):
        level_grid_indexes.append([])
        
        level_grid_indexes[x].append([])
        level_grid_indexes[x].append([])
                
        for a in range(len(triangles)):
            # Why did i create a 4d list
            #TODO You could probably remove these 6 lines
            x1 = triangles[a].x1
            x2 = triangles[a].x2
            x3 = triangles[a].x3
            y1 = triangles[a].y1
            y2 = triangles[a].y2
            y3 = triangles[a].y3
            #Bottom left rectangle
            if point_collision_with_tri(scanner_x - (scanner_width / 2), scanner_y - (scanner_height / 2), x1, x2, x3, y1, y2, y3) == True:
                level_grid_indexes[x][1].append(a)
            #Bottom Right rectangle
            elif point_collision_with_tri(scanner_x + (scanner_width / 2), scanner_y - (scanner_height / 2), x1, x2, x3, y1, y2, y3) == True:
                level_grid_indexes[x][1].append(a)
            #Top Left rectangle
            elif point_collision_with_tri(scanner_x - (scanner_width / 2), scanner_y + (scanner_height / 3.1), x1, x2, x3, y1, y2, y3) == True:
                level_grid_indexes[x][1].append(a)
            #Top Right rectangle
            elif point_collision_with_tri(scanner_x + (scanner_width / 2), scanner_y + (scanner_height / 3.1), x1, x2, x3, y1, y2, y3) == True:
                level_grid_indexes[x][1].append(a)
            #First vertice
            elif point_collision_with_rect(x1, y1, (scanner_x - scanner_width / 2), (scanner_y - scanner_height / 2), (scanner_x + scanner_width / 2), (scanner_y + scanner_height / 3.1)) == True:
                level_grid_indexes[x][1].append(a)
            #Second vertice
            elif point_collision_with_rect(x2, y2, (scanner_x - scanner_width / 2), (scanner_y - scanner_height / 2), (scanner_x + scanner_width / 2), (scanner_y + scanner_height / 3.1)) == True:
                level_grid_indexes[x][1].append(a)
            #Third vertice
            elif point_collision_with_rect(x3, y3, (scanner_x - scanner_width / 2), (scanner_y - scanner_height / 2), (scanner_x + scanner_width / 2), (scanner_y + scanner_height / 3.1)) == True:
                level_grid_indexes[x][1].append(a)
            
        #Rectangles
        for a in range(len(rectangles)):
            if (scanner_x + (scanner_width / 2) > rectangles[a].bottom_left_x and scanner_x - (scanner_width / 2) < rectangles[a].top_right_x and scanner_y + (scanner_height / 3.1) > rectangles[a].bottom_left_y and scanner_y - (scanner_height / 2) < rectangles[a].top_right_y):
                level_grid_indexes[x][0].append(a)
        
        scanner_x += 200
    print(level_grid_indexes[0])