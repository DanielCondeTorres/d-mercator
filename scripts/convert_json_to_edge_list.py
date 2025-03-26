#!/usr/bin/env python3
import argparse
import json
import networkx as nx
import matplotlib.pyplot as plt

def main(input_file, output1_file, output2_file, output3_file):
    # Cargar el JSON usando 'utf-8-sig' para manejar el BOM
    with open(input_file, "r", encoding="utf-8-sig") as f:
        data = json.load(f)
    
    # Extraer la sección de red
    network = data.get("network", {})
    nodes = network.get("items", [])
    edges = network.get("edges", network.get("links", []))
    
    # Crear el grafo (usa nx.DiGraph() si los enlaces son dirigidos)
    G = nx.Graph()
    
    # Agregar los nodos al grafo, usando el 'id' y guardando la etiqueta
    for node in nodes:
        G.add_node(node["id"], label=node.get("label", str(node["id"])))
    
    # Agregar los enlaces utilizando las claves "source_id", "target_id" y "strength" como peso
    for edge in edges:
        if "source_id" in edge and "target_id" in edge:
            source_id = edge["source_id"]
            target_id = edge["target_id"]
            weight = edge.get("strength", 1)  # Valor por defecto 1 si no se encuentra 'strength'
            G.add_edge(source_id, target_id, weight=weight)
        else:
            print("No se encontró 'source_id' ni 'target_id' en el enlace:", edge)
    
    # Guardar la edge list en el archivo de salida especificado (-o1)
    with open(output1_file, "w", encoding="utf-8") as f:
        f.write("# node1 node2 weight\n")
        for source, target, data_edge in G.edges(data=True):
            weight = data_edge.get("weight", 1)
            f.write(f"{source} {target}\n")  # {weight}\n")
    
    print(f"Edge list guardada en: {output1_file}")
    
    # Guardar la lista de nodos en el archivo de salida especificado (-o2)
    with open(output2_file, "w", encoding="utf-8") as f:
        f.write("# node label\n")
        for node, data_node in G.nodes(data=True):
            label = data_node.get("label", str(node))
            f.write(f"{node} {label}\n")
    
    print(f"Lista de nodos guardada en: {output2_file}")
    
    # Guardar la edge list usando etiquetas en lugar de IDs (-o3)
    # Asegurando que los nombres multi-palabra aparezcan juntos
    with open(output3_file, "w", encoding="utf-8") as f:
        f.write("# node1_label node2_label weight\n")
        for source, target, data_edge in G.edges(data=True):
            source_label = G.nodes[source].get("label", str(source))
            target_label = G.nodes[target].get("label", str(target))
            
            # Reemplazar espacios con guiones bajos para mantener las etiquetas juntas
            source_label_formatted = source_label.replace(" ", "_")
            target_label_formatted = target_label.replace(" ", "_")
            
            weight = data_edge.get("weight", 1)
            f.write(f"{source_label_formatted} {target_label_formatted}\n")  # {weight}\n")
    
    print(f"Edge list con etiquetas guardada en: {output3_file}")
    
    # Dibujar el grafo utilizando una disposición de fuerza de resorte
    pos = nx.spring_layout(G)
    labels = nx.get_node_attributes(G, "label")
    plt.figure(figsize=(12, 12))
    nx.draw_networkx_nodes(G, pos, node_size=500, node_color="skyblue")
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.7)
    nx.draw_networkx_labels(G, pos, labels, font_size=10)
    plt.title("Grafo generado a partir del JSON de VOSviewer")
    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convierte un archivo JSON de VOSviewer a edge list y node list, y dibuja el grafo"
    )
    parser.add_argument("-i", "--input", required=True,
                        help="Ruta del archivo JSON de entrada")
    parser.add_argument("-o1", "--output1", required=True,
                        help="Nombre del archivo de salida para la edge list (node1 node2 weight)")
    parser.add_argument("-o2", "--output2", required=True,
                        help="Nombre del archivo de salida para la lista de nodos (node label)")
    parser.add_argument("-o3", "--output3", required=True,
                        help="Nombre del archivo de salida para la edge list usando etiquetas (node1_label node2_label weight)")
    args = parser.parse_args()
    main(args.input, args.output1, args.output2, args.output3)
