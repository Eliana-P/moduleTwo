import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

file_path = '/Users/elianapritchard/Documents/INST414 WORK/top_insta_influencers_data.csv'  # Your file path
df = pd.read_csv(file_path, nrows=20)

def convert_to_float(value):
    if isinstance(value, str):
        if 'm' in value:
            return float(value.replace('m', '').replace(',', '').strip()) * 1e6
        elif 'k' in value:
            return float(value.replace('k', '').replace(',', '').strip()) * 1e3
        elif 'b' in value:
            return float(value.replace('b', '').replace(',', '').strip()) * 1e9
        else:
            return float(value.replace(',', '').strip())
    return value

df['new_post_avg_like'] = df['new_post_avg_like'].apply(convert_to_float)
df['followers'] = df['followers'].apply(convert_to_float)
df['group'] = pd.qcut(df['new_post_avg_like'], q=6, labels=False) #he said this

def create_likes_graph():
    G = nx.Graph()

    for _, row in df.iterrows():
        G.add_node((row['channel_info'], row['new_post_avg_like']), followers=row['followers'], new_post_avg_like=row['new_post_avg_like'], group=row['group'])

    for i, row_i in df.iterrows():
        for j, row_j in df.iterrows():
            if i >= j:
                continue  
            if row_i['group'] == row_j['group']:
                G.add_edge((row_i['channel_info'], row_i['new_post_avg_like']), (row_j['channel_info'], row_j['new_post_avg_like']))
    return G

def visualize_graph(G):
    plt.figure(figsize=(12, 10))
    pos = nx.spring_layout(G, seed=42, k=0.8)  
    node_sizes = [G.nodes[node]['followers'] / 80000 for node in G.nodes()] 

    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='skyblue', alpha=0.7)
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5, edge_color='gray')
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

    plt.title("Influencer Network Graph Based on Average Like Count and Number of Followers")
    plt.axis('off')
    plt.show()
    
likes_graph = create_likes_graph()

visualize_graph(likes_graph)
