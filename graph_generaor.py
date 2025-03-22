

# actor_id = 3195362


def create_graph(actor_id, depth=1):
    all_actors = []
    for i in range(depth):
        movies = get_movies_ids(actor_id)
        for movie in movies:
            actors = get_actors_id_from_movie(movie)
            for actor in actors:
                if actor not in all_actors:
                    all_actors.append(actor)
