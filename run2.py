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
            elif node2.isupper():
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
        
        def find_target_gateway_and_next_move(self, virus_pos: str) -> Tuple[str, str]:

            if virus_pos in self.gateways:
                return virus_pos, virus_pos
            
            visited = set()
            queue = deque([(virus_pos, [virus_pos])])
            best_gateway = None
            best_path = None
            min_distance = float('inf')
            
            while queue:
                current, path = queue.popleft()
                
                if current in visited:
                    continue
                visited.add(current)
                
                if current in self.gateways:
                    distance = len(path) - 1
                    if (distance < min_distance or 
                        (distance == min_distance and current < best_gateway)):
                        min_distance = distance
                        best_gateway = current
                        best_path = path
                    continue
                
                if len(path) - 1 <= min_distance:
                    for neighbor in sorted(self.graph.get(current, [])):
                        if neighbor not in visited:
                            queue.append((neighbor, path + [neighbor]))
            
            if best_path and len(best_path) > 1:
                return best_gateway, best_path[1]
            return best_gateway, best_gateway
        
        def get_critical_links(self, virus_pos: str) -> List[Tuple[str, str]]:
            critical_links = []
            
            for neighbor in sorted(self.graph.get(virus_pos, [])):
                if neighbor in self.gateways:
                    critical_links.append((neighbor, virus_pos))
            
            if critical_links:
                return critical_links
            
            _, next_move = self.find_target_gateway_and_next_move(virus_pos)
            if next_move and next_move not in self.gateways:
                for neighbor in sorted(self.graph.get(next_move, [])):
                    if neighbor in self.gateways:
                        critical_links.append((neighbor, next_move))
            
            return critical_links
        
        def get_lexicographically_smallest_gateway_link(self) -> Tuple[str, str]:
            all_links = []
            
            for gateway in sorted(self.gateway_links.keys()):
                for node in sorted(self.gateway_links[gateway]):
                    all_links.append((gateway, node))
            
            return all_links[0] if all_links else None


    network = Network()
    for node1, node2 in edges:
        network.add_link(node1, node2)
    
    result = []
    virus_pos = "a" 
    
    while True:
        if virus_pos in network.gateways:
            break
        
        critical_links = network.get_critical_links(virus_pos)
        
        if critical_links:
            critical_links.sort()
            gateway, node = critical_links[0]
            result.append(f"{gateway}-{node}")
            network.remove_link(gateway, node)
        else:
            link = network.get_lexicographically_smallest_gateway_link()
            if link:
                gateway, node = link
                result.append(f"{gateway}-{node}")
                network.remove_link(gateway, node)
            else:
                break
        
        if virus_pos not in network.gateways:
            _, next_move = network.find_target_gateway_and_next_move(virus_pos)
            if next_move and next_move in network.graph.get(virus_pos, []):
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