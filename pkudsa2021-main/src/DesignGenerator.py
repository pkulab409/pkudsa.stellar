from typing import Tuple, List
import random

class DesignGenerator:
    
    def __init__(self, bridge: float, branch: Tuple[int, int], depth: int):
        self.bridge = bridge
        self.branch = branch
        self.depth = depth
    
    def generate(self):
        design = {}
        depth_nodes = [[] for i in range(self.depth)]
        depth_nodes[0].append(1)
        design[1] = {}
        total_nodes = 1
        for depth in range(self.depth - 1):
            for node in depth_nodes[depth]:
                son_number = random.randint(self.branch[0], self.branch[1])
                for k in range(son_number):
                    depth_nodes[depth + 1].append(total_nodes + 1)
                    design[node][total_nodes + 1] = 0
                    design[total_nodes + 1] = {node: 0}
                    total_nodes += 1
        for nodes in depth_nodes:
            for i in nodes[:-1]:
                x = random.random()
                if x < self.bridge:
                    design[i][i + 1] = 0
                    design[i + 1][i] = 0
            
        front_nodes = len(depth_nodes[-1])
        back_nodes = total_nodes - front_nodes 
        total_nodes = 2 * back_nodes + front_nodes
        for index in range(1, back_nodes + 1):
            design[total_nodes - index + 1] = {}
            for node in design[index]:
                design[total_nodes - index + 1][total_nodes - node + 1] = 0
                if total_nodes - node + 1 in depth_nodes[-1]:
                    design[total_nodes - node + 1][total_nodes - index + 1] = 0
                
        a = int(total_nodes**0.5)
        x0, y0 = -a/2, -a/2
        cnt = 0
        xy = {}
        for i in range(a+1):
            for j in range(a+1):
                cnt += 1
                if cnt>total_nodes:
                    break
                x = x0+i
                y = y0+j
                xy[cnt] = (x,y)

        return {
            "design": design,
            "xy": xy
        }