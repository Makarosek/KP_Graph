import requests
import json

kpURL = "https://api.kinopoisk.dev/v1.4"
X_API_KEY = "17DVSCF-KSFMT8M-J48JDQB-BFGV7MS"


def get_movies_ids(actor_id):
    request_url = f"/person/{actor_id}"
    url = kp_url + request_url

    headers = {"accept": "application/json",
               "X-API-KEY": f"{X_API_KEY}"}

    response = requests.get(url, headers=headers)

    data = json.loads(response.text)
    movies = data["movies"]          #List of dict

    for movie in movies :
        movies_ids.append(movie["id"])

    return movies_ids


def get_actors_id_from_movie(movie_id):
    request_url = f"/movie/{movie_id}"
    url = kp_url + request_url

    headers = {"accept": "application/json",
               "X-API-KEY": f"{X_API_KEY}"}

    response = requests.get(url, headers=headers)

    data = json.loads(response.text)
    persons = data["persons"]

    for person in persons:
        if person["enProfession"]=="actor":
            actors_ids.append(person["id"])

    return actors_ids
