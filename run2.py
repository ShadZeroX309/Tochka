import sys
from collections import deque
from typing import List, Tuple

def solve(edges: List[Tuple[str, str]]) -> List[str]:

    class Network:
        def __init__(self):
            self.graph = {}
            self.gateways = set()
        
        def add_link(self, node1: str, node2: str):
            if node1 not in self.graph:
                self.graph[node1] = []
            if node2 not in self.graph:
                self.graph[node2] = []
            
            self.graph[node1].append(node2)
            self.graph[node2].append(node1)
            
            if node1.isupper():
                self.gateways.add(node1)
            if node2.isupper():
                self.gateways.add(node2)
        
        def remove_link(self, node1: str, node2: str):
            if node1 in self.graph and node2 in self.graph[node1]:
                self.graph[node1].remove(node2)
            if node2 in self.graph and node1 in self.graph[node2]:
                self.graph[node2].remove(node1)
        
        def find_virus_path(self, virus_pos: str) -> Tuple[str, List[str]]:
            if virus_pos in self.gateways:
                return virus_pos, [virus_pos]
            
            visited = set()
            queue = deque([(virus_pos, [virus_pos])])
            gateway_paths = []
            
            while queue:
                current, path = queue.popleft()
                if current in visited:
                    continue
                visited.add(current)
                
                if current in self.gateways:
                    distance = len(path) - 1
                    gateway_paths.append((current, path, distance))
                    continue
                
                for neighbor in sorted(self.graph.get(current, [])):
                    if neighbor not in visited:
                        queue.append((neighbor, path + [neighbor]))
            
            if not gateway_paths:
                return None, []
            
            gateway_paths.sort(key=lambda x: (x[2], x[0]))
            target_gateway, best_path, _ = gateway_paths[0]
            
            return target_gateway, best_path
        
        def get_virus_next_move(self, virus_pos: str) -> str:
            target_gateway, path = self.find_virus_path(virus_pos)
            if not path or len(path) < 2:
                return virus_pos
            return path[1] 
        
        def simulate_game(self) -> List[str]:
            result = []
            virus_pos = "a"
            
            while True:

                if virus_pos in self.gateways:
                    break
                

                action = self.get_best_action(virus_pos)
                if not action:
                    break
                
                result.append(action)

                gateway, node = action.split('-')
                self.remove_link(gateway, node)
                

                if virus_pos not in self.gateways:
                    next_move = self.get_virus_next_move(virus_pos)
                    if next_move != virus_pos and next_move in self.graph.get(virus_pos, []):
                        virus_pos = next_move
                    else:
                        break 
            
            return result
        
        def get_best_action(self, virus_pos: str) -> str:
            for neighbor in sorted(self.graph.get(virus_pos, [])):
                if neighbor in self.gateways:
                    return f"{neighbor}-{virus_pos}"
            
            next_move = self.get_virus_next_move(virus_pos)

            if next_move in self.gateways:
                return f"{next_move}-{virus_pos}"
            

            for neighbor in sorted(self.graph.get(next_move, [])):
                if neighbor in self.gateways:
                    return f"{neighbor}-{next_move}"
            
            all_links = []
            for gateway in sorted(self.gateways):
                if gateway in self.graph:
                    for node in sorted(self.graph[gateway]):
                        all_links.append(f"{gateway}-{node}")
            
            return all_links[0] if all_links else None
    
    network = Network()
    for node1, node2 in edges:
        network.add_link(node1, node2)
    
    return network.simulate_game()

def main():
    edges = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            parts = line.split('-')
            if len(parts) == 2:
                node1, node2 = parts
                edges.append((node1, node2))
            else:
                nodes = line.split()
                if len(nodes) >= 2:
                    edges.append((nodes[0], nodes[1]))

    result = solve(edges)
    for edge in result:
        print(edge)

if __name__ == "__main__":
    main()