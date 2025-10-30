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
        target_gateway = find_target_gateway(graph, virus_pos, gateways)
        if target_gateway is None:
            break
            
        optimal_path = find_optimal_path_to_gateway(graph, virus_pos, target_gateway)
        if not optimal_path or len(optimal_path) < 2:
            break
            
        edge_to_cut = find_gateway_edge_on_path(optimal_path, gateways)
        if edge_to_cut is None:
            edge_to_cut = find_lexicographically_smallest_gateway_edge(graph, gateways)
            if edge_to_cut is None:
                break
        
        result.append(f"{edge_to_cut[0]}-{edge_to_cut[1]}")
        graph[edge_to_cut[0]].remove(edge_to_cut[1])
        graph[edge_to_cut[1]].remove(edge_to_cut[0])
        
        new_path = find_optimal_path_to_gateway(graph, virus_pos, target_gateway)
        
        if new_path and len(new_path) > 1:
            virus_pos = new_path[1]
        else:
            new_target_gateway = find_target_gateway(graph, virus_pos, gateways)
            if new_target_gateway:
                new_path_to_new_target = find_optimal_path_to_gateway(graph, virus_pos, new_target_gateway)
                if new_path_to_new_target and len(new_path_to_new_target) > 1:
                    target_gateway = new_target_gateway
                    virus_pos = new_path_to_new_target[1]
                else:
                    break
            else:
                break
            
    return result

def find_target_gateway(graph, start, gateways):
    distances = {}
    visited = set()
    queue = deque([(start, 0)])
    
    while queue:
        current, dist = queue.popleft()
        if current in visited:
            continue
        visited.add(current)
        
        if current in gateways:
            distances[current] = dist
            continue
            
        if current in graph:
            for neighbor in sorted(graph[current]):
                if neighbor not in visited:
                    queue.append((neighbor, dist + 1))
    
    if not distances:
        return None
    
    min_distance = min(distances.values())
    candidate_gateways = [gw for gw, dist in distances.items() if dist == min_distance]
    
    return sorted(candidate_gateways)[0]

def find_optimal_path_to_gateway(graph, start, target_gateway):
    visited = {start: None}
    queue = deque([start])
    
    while queue:
        current = queue.popleft()
        
        if current == target_gateway:
            return reconstruct_path(visited, start, target_gateway)
            
        if current in graph:
            neighbors = sorted(graph[current])
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited[neighbor] = current
                    queue.append(neighbor)
    
    return None

def find_gateway_edge_on_path(path, gateways):
    for i in range(len(path) - 1):
        node1, node2 = path[i], path[i+1]
        if node1 in gateways or node2 in gateways:
            return (node1, node2) if node1 in gateways else (node2, node1)
    return None

def find_lexicographically_smallest_gateway_edge(graph, gateways):
    possible_cuts = []
    for gateway in sorted(gateways):
        if gateway in graph:
            for neighbor in sorted(graph[gateway]):
                possible_cuts.append((gateway, neighbor))
    return possible_cuts[0] if possible_cuts else None

def reconstruct_path(visited, start, end):
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = visited[current]
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