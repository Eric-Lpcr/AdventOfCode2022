from utilities.graph import SimpleWeightedGraph, SimpleGraph, print_visitor

graph = SimpleWeightedGraph()
data = [[(1, 1), (2, 7), (5, 3)], [(0, 1), (2, 1), (5, 1)], [(0, 7), (1, 1)], [(4, 2), (5, 2)], [(3, 2), (5, 5)], [(0, 3), (1, 1), (3, 2), (4, 5)]]
for i, neighbors in enumerate(data):
    for neighbor, weight in neighbors:
        graph.add_edge(i, neighbor, weight)

result, routes = graph.floyd_warshall()

print(repr(result))
print(repr(routes))

dist24 = result[2][4]
path24 = graph.reconstruct_path(routes[2], 2, 4)

print(dist24)
print(path24)

graph2 = SimpleGraph()
graph2.edges = {'A': {'B', 'C'},
                'B': {'D', 'E'},
                'C': {'F', 'G'},
                'E': {'H'}}

print('DFT')
graph2.depth_first_traversal('A', print_visitor)
print('BFT')
graph2.breadth_first_traversal('A', print_visitor)

came_from = graph2.breadth_first_search('A', 'F')
path24 = graph2.reconstruct_path(came_from, 'A', 'F')
print(path24)

