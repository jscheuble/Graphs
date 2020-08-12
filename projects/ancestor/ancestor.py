from stack import Stack


def dfs(starting_vertex, g):

    stack = Stack()
    stack.push([starting_vertex])

    visited = []

    while stack.size():
        path = stack.pop()

        # Get the last vertex in the path
        vertex = path[-1]

        # mark visited
        if vertex not in visited:
            visited.append(vertex)

        # add path to parents to the stack
        # if the vertex has no parents, it sets dict value to empty list
        for parent in g.get(vertex, []):
            stack.push(path + [parent])

    # return the last visited vertex, this will be the highest level parent
    return visited[-1]


def earliest_ancestor(ancestors, starting_node):
    g = {}

    # loop over ancestors, add
    for parent, child in ancestors:
        if child not in g:
            g[child] = [parent]
        else:
            g[child].append(parent)

    # return -1 if starting node has no parents
    if starting_node not in g:
        return -1

    # else return depth first search
    return dfs(starting_node, g)
