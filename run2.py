import sys
from collections import deque, defaultdict

def solve(edges: list[tuple[str, str]]) -> list[str]:

    graph = defaultdict(set)
    gateways = set()
    gateway_links = []
    
    for node1, node2 in edges:
        graph[node1].add(node2)
        graph[node2].add(node1)

        if node1.isupper():
            gateways.add(node1)
            gateway_links.append((node1, node2))
        if node2.isupper():
            gateways.add(node2)
            gateway_links.append((node2, node1))
    gateway_links.sort()
    
    result = []
    virus_pos = "a"
    
    def bfs_distances(start):
        distances = {start: 0}
        queue = deque([start])
        
        while queue:
            current = queue.popleft()
            for neighbor in graph.get(current, set()):
                if neighbor not in distances:
                    distances[neighbor] = distances[current] + 1
                    queue.append(neighbor)
        return distances
    
    def find_target_gateway(position):
        distances = bfs_distances(position)
        
        reachable_gateways = [gw for gw in gateways if gw in distances]
        
        if not reachable_gateways:
            return None
            
        min_dist = min(distances[gw] for gw in reachable_gateways)
        candidate_gateways = [gw for gw in reachable_gateways if distances[gw] == min_dist]
        
        candidate_gateways.sort()
        return candidate_gateways[0]
    
    def find_next_move(position, target_gateway):
        distances = bfs_distances(target_gateway)
        
        neighbors = list(graph.get(position, set()))
        neighbor_distances = []
        for neighbor in neighbors:
            if neighbor in distances:
                neighbor_distances.append((neighbor, distances[neighbor]))
        
        if not neighbor_distances:
            return None
            
        min_dist = min(dist for _, dist in neighbor_distances)
        candidate_neighbors = [node for node, dist in neighbor_distances if dist == min_dist]
        
        candidate_neighbors.sort()
        return candidate_neighbors[0]
    
    while True:
        immediate_threat = None
        for neighbor in graph.get(virus_pos, set()):
            if neighbor in gateways:
                immediate_threat = neighbor
                break
        
        if immediate_threat:
            if virus_pos < immediate_threat:
                link = f"{virus_pos}-{immediate_threat}"
            else:
                link = f"{immediate_threat}-{virus_pos}"
            
            result.append(link)
            graph[virus_pos].discard(immediate_threat)
            graph[immediate_threat].discard(virus_pos)
            
            if graph[virus_pos]:
                target_gw = find_target_gateway(virus_pos)
                if target_gw:
                    next_pos = find_next_move(virus_pos, target_gw)
                    if next_pos:
                        virus_pos = next_pos
                    else:
                        break
                else:
                    break
            else:
                break
            continue
        
        target_gw = find_target_gateway(virus_pos)
        if not target_gw:
            break
        
        next_pos = find_next_move(virus_pos, target_gw)
        if not next_pos:
            break
        
        blocked = False
        for gw_link in gateway_links:
            gw, node = gw_link
            if gw in graph and node in graph[gw]:
                result.append(f"{gw}-{node}")
                graph[gw].discard(node)
                graph[node].discard(gw)
                gateway_links = [(g, n) for g, n in gateway_links if not (g == gw and n == node)]
                blocked = True
                break
        
        if not blocked:
            available_links = []
            for gw in gateways:
                for node in graph.get(gw, set()):
                    available_links.append(f"{gw}-{node}")
            
            if available_links:
                available_links.sort()
                link = available_links[0]
                result.append(link)
                gw, node = link.split('-')
                graph[gw].discard(node)
                graph[node].discard(gw)
            else:
                break
        
        virus_pos = next_pos
        
        if virus_pos in gateways:
            break
    
    return result


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