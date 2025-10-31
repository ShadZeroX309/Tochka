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
        if node2 not in graph[node1]:
            graph[node1].append(node2)
        if node1 not in graph[node2]:
            graph[node2].append(node1)
        
        if node1.isupper():
            gateways.add(node1)
        if node2.isupper():
            gateways.add(node2)
    
    result = []
    virus_pos = 'a'
    
    while True:
        immediate_threat = None
        if virus_pos in graph:
            for neighbor in sorted(graph[virus_pos]):
                if neighbor in gateways:
                    immediate_threat = (neighbor, virus_pos)
                    break
        
        if immediate_threat:
            result.append(f"{immediate_threat[0]}-{immediate_threat[1]}")
            graph[immediate_threat[0]].remove(immediate_threat[1])
            graph[immediate_threat[1]].remove(immediate_threat[0])
            continue
        
        gateway_info = find_all_reachable_gateways(graph, virus_pos, gateways)
        
        if not gateway_info:
            break
        
        target_gateway = select_target_gateway(gateway_info)
        
        all_paths = find_all_shortest_paths(graph, virus_pos, target_gateway)
        
        if not all_paths:
            break
        
        next_nodes = set()
        for path in all_paths:
            if len(path) > 1:
                next_nodes.add(path[1])
        
        if not next_nodes:
            break
            
        next_virus_pos = sorted(next_nodes)[0]
        
        threatened_gateways = set()
        for path in all_paths:
            if len(path) > 1 and path[1] == next_virus_pos:
                for node in path:
                    if node in gateways:
                        threatened_gateways.add(node)
                        break
        
        edge_to_cut = None
        
        if threatened_gateways:
            gateway_to_block = sorted(threatened_gateways)[0]
            
            gateway_edges = set()
            for path in all_paths:
                if len(path) > 1 and path[1] == next_virus_pos:
                    for i in range(len(path) - 1):
                        if path[i] == gateway_to_block or path[i+1] == gateway_to_block:
                            if path[i] in gateways:
                                gateway_edges.add((path[i], path[i+1]))
                            else:
                                gateway_edges.add((path[i+1], path[i]))
            
            if gateway_edges:
                edge_to_cut = sorted(gateway_edges)[0]
        
        if edge_to_cut is None:
            all_gateway_edges = set()
            for path in all_paths:
                if len(path) > 1 and path[1] == next_virus_pos:
                    for i in range(len(path) - 1):
                        if path[i] in gateways or path[i+1] in gateways:
                            if path[i] in gateways:
                                all_gateway_edges.add((path[i], path[i+1]))
                            else:
                                all_gateway_edges.add((path[i+1], path[i]))
            
            if all_gateway_edges:
                edge_to_cut = sorted(all_gateway_edges)[0]
        
        if edge_to_cut is None:
            edge_to_cut = find_lexicographically_smallest_gateway_edge(graph, gateways)
            if edge_to_cut is None:
                break
        
        result.append(f"{edge_to_cut[0]}-{edge_to_cut[1]}")
        graph[edge_to_cut[0]].remove(edge_to_cut[1])
        graph[edge_to_cut[1]].remove(edge_to_cut[0])
        
        virus_pos = next_virus_pos
            
    return result

def find_all_reachable_gateways(graph, start, gateways):
    distances = {}
    visited = set([start])
    queue = deque([(start, 0)])
    
    while queue:
        current, dist = queue.popleft()
        
        if current in gateways:
            distances[current] = dist
            continue
            
        if current in graph:
            for neighbor in sorted(graph[current]):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
    
    return distances

def select_target_gateway(gateway_info):
    if not gateway_info:
        return None
    
    min_distance = min(gateway_info.values())
    candidate_gateways = [gw for gw, dist in gateway_info.items() if dist == min_distance]
    return sorted(candidate_gateways)[0]

def find_all_shortest_paths(graph, start, target):
    distances = {start: 0}
    predecessors = {start: []}
    queue = deque([start])
    
    while queue:
        current = queue.popleft()
        
        if current == target:
            continue
            
        current_dist = distances[current]
        
        if current in graph:
            for neighbor in sorted(graph[current]):
                if neighbor not in distances:
                    distances[neighbor] = current_dist + 1
                    predecessors[neighbor] = [current]
                    queue.append(neighbor)
                elif distances[neighbor] == current_dist + 1:
                    predecessors[neighbor].append(current)
    
    def build_paths(node):
        if node == start:
            return [[start]]
        
        paths = []
        for pred in predecessors.get(node, []):
            for path in build_paths(pred):
                paths.append(path + [node])
        return paths
    
    return build_paths(target) if target in predecessors else []

def find_lexicographically_smallest_gateway_edge(graph, gateways):
    possible_cuts = []
    for gateway in sorted(gateways):
        if gateway in graph:
            for neighbor in sorted(graph[gateway]):
                possible_cuts.append((gateway, neighbor))
    return possible_cuts[0] if possible_cuts else None

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