from room import Room
from player import Player
from world import World
from util import Stack


import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


def populate_seen(g, current_room):
    exits = current_room.get_exits()
    g[current_room.id] = {}

    for exit in exits:
        g[current_room.id][exit] = '?'
    # print(g)


def get_opposites(direction):
    # save our route back to unvisited exits
    if direction == 'n':
        return 's'
    elif direction == 's':
        return 'n'
    elif direction == 'e':
        return 'w'
    elif direction == 'w':
        return 'e'


s = Stack()
visited = set()

seen = dict()
# populate seen dict with initial room
populate_seen(seen, player.current_room)

# while loop will terminate when each room has been added to visited set
while len(visited) < len(world.rooms):
    exits = player.current_room.get_exits()

    path = []
    for direction in exits:
        # check if exits in visited, add to path
        if player.current_room.get_room_in_direction(direction) not in visited and direction is not None:
            path.append(direction)

    # add to visited and populate seen dict
    visited.add(player.current_room)
    populate_seen(seen, player.current_room)

    # if there are directions in the path, pick one and travel
    if len(path) > 0:
        # pick random direction
        nxt = random.randint(0, len(path) - 1)
        # add to traversal path and stack
        traversal_path.append(path[nxt])
        s.push(path[nxt])
        # move player
        player.travel(path[nxt])
    else:  # travel backward
        last = s.pop()
        player.travel(get_opposites(last))
        traversal_path.append(get_opposites(last))

# print(seen)

print('===================')
print(traversal_path)
print('===================')


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
