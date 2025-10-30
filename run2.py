import sys
from collections import deque

def solve(edges: list[tuple[str, str]]) -> list[str]:
    graph = {}
    gateways = set()
    
    for node1, node2 in edges:
        if node1 not in graph:
            graph[node1] = []
        if node2 not in graph:
            graph[node2] = []
        
        graph[node1].append(node2)
        graph[node2].append(node1)
        
        if node1.isupper():
            gateways.add(node1)
        if node2.isupper():
            gateways.add(node2)
    
    result = []
    virus_pos = 'a'
    
    while True:
        target_gateway, path = find_optimal_path(graph, virus_pos, gateways)
        
        if target_gateway is None:
            break
            
        edge_to_cut = find_edge_to_cut(graph, path, gateways, virus_pos)
        
        if edge_to_cut is None:
            edge_to_cut = find_any_available_gateway_edge(graph, gateways)
            if edge_to_cut is None:
                break  
        
        result.append(f"{edge_to_cut[0]}-{edge_to_cut[1]}")
        
        graph[edge_to_cut[0]].remove(edge_to_cut[1])
        graph[edge_to_cut[1]].remove(edge_to_cut[0])
        _, new_path = find_optimal_path(graph, virus_pos, gateways)
        if new_path and len(new_path) > 1:
            virus_pos = new_path[1] 
        else:
            break
            
    return result


def find_optimal_path(graph, start, gateways):
    distances = {start: 0}
    previous = {start: None}
    queue = deque([start])
    gateways_reached = {}
    
    while queue:
        current_level = sorted(queue) 
        queue.clear()
        
        for current in current_level:
            if current in gateways:
                path = reconstruct_path(previous, start, current)
                gateways_reached[current] = path
                continue  
            
            neighbors = sorted(graph.get(current, []))
            for neighbor in neighbors:
                if neighbor not in distances:
                    distances[neighbor] = distances[current] + 1
                    previous[neighbor] = current
                    queue.append(neighbor)
    
    if not gateways_reached:
        return None, None
    
    min_distance = min(len(path) - 1 for path in gateways_reached.values())
    candidate_gateways = [
        (gateway, path) for gateway, path in gateways_reached.items() 
        if len(path) - 1 == min_distance
    ]
    
    candidate_gateways.sort(key=lambda x: x[0])
    
    return candidate_gateways[0]


def find_edge_to_cut(graph, path, gateways, virus_pos):
    for i in range(len(path) - 1):
        node1, node2 = path[i], path[i + 1]
        if node1 in gateways or node2 in gateways:
            if node1 in gateways:
                return (node1, node2)
            else:
                return (node2, node1)
    
    if len(path) == 2 and path[1] in gateways:
        return (path[1], path[0])
    
    return None


def find_any_available_gateway_edge(graph, gateways):
    possible_cuts = []
    for gateway in sorted(gateways):
        if gateway in graph:
            for neighbor in sorted(graph[gateway]):
                possible_cuts.append((gateway, neighbor))
    
    return possible_cuts[0] if possible_cuts else None


def reconstruct_path(previous, start, end):
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous.get(current)
    return path[::-1]


def main():
    edges = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            node1, sep, node2 = line.partition('-')
            if sep:
                edges.append((node1, node2))
    
    result = solve(edges)
    for edge in result:
        print(edge)


if __name__ == "__main__":
    main()