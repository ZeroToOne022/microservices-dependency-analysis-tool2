import os
import re
import javalang
import ast
import yaml
import configparser
import networkx as nx
import matplotlib.pyplot as plt

# Function to parse Java files for endpoints and entities
def parse_java_file(file_path):
    with open(file_path, 'r') as file:
        java_code = file.read()
    try:
        tree = javalang.parse.parse(java_code)
    except javalang.parser.JavaSyntaxError:
        print(f"Syntax error in {file_path}. Skipping.")
        return [], []
    endpoints = []
    entities = []
    for path, node in tree:
        if isinstance(node, javalang.tree.MethodDeclaration):
            for annotation in node.annotations:
                if annotation.name in ['GetMapping', 'PostMapping', 'RequestMapping']:
                    path_value = ''
                    if annotation.element:
                        if isinstance(annotation.element, list):
                            path_value = ", ".join([str(getattr(elem, 'value', '')) for elem in annotation.element if isinstance(elem, javalang.tree.Literal)])
                        elif isinstance(annotation.element, javalang.tree.Literal):
                            path_value = annotation.element.value
                    endpoint = {
                        'method': annotation.name,
                        'path': path_value,
                        'return_type': node.return_type.name if node.return_type else 'void',
                        'params': [param.type.name for param in node.parameters]
                    }
                    endpoints.append(endpoint)
        if isinstance(node, javalang.tree.ClassDeclaration):
            if any('@Entity' in str(annotation) or '@Table' in str(annotation) or '@Document' in str(annotation) for annotation in node.annotations):
                entities.append(node.name)
    return endpoints, entities

# Function to parse Python files for endpoints and entities
def parse_python_file(file_path):
    with open(file_path, 'r') as file:
        python_code = file.read()
    try:
        tree = ast.parse(python_code)
    except SyntaxError:
        print(f"Syntax error in {file_path}. Skipping.")
        return [], []
    endpoints = []
    entities = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Attribute):
                    if decorator.func.attr in ['route', 'get', 'post']:
                        path_value = decorator.args[0].value if decorator.args else ''
                        endpoint = {
                            'method': decorator.func.attr.upper(),
                            'path': path_value,
                            'return_type': 'Unknown',
                            'params': [arg.arg for arg in node.args.args]
                        }
                        endpoints.append(endpoint)
        if isinstance(node, ast.ClassDef):
            for base in node.bases:
                if isinstance(base, ast.Name) and base.id == 'Model':
                    entities.append(node.name)
    return endpoints, entities

# Function to load service URLs from config files
def load_service_urls(root_folder):
    service_urls = {}
    for root, _, files in os.walk(root_folder):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(('.properties', '.yml', '.yaml')):
                try:
                    if file.endswith('.properties'):
                        config = configparser.ConfigParser()
                        config.read(file_path)
                        for key in config['DEFAULT']:
                            if 'url' in key.lower():
                                service_urls[key] = config['DEFAULT'][key]
                    elif file.endswith(('.yml', '.yaml')):
                        with open(file_path, 'r') as ymlfile:
                            cfg = yaml.safe_load(ymlfile)
                            for key, value in cfg.items():
                                if 'url' in key.lower():
                                    service_urls[key] = value
                except Exception as e:
                    print(f"Error parsing {file_path}: {e}")
    return service_urls

# Function to detect HTTP calls in Java files
def find_http_calls(java_code, service_urls):
    pattern = r'\.(post|get|put|delete)\s*\(.*\)'
    matches = re.findall(pattern, java_code, re.IGNORECASE)
    calls = []
    for match in matches:
        calls.append({
            'service': 'unknown',
            'method': match
        })
    # Try matching services from URLs if found
    for call in calls:
        if call['service'] == 'unknown':
            call['service'] = next((k for k, v in service_urls.items() if v in java_code), 'unknown')
    return calls

# Main function to analyze microservices
def analyze_microservices(root_folder):
    dependencies = []
    context_maps = {}
    service_urls = load_service_urls(root_folder)
    
    for root, dirs, files in os.walk(root_folder):
        if "test" in root.split(os.sep):
            continue
        for file in files:
            file_path = os.path.join(root, file)
            print(f"Processing file: {file_path}")
            if file.endswith('.java'):
                with open(file_path, 'r') as f:
                    java_code = f.read()
                endpoints, entities = parse_java_file(file_path)
                calls = find_http_calls(java_code, service_urls)
                dependencies.extend({
                    'caller': root.split(os.sep)[-2],
                    'callee': call['service'],
                    'method': call['method']
                } for call in calls)
            elif file.endswith('.py'):
                endpoints, entities = parse_python_file(file_path)
            else:
                continue
            service_name = root.split(os.sep)[-2]
            if service_name not in context_maps:
                context_maps[service_name] = {'endpoints': [], 'entities': []}
            context_maps[service_name]['endpoints'].extend(endpoints)
            context_maps[service_name]['entities'].extend(entities)
    return dependencies, context_maps

# Function to visualize the dependency graph
def draw_dependency_graph(dependencies):
    G = nx.DiGraph()
    for dep in dependencies:
        G.add_edge(dep['caller'], dep['callee'], label=dep['method'])
    
    pos = nx.spring_layout(G, k=0.3, seed=42)
    plt.figure(figsize=(14, 12))
    color_map = {'get': 'blue', 'post': 'green', 'put': 'orange', 'delete': 'red'}
    node_sizes = [3000 * (G.degree[node] + 1) for node in G.nodes()]
    
    nx.draw(G, pos, with_labels=True, node_size=node_sizes, node_color='lightgreen', font_size=10, font_weight='bold')
    for edge in G.edges(data=True):
        color = color_map.get(edge[2]['label'].lower(), 'black')
        nx.draw_networkx_edges(G, pos, edgelist=[edge], edge_color=color)
    
    edge_labels = {(dep['caller'], dep['callee']): dep['method'] for dep in dependencies}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
    
    for method, color in color_map.items():
        plt.plot([], [], color=color, label=method)
    plt.legend(title="HTTP Methods", loc="upper left")
    plt.title("Enhanced Microservices Dependency Graph")
    plt.show()

if __name__ == '__main__':
    root_folder = '/Users/sauravkumar/train-ticket'
    dependencies, context_maps = analyze_microservices(root_folder)
    print("\n=== Summary ===")
    print(f"Total detected dependencies: {len(dependencies)}")
    total_entities = sum(len(service['entities']) for service in context_maps.values())
    print(f"Total detected entities: {total_entities}")
    print("\nContext Maps:", context_maps)
    draw_dependency_graph(dependencies)
