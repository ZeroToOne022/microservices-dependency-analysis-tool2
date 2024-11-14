
# Microservices Dependency Analysis Tool

Welcome to the **Microservices Dependency Analysis Tool**! This tool is designed to provide insights into the inner workings of a microservices-based system by analyzing code and configuration files, detecting API endpoints, HTTP calls, entities, and service dependencies, and visualizing them in an intuitive, color-coded dependency graph.

This tool is particularly useful for development teams working with complex microservices architectures who want a clearer understanding of inter-service communication and dependencies. It's also valuable for DevOps engineers and architects looking to document or troubleshoot interactions within a service ecosystem.

---

## 🌟 Key Features

- **Java and Python File Parsing**: Detects API endpoints, HTTP methods, and entities in Java and Python files.
- **Configuration Parsing**: Reads URLs and dependencies from `.properties` and `.yaml` files to map inter-service relationships.
- **Dependency Detection**: Identifies HTTP calls across services, including GET, POST, PUT, and DELETE methods, and maps them to known services.
- **Color-Coded Dependency Graph Visualization**: Generates a directed graph that visually represents service dependencies, with nodes and edges color-coded by the type of HTTP communication.
- **Entity Mapping**: Detects domain entities in both Java and Python classes, identifying which services interact with these entities.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Configuration Files](#configuration-files)
5. [Dependency Graph Visualization](#dependency-graph-visualization)
6. [Project Structure](#project-structure)
7. [Error Handling](#error-handling)
8. [Future Enhancements](#future-enhancements)

---

## 🔧 Prerequisites

Before you begin, make sure you have the following installed:

- **Python 3.6+**
- **Java environment** (for Java code analysis)
- Required Python packages:
  - `javalang` for Java file parsing
  - `pyyaml` for reading YAML configuration files
  - `configparser` for `.properties` file handling
  - `networkx` and `matplotlib` for generating and visualizing the dependency graph

---

## 🚀 Installation

To set up the Microservices Dependency Analysis Tool on your machine, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. **Install the required Python packages**:
   ```bash
   pip install javalang pyyaml configparser networkx matplotlib
   ```

3. **Set the `root_folder` variable** in the script to point to the root directory of your microservices project.

---

## 💻 Usage

Once everything is set up, you can run the tool to analyze your microservices project.

### Running the Analysis

To analyze the dependencies within your microservices project, run the following command:

```bash
python3 analyze_train_ticket.py
```

The tool will traverse the specified directory, parsing Java and Python files for API endpoints, HTTP calls, and entities. It will also read configuration files for service URLs and dependencies.

### Example Output

The script will produce two main outputs:

1. **Dependency Graph**: A graphical visualization of service dependencies.
2. **Summary Report**: A summary of total detected dependencies, entities, and a context map for each service.

---

## 🔧 Configuration Files

The tool supports parsing the following configuration file types:

- **`.properties` files**: Commonly used in Java projects, these files are parsed using the `configparser` module to map URLs to specific services.
- **YAML files (`.yml` or `.yaml`)**: These are parsed with the `pyyaml` module and allow you to map complex URL patterns to services.

Configuration files enable the tool to map URLs found in code to actual services, which is critical for accurate dependency detection.

---

## 📊 Dependency Graph Visualization

The visualized dependency graph is the highlight of this tool, making it easy to understand service interactions at a glance.

### Graph Details

- **Node Size**: Larger nodes represent core services with more dependencies, while smaller nodes indicate services with fewer connections.
- **Edge Color**: Different colors represent different HTTP methods:
  - **Blue**: GET requests
  - **Green**: POST requests
  - **Orange**: PUT requests
  - **Red**: DELETE requests

This color-coded approach lets you quickly see the type of communication each service utilizes.

---

## 📂 Project Structure

Here’s a breakdown of the main components within the project:

- **`parse_java_file(file_path)`**: Parses Java files to detect API endpoints and entities based on method and class declarations.
- **`parse_python_file(file_path)`**: Analyzes Python files to detect function and class definitions, identifying endpoints and domain entities.
- **`load_service_urls(root_folder)`**: Loads service URLs from configuration files to establish service mappings.
- **`find_http_calls(java_code, service_urls)`**: Detects HTTP calls in Java code and attempts to map them to known services using configuration data.
- **`analyze_microservices(root_folder)`**: Main function that traverses the project directory, parses code, collects dependency data, and builds a context map for each service.
- **`draw_dependency_graph(dependencies)`**: Generates and displays a color-coded dependency graph.

---

## 🛠️ Error Handling

This tool is designed to handle errors gracefully:

- **Syntax Errors**: Caught during Java and Python file parsing to prevent interruptions.
- **Configuration Parsing Errors**: If a configuration file contains errors, it is skipped, and the tool proceeds with other files.

Errors are logged to the console with helpful messages, making it easier to troubleshoot issues with specific files.

---

## 🚀 Future Enhancements

We’re actively working to make this tool even better! Planned enhancements include:

1. **Runtime Dependency Analysis**: Extend the tool to capture dependencies dynamically during runtime.
2. **Extended Language and Configuration Support**: Add support for languages like JavaScript and additional HTTP client libraries.
3. **Interactive Graph Navigation**: Allow users to zoom, filter, and interact with the graph for more in-depth analysis.

If you have any suggestions or ideas, please feel free to reach out!

---

We hope this tool makes it easier for you to manage and understand the complexity of your microservices architecture. Thank you for using the Microservices Dependency Analysis Tool!
