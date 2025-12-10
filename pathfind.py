import math

class Node:
    def __init__(self, position, tile, parent=None):
        self.position = position
        self.tile = tile
        self.parent = parent
        self.g = 0  # Cost from start to current node
        self.h = 0  # Heuristic cost estimate to goal
        self.f = 0  # Total cost
        

    def __eq__(self, other):
        return self.position == other.position
    
    def __lt__(self, other):
        return self.f < other.f
    
    def calculate_costs(self, goal):
        if self.parent:
            self.g = self.parent.g + 1
        else:
            self.g = 0
        if self.tile == 31:
            self.g += 2  # difficult terrain
        self.h = math.sqrt((self.position[0] - goal.position[0]) ** 2 + (self.position[1] - goal.position[1]) ** 2)
        self.f = self.g + self.h
    
def astar(start_pos, player_pos, tilemap, trees):
    x, y = 0, 0
    if player_pos[0] % 1 >= 0.5:
        x = int(player_pos[0]) + 1
    else: 
        x = int(player_pos[0])
    if player_pos[1] % 1 >= 0.5:
        y = int(player_pos[1]) + 1
    else: 
        y = int(player_pos[1])
    goal_pos = (x,y)
    start_node = Node(start_pos, tilemap[start_pos[1]][start_pos[0]])
    goal_node = Node(goal_pos, tilemap[goal_pos[1]][goal_pos[0]])
    
    open_list = []
    closed_list = []
    
    open_list.append(start_node)

    def add_to_open(open_list, neighbor_node):
        for open_node in open_list:
            if neighbor_node == open_node and neighbor_node.g >= open_node.g:
                return False
        return True
    
    while open_list:
        current_node = min(open_list, key=lambda node: node.f)
        open_list.remove(current_node)
        closed_list.append(current_node)
        
        if current_node == goal_node:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]
        
        neighbors = [
            (0, -1),  # Up
            (0, 1),   # Down
            (-1, 0),  # Left
            (1, 0)    # Right
        ]
        
        for new_position in neighbors:
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            
            if (node_position[0] > (len(tilemap[0]) - 1) or 
                node_position[0] < 0 or 
                node_position[1] > (len(tilemap) - 1) or 
                node_position[1] < 0):
                continue

            tile = tilemap[node_position[1]][node_position[0]]
            if tile >= 32:
                continue
            if (node_position[0], node_position[1]) in trees:
                continue

            neighbor_node = Node(node_position, tile, current_node)

            if neighbor_node in closed_list:
                continue
            
            neighbor_node.calculate_costs(goal_node)
            
            if add_to_open(open_list, neighbor_node):
                open_list.append(neighbor_node)
    
    return None