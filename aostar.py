import networkx as nx

def ao_star_search(G, start, cost_key='cost'):
    # Initialize all node costs to None
    for node in G.nodes():
        G.nodes[node][cost_key] = None

    # Compute the cost of the start node
    best_cost = compute_cost(G, start, cost_key)
    
    solution = []
    build_solution(G, start, solution, cost_key)
    
    return best_cost, solution

def compute_cost(G, node, cost_key):
    # Get the children of the current node
    children = list(G.successors(node))
    
    # If the node has no children (it's a leaf), cost is 0
    if not children:
        G.nodes[node][cost_key] = 0
        return 0
    
    # Get the node type (OR/AND)
    node_type = G.nodes[node].get('node_type', 'OR')
    
    child_costs = []
    for c in children:
        c_cost = compute_cost(G, c, cost_key)
        child_costs.append(c_cost)
    
    # If the node is of type AND, sum the costs of the children
    if node_type == 'AND':
        total = sum(child_costs)
        G.nodes[node][cost_key] = total
        return total
    else:
        # If the node is of type OR, take the minimum cost of the children
        best = min(child_costs)
        G.nodes[node][cost_key] = best
        return best

def build_solution(G, node, solution, cost_key):
    solution.append(node)
    children = list(G.successors(node))
    
    # If no children, we have reached a leaf node
    if not children:
        return
    
    node_type = G.nodes[node].get('node_type', 'OR')
    
    if node_type == 'AND':
        # If the node is of type AND, explore all children
        for c in children:
            build_solution(G, c, solution, cost_key)
    else:
        # If the node is of type OR, choose the best child with the least cost
        best_c = None
        best_val = float('inf')
        for c in children:
            val = G.nodes[c][cost_key]
            if val < best_val:
                best_val = val
                best_c = c
        # Recurse on the best child
        build_solution(G, best_c, solution, cost_key)

if __name__ == "__main__":
    G = nx.DiGraph()
    G.add_node('A', node_type='OR')
    G.add_node('B', node_type='AND')
    G.add_node('C', node_type='OR')
    G.add_node('D', node_type='AND')
    
    G.add_edge('A', 'B')
    G.add_edge('A', 'C')
    G.add_edge('B', 'D')

    best_cost, solution_path = ao_star_search(G, 'A')
    
    print("Best cost:", best_cost)
    print("Solution path:", solution_path)
