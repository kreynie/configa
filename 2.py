import argparse

import graphviz
import requests


def get_dependencies(package_name):
    url = f"https://pypi.python.org/pypi/{package_name}/json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("info", {}).get("requires_dist", [])
    return []


def generate_dependency_graph(package_name):
    graph = graphviz.Digraph(format="png")
    visited = set()
    packages_to_check = [package_name]

    while packages_to_check:
        current_package = packages_to_check.pop()
        if current_package in visited:
            continue
        visited.add(current_package)
        graph.node(current_package)

        dependencies = get_dependencies(current_package)
        for dependency in dependencies:
            graph.edge(current_package, dependency)
            packages_to_check.append(dependency.split(" ", 1)[0])

    return graph


def main():
    parser = argparse.ArgumentParser(
        description="Generate a Graphviz dependency graph for a Python package"
    )
    parser.add_argument("package_name", help="Name of the Python package")
    args = parser.parse_args()

    graph = generate_dependency_graph(args.package_name)
    graph.render(filename=f"dependency_graph_{args.package_name}", view=True)


if __name__ == "__main__":
    main()
