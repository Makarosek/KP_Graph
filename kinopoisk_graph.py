import requests
from bs4 import BeautifulSoup
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objs as go


def parse_kinopoisk(actor_id):
    url = f"https://www.kinopoisk.ru/name/{actor_id}/film/"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Ошибка при запросе данных: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    film_elements = soup.select('.selection-film-item-meta a')
    film_ids = [film.get('href').split('/')[-2] for film in film_elements]
    return film_ids


def get_actors_from_film(film_id):
    url = f"https://www.kinopoisk.ru/film/{film_id}/"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Ошибка при запросе данных: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    actors = [actor.text.strip() for actor in soup.select('.actor-list .actor-name')]
    return actors


def get_film_data(film_id):
    url = f"https://www.kinopoisk.ru/film/{film_id}/"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Ошибка при запросе данных: {e}")
        return {}

    soup = BeautifulSoup(response.text, 'html.parser')
    genres = [genre.text.strip() for genre in soup.select('.info .g-i')]
    year = soup.select_one('.info .year').text.strip() if soup.select_one('.info .year') else None

    return {
        'genres': genres,
        'year': year
    }


def create_graph(actor_id, depth=1, genres=None, years=None, visited=None):
    if visited is None:
        visited = set()

    if actor_id in visited:
        return nx.Graph()

    visited.add(actor_id)

    G = nx.Graph()
    films = parse_kinopoisk(actor_id)

    for film_id in films:
        film_data = get_film_data(film_id)
        if genres and not any(genre in film_data['genres'] for genre in genres):
            continue
        if years and film_data['year'] not in years:
            continue

        G.add_node(film_id)
        G.add_edge(actor_id, film_id)
        actors = get_actors_from_film(film_id)
        for actor in actors:
            if actor not in visited:
                G.add_node(actor)
                G.add_edge(actor, film_id)
                if depth > 1:
                    G = nx.compose(G, create_graph(actor, depth-1, genres, years, visited))

    return G


def visualize_graph(G):
    pos = nx.spring_layout(G)
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=list(G.nodes()),
        textposition='top center',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left'
            ),
        )
    )

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=0, l=0, r=0, t=0),
                        xaxis=dict(showgrid=False, zeroline=False),
                        yaxis=dict(showgrid=False, zeroline=False)
                    ))
    fig.show()


def main():
    actor_id = "37859"  # ID актера на Кинопоиске
    G = create_graph(actor_id, depth=1)
    visualize_graph(G)


if __name__ == "__main__":
    main()
