from util import Queue


def populate_seen(g, current_room):
    exits = current_room.get_exits()
    g[current_room.id] = {}

    for exit in exits:
        g[current_room.id][exit] = '?'
    # print(g)


def get_opposites(direction):
    opposites = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
    return opposites[direction]


def get_room(room, path):
    if path == [] or path is None:
        return room
    else:
        print('path from get room', path)
        # something here is wrong, told me to go north when there is no north and therefore returns none
        print(room.get_room_in_direction(path[-1]))
        print('path -1', path[-1])
        return room.get_room_in_direction(path[-1])


def path_to_unexplored(current_room, visited):
    # bfs, finds closest room with unexplored path
    q = Queue()
    seen = set()

    q.enqueue([])
    for exit in current_room.get_exits():
        q.enqueue([exit, current_room.id])

    while q.size():
        path = q.dequeue()
        # room = path[-1]

        # forward = path[-2]

        # next_room = room.get_room_in_direction(forward)

        # if next_room:
        #     if next_room not in visited:
        #         return path[:-1]

        #     for direction in next_room.get_exits():
        #         next_path = path[:-1].copy()
        #         next_path.append(direction)
        #         next_path.append(next_room)
        #         q.enqueue(next_path)

        # return False

        room = get_room(current_room, path)
        if room:
            print('room', room.id)
        exits = room.get_exits() if room else None

        if exits:
            for direction in exits:
                if visited[room.id][direction] == '?':
                    print('++++++', path + [direction])
                    return path + [direction]
                if (room.id, direction) not in seen:
                    print('&&&&&&', path + [direction])

                    q.enqueue(path + [direction])
                seen.add((room.id, direction))


def traverse(player):
    seen = dict()
    current_room = player.current_room
    path = list()

    # add first room to visited
    populate_seen(seen, current_room)

    while True:
        directions = path_to_unexplored(current_room, seen)
        print('directons from main', directions)
        if directions is None or len(directions) == 0:
            return path
        for direction in directions:
            player.travel(direction)
            next_room = current_room.get_room_in_direction(direction)
            path.append(direction)
            prev = get_opposites(direction)
            populate_seen(seen, next_room)
            seen[current_room.id][direction] = next_room.id
            seen[next_room.id][prev] = current_room.id
            current_room = next_room
