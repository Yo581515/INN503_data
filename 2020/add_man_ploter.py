import pandas as pd
import plotly.graph_objects as go
from vars import country_names


def plot_3d(list_of_dicts, title_text=""):
    # Initialize the graph
    G = nx.Graph()

    # Generate a broader range of distinct colors
    all_colors = list(mcolors.CSS4_COLORS.values())
    num_projects = len(list_of_dicts)  # Adjust based on the number of unique projects
    selected_colors = all_colors[:num_projects]

    # Map each project to a unique color in RGBA format acceptable by Plotly
    colors = {project: plt.cm.viridis(i / len(list_of_dicts)) for i, dict_item in enumerate(list_of_dicts)
              for project in dict_item}
    edge_color = [f'rgba({int(col[0] * 255)},{int(col[1] * 255)},{int(col[2] * 255)},{col[3]})' for col in
                  colors.values()]

    # Add edges and nodes from list_of_dicts with color information
    for project_dict in list_of_dicts:
        for project, countries in project_dict.items():
            for country in countries:
                G.add_node(country, type='country')
            for i, country in enumerate(countries):
                for j in range(i + 1, len(countries)):
                    G.add_edge(countries[i], countries[j], color=colors[project], project=project)

    # Position nodes using the spring layout
    pos = nx.spring_layout(G, dim=3, seed=42)

    # Extract node positions
    node_x = [pos[node][0] for node in G]
    node_y = [pos[node][1] for node in G]
    node_z = [pos[node][2] for node in G]

    # Extract edges and their colors for Plotly
    edge_x, edge_y, edge_z = [], [], []
    for edge in G.edges(data=True):
        x0, y0, z0 = pos[edge[0]]
        x1, y1, z1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_z.extend([z0, z1, None])

    # Initialize your figure
    fig = go.Figure()

    # Add nodes as scatter3d traces
    fig.add_trace(go.Scatter3d(
        x=node_x,
        y=node_y,
        z=node_z,
        mode='markers+text',  # Ensure 'text' is part of the mode if you want labels visible without hover
        marker=dict(size=10, color='black', line=dict(color='rgba(50,50,50,0.14)', width=0.5)),
        text=list(G.nodes),  # Ensure this list contains the node names you want to display
        hoverinfo='text'  # This ensures the text appears when hovering over the node
    ))

    # Add edges as scatter3d traces directly, avoiding indirect index access
    for edge in G.edges(data=True):
        x0, y0, z0 = pos[edge[0]]
        x1, y1, z1 = pos[edge[1]]
        color = f"rgba({int(edge[2]['color'][0] * 255)}, {int(edge[2]['color'][1] * 255)}, {int(edge[2]['color'][2] * 255)}, {edge[2]['color'][3]})"
        fig.add_trace(go.Scatter3d(
            x=[x0, x1, None], y=[y0, y1, None], z=[z0, z1, None],
            mode='lines',
            line=dict(color=color, width=2),
            hoverinfo='none'
        ))

    # Configure and display the figure as before
    fig.update_layout(
        title_text=str(title_text),
        showlegend=False,
        scene=dict(
            xaxis=dict(showbackground=False, showticklabels=False, title=''),
            yaxis=dict(showbackground=False, showticklabels=False, title=''),
            zaxis=dict(showbackground=False, showticklabels=False, title='')
        )
    )

    fig.show()


import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.colors as mcolors


def plot_2d(list_of_dicts, title_text=""):
    # Initialize the graph
    G = nx.Graph()

    # Generate colors for each project
    num_projects = len(list_of_dicts)
    color_map = plt.cm.get_cmap('viridis', num_projects)
    project_colors = {project: color_map(i) for i, dict_item in enumerate(list_of_dicts) for project in dict_item}

    # Add edges and nodes with color information
    for project_dict in list_of_dicts:
        for project, countries in project_dict.items():
            G.add_edges_from(
                [(countries[i], countries[j]) for i in range(len(countries)) for j in range(i + 1, len(countries))],
                color=project_colors[project])

    # Position nodes using the spring layout
    pos = nx.spring_layout(G)

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=100, node_color='skyblue')

    # Draw edges with colors
    edges = G.edges(data=True)
    colored_edges = [edge[2]['color'] for edge in edges]
    nx.draw_networkx_edges(G, pos, edges, edge_color=colored_edges)

    # Draw labels
    nx.draw_networkx_labels(G, pos)

    plt.title(str(title_text))
    plt.axis('off')  # Turn off the axis for a cleaner look
    plt.show()


def count_projects_per_year(projects, organizations):
    # Merge projects and organizations datasets
    merged_data = pd.merge(projects, organizations, left_on='id', right_on='projectID')

    # Convert 'startDate' to datetime and extract the year
    merged_data['Year'] = pd.to_datetime(merged_data['startDate'], errors='coerce').dt.year

    # Map country codes to country names using 'country_names' dictionary
    merged_data['Country'] = merged_data['country'].map(country_names)

    # Group by Country and Year, counting unique project IDs
    grouped_data = merged_data.groupby(['Country', 'Year']).agg(NumberOfProjects=('projectID', 'nunique')).reset_index()

    # Transform grouped data into the desired format
    countries_projects = {}
    for _, row in grouped_data.iterrows():
        if row['Country'] not in countries_projects:
            countries_projects[row['Country']] = {}
        countries_projects[row['Country']][row['Year']] = row['NumberOfProjects']

    return countries_projects

def plot_number_of_projects_per_year(countries_projects, list_of_countries):
    plt.figure(figsize=(10, 6))

    for country in list_of_countries:
        if country in countries_projects:
            years = sorted(countries_projects[country].keys())
            num_projects = [countries_projects[country][year] for year in years]
            plt.plot(years, num_projects, marker='o', linestyle='-', label=country)

    plt.title('Number of Projects per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Projects')
    plt.legend(title="Country")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_ec_contribution_for_year(df_org, year, from_=""):
    activity_type_mapping = {
        'REC': 'Research',
        'OTH': 'Other',
        'PRC': 'Private Company',
        'HES': 'Higher Education',
        'PUB': 'Public Sector'
    }

    df_org['OrgType'] = df_org['activityType'].map(activity_type_mapping)
    # Assuming df_orgs_h2020 is your DataFrame
    # 1. Classify organizations
    df_org['OrgType'] = df_org['activityType'].map(activity_type_mapping)

    # 2. Aggregate data yearly
    df_org['Year'] = pd.to_datetime(df_org['contentUpdateDate']).dt.year
    yearly_data = df_org.groupby(['Year', 'OrgType']).agg({
        'ecContribution': ['mean', 'std', 'sum'],
        'projectID': 'nunique'
    }).reset_index()

    # 3. Descriptive statistics
    print(yearly_data)

    # 4. Visualizations 2022
    # For example, a pie chart of organizations types in a given year
    year_filter = yearly_data['Year'] == year
    data = yearly_data[year_filter]
    plt.pie(data['ecContribution']['sum'], labels=data['OrgType'], autopct='%1.1f%%')
    plt.title(f'Share of EC Contribution received by different types of organizations in the year {year} from {from_}')
    plt.show()