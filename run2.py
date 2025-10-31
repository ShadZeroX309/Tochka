import sys
from collections import deque
from typing import List, Tuple

def solve(edges: List[Tuple[str, str]]) -> List[str]:

    class Network:
        def __init__(self):
            self.graph = {}
            self.gateways = set()
            self.gateway_links = {}
        
        def add_link(self, node1: str, node2: str):
            if node1 not in self.graph:
                self.graph[node1] = []
            if node2 not in self.graph:
                self.graph[node2] = []
            
            self.graph[node1].append(node2)
            self.graph[node2].append(node1)
            

            if node1.isupper():
                self.gateways.add(node1)
                if node1 not in self.gateway_links:
                    self.gateway_links[node1] = set()
                self.gateway_links[node1].add(node2)
            if node2.isupper():
                self.gateways.add(node2)
                if node2 not in self.gateway_links:
                    self.gateway_links[node2] = set()
                self.gateway_links[node2].add(node1)
        
        def remove_link(self, node1: str, node2: str):
            if node1 in self.graph and node2 in self.graph[node1]:
                self.graph[node1].remove(node2)
            if node2 in self.graph and node1 in self.graph[node2]:
                self.graph[node2].remove(node1)
            
            if node1 in self.gateway_links and node2 in self.gateway_links[node1]:
                self.gateway_links[node1].remove(node2)
            if node2 in self.gateway_links and node1 in self.gateway_links[node2]:
                self.gateway_links[node2].remove(node1)
        
        def find_virus_next_move(self, virus_pos: str) -> str:

            if virus_pos in self.gateways:
                return virus_pos
            
            visited = set()
            queue = deque([(virus_pos, [virus_pos])])
            gateway_paths = []
            min_distance = float('inf')
            
            while queue:
                current, path = queue.popleft()
                
                if current in visited:
                    continue
                visited.add(current)
                
                distance = len(path) - 1
                if distance > min_distance:
                    continue
                
                if current in self.gateways:
                    if distance < min_distance:
                        min_distance = distance
                        gateway_paths = [(current, path)]
                    elif distance == min_distance:
                        gateway_paths.append((current, path))
                    continue
                
                for neighbor in sorted(self.graph.get(current, [])):
                    if neighbor not in visited:
                        queue.append((neighbor, path + [neighbor]))
            
            if not gateway_paths:
                return virus_pos
            

            gateway_paths.sort(key=lambda x: x[0])
            target_gateway, best_path = gateway_paths[0]
            
            all_paths_to_target = []
            visited = set()
            queue = deque([(virus_pos, [virus_pos])])
            
            while queue:
                current, path = queue.popleft()
                
                if current in visited:
                    continue
                visited.add(current)
                
                if current == target_gateway:
                    if len(path) - 1 == min_distance:
                        all_paths_to_target.append(path)
                    continue
                
                if len(path) - 1 < min_distance:
                    for neighbor in sorted(self.graph.get(current, [])):
                        if neighbor not in visited:
                            queue.append((neighbor, path + [neighbor]))
            
            next_nodes = set()
            for path in all_paths_to_target:
                if len(path) > 1:
                    next_nodes.add(path[1])
            
            return min(next_nodes) if next_nodes else virus_pos
        
        def get_links_to_disconnect(self, virus_pos: str) -> List[Tuple[str, str]]:

            links = []
            

            for neighbor in sorted(self.graph.get(virus_pos, [])):
                if neighbor in self.gateways:
                    links.append((neighbor, virus_pos))
            
            if links:
                return links
            
            next_move = self.find_virus_next_move(virus_pos)
            

            if next_move in self.gateways:

                for node in sorted(self.graph.get(virus_pos, [])):
                    if node == next_move:
                        links.append((next_move, virus_pos))
                return links
            
            for neighbor in sorted(self.graph.get(next_move, [])):
                if neighbor in self.gateways:
                    links.append((neighbor, next_move))
            
            if links:
                return links
            
            all_gateway_links = []
            for gateway in sorted(self.gateway_links.keys()):
                for node in sorted(self.gateway_links[gateway]):
                    all_gateway_links.append((gateway, node))
            
            return all_gateway_links[:1]
    
    network = Network()
    for node1, node2 in edges:
        network.add_link(node1, node2)
    
    result = []
    virus_pos = "a"
    

    while True:
        if virus_pos in network.gateways:
            break
        
        links_to_disconnect = network.get_links_to_disconnect(virus_pos)
        
        if not links_to_disconnect:
            break
        
        gateway, node = links_to_disconnect[0]
        result.append(f"{gateway}-{node}")
        network.remove_link(gateway, node)
        
        if virus_pos not in network.gateways:
            next_move = network.find_virus_next_move(virus_pos)
            if next_move != virus_pos and next_move in network.graph.get(virus_pos, []):
                virus_pos = next_move
            else:
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