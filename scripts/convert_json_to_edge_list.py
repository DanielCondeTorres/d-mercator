#!/usr/bin/env python3
import argparse
import json
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# Diccionario de países, continentes y colores
continent_dict = {
    "africa": ["egypt", "morocco", "south africa"],
    "asia": ["china", "india", "indonesia", "iran", "israel", "japan", "jordan", "kazakhstan", "kuwait", "macao", "malaysia", "pakistan", "palestine", "saudi arabia", "singapore", "south korea", "sri lanka", "taiwan", "thailand", "turkey", "united arab emirates", "viet nam"],
    "europe": ["austria", "belgium", "bulgaria", "croatia", "cyprus", "czech republic", "denmark", "estonia", "finland", "france", "germany", "greece", "hungary", "ireland", "italy", "netherlands", "norway", "poland", "portugal", "romania", "russian federation", "serbia", "slovakia", "slovenia", "spain", "sweden", "switzerland", "ukraine", "united kingdom"],
    "north america": ["canada", "mexico", "united states"],
    "south america": ["argentina", "brazil", "chile", "colombia", "ecuador", "peru", "venezuela"],
    "oceania": ["australia", "new zealand"]
}

continent_colors = {
    "Africa": "#FF5733",
    "Asia": "#33FF57",
    "Europe": "#3357FF",
    "North America": "#FF33A1",
    "South America": "#A133FF",
    "Oceania": "#33FFF5",
    "Unknown": "#808080"
}

# Función para obtener el continente y color
def get_continent_and_color(country):
    for continent, countries in continent_dict.items():
        if country.lower() in countries:
            continent_title = continent.title()
            return continent_title, continent_colors.get(continent_title, "#808080")
    return "Unknown", "#808080"

# Procesar archivo de países
def process_countries(input_file, output_file):
    data = []
    with open(input_file, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split(" ", 1)
            if len(parts) == 2:
                code, country = parts
                continent, color = get_continent_and_color(country)
                data.append(f"{code} {country} {continent} {color}")
    
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("\n".join(data))
    
    print(f"Archivo generado: {output_file}")

# Procesar archivo JSON y generar grafos
def process_network(input_file, output1_file, output2_file, output3_file):
    with open(input_file, "r", encoding="utf-8-sig") as f:
        data = json.load(f)
    
    network = data.get("network", {})
    nodes = network.get("items", [])
    edges = network.get("edges", network.get("links", []))
    
    G = nx.Graph()
    for node in nodes:
        G.add_node(node["id"], label=node.get("label", str(node["id"])))
    
    for edge in edges:
        if "source_id" in edge and "target_id" in edge:
            G.add_edge(edge["source_id"], edge["target_id"], weight=edge.get("strength", 1))
    
    with open(output1_file, "w", encoding="utf-8") as f:
        f.write("# node1 node2 weight\n")
        for source, target in G.edges():
            f.write(f"{source} {target}\n")
    
    with open(output2_file, "w", encoding="utf-8") as f:
        f.write("# node label\n")
        for node, data in G.nodes(data=True):
            f.write(f"{node} {data.get('label', str(node))}\n")
    
    with open(output3_file, "w", encoding="utf-8") as f:
        f.write("# node1_label node2_label\n")
        for source, target in G.edges():
            f.write(f"{G.nodes[source]['label'].replace(' ', '_')} {G.nodes[target]['label'].replace(' ', '_')}\n")
    
    print(f"Archivos de red generados: {output1_file}, {output2_file}, {output3_file}")

    pos = nx.spring_layout(G)
    plt.figure(figsize=(12, 12))
    nx.draw(G, pos, with_labels=True, node_size=500, node_color="skyblue", edge_color="gray")
    plt.title("Grafo generado a partir del JSON de VOSviewer")
    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Procesa archivos JSON de VOSviewer y datos de países.")
    parser.add_argument("-i", "--input", help="Archivo JSON de entrada")
    parser.add_argument("-o1", "--output1", help="Archivo edge list (node1 node2)")
    parser.add_argument("-o2", "--output2", help="Archivo lista de nodos (node label)")
    parser.add_argument("-o3", "--output3", help="Archivo edge list con etiquetas (node1_label node2_label)")
    #parser.add_argument("-c", "--countries", help="Archivo de países de entrada")
    parser.add_argument("-oc", "--output_countries", help="Archivo de países de salida con continentes y colores")
    
    args = parser.parse_args()
    
    if args.input and args.output1 and args.output2 and args.output3:
        process_network(args.input, args.output1, args.output2, args.output3)
    
    if args.countries and args.o2:
        process_countries(args.o2, args.output_countries)
