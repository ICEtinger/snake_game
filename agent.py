from environment import environment
import copy
import numpy as np

# mov[direction] is the displacement for the snake's head.
mov = [(0,1), (0,-1), (1,0), (-1,0)]
    
# the size of the maze region accessible from the snake's head
# (i.e.: that the snake can go to without hitting an obstacle).
def size_of_accessible_region(state):
    def DFS(tmp_obstacles, coord):
        if coord in tmp_obstacles:
            return 0
        size = 1
        # mark as visited
        tmp_obstacles.add(coord)
        # for each direction, visit adjacent cell
        for dir in range(4):
            size += DFS( tmp_obstacles, (coord[0]+mov[dir][0],coord[1]+mov[dir][1]) )
        return size
    
    obstacles, mice, head, curr_direction, score, game_terminated = state
     
    tmp = obstacles.copy()
    tmp.remove(head)
    return DFS(tmp, head)

def reward(state):
    obstacles, mice, head, curr_direction, score, game_terminated = state
    if game_terminated:
        return 10 * score + size_of_accessible_region(state) - 100100100
    else:
        return 10 * score + size_of_accessible_region(state)


def power_list(list_, power):
    if power == 1:
        return list_
    else:
        return [power_list(list_, power - 1) for i in list_]

def get_rewards_in_power_list(env_to_copy, power_list_):
    if type(power_list_) is list:    
        to_return = []
        for i,inner_pl in enumerate(power_list_):
            tmp_environment = copy.deepcopy(env_to_copy)
            tmp_environment.move(i)
            to_return.append(get_rewards_in_power_list(tmp_environment, inner_pl))
        return to_return
    else:
       return reward(env_to_copy.get_state()) 

def get_max_from_power_list(power_list_):
    if type(power_list_) is list:
        return max([get_max_from_power_list(inner_pl) for inner_pl in power_list_])
    else:
        return power_list_     

env = environment()
hit_an_obstacle = False
depth = 3 ######### parameter to change ##########
while hit_an_obstacle == False:
    pl = power_list([0,0,0,0], depth)
    rewards = get_rewards_in_power_list(env, pl)
    optimal_direction = np.argmax([get_max_from_power_list(rewards[i]) for i in range(4)])        
    env.move(optimal_direction)
    obstacles, mice, head, curr_direction, score, game_terminated = env.get_state()
    hit_an_obstacle = game_terminated

# just to test
state = env.get_state()
obstacles, mice, head, curr_direction, score, game_terminated = state
#print(obstacles)
print(mice)
print(head)
print(curr_direction)

print(size_of_accessible_region(state))
