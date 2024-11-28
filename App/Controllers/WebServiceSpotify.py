from dotenv import load_dotenv
import os
import requests
from flask import redirect, session, send_file 

import json
from Controllers.Graficos import *
from Controllers.dbControll import DatabaseConnection
import re


load_dotenv()

db = DatabaseConnection(host="localhost", dbname="pesquisaHPS", user="postgres", password="316214", port=5432)

# Cred para o token do Spotify 

client_id = os.getenv('CLIENT_ID') 
client_secret_spty = os.getenv('CLIENT_SECRET')
autt_url = os.getenv('AUTH_URL')
uri = os.getenv('REDIRECT_URI')
scope = os.getenv('SCOPE')
tokenURL = os.getenv('TOKEN_URL')

def acceptTermsSpotify():
    session.clear()
    autt_query = f"{autt_url}?response_type=code&client_id={client_id}&redirect_uri={uri}&scope={scope}"
    return redirect(autt_query)

def token_session(code):
    token_response = requests.post(tokenURL, {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': uri,
        'client_id': client_id,
        'client_secret': client_secret_spty
    })
    token_json = json.loads(token_response.content)
    token = token_json.get('access_token')
    
    session['token'] = token

    return token


#spotify busca por artista 
def buscaArtistaSpotify():
    artistName = session['artistName']
    token = session['token']
    artistType = session['artistType']


    headers = {
        'Authorization': f'Bearer {token}'
    }

    params = {
    'q': artistName,
    'type': 'artist',
    'limit': 1
    } 

    genres = [] 
    dictSpotifyMain = []
    
    requestURL = requests.get(f'https://api.spotify.com/v1/search', headers=headers, params=params)

    retorno = json.loads(requestURL.content)

    if 'artists' in retorno:

        for genre in retorno['artists']['items'][0]['genres']:
            genres.append(genre)

        session['genres'] = genres

        Followers = retorno['artists']['items'][0]['followers']['total']

        followers_formatado = "{:,}".format(Followers)
        followers_formatado = followers_formatado.replace(",", "X").replace(".", ",").replace("X", ".")

        idSpotify = retorno['artists']['items'][0]['id']

        session['idSpotify'] = idSpotify

        session['followers'] = followers_formatado

        session['genres'] = genres

        session['popularidade'] = retorno['artists']['items'][0]['popularity']

        dictSpotifyData = {'Nome': retorno['artists']['items'][0]['name'], 'Genres': genres, 'Followers': followers_formatado, 'id':retorno['artists']['items'][0]['id'], 'Tipo': artistType, 'Popularidade': retorno['artists']['items'][0]['popularity'], 'ImageURL': retorno['artists']['items'][0]['images'][0]['url']}
        dictSpotifyMain.append(dictSpotifyData)
    
        session['dictSpotifyMain'] = dictSpotifyMain

        return dictSpotifyMain
    else: 
        dictSpotifyMain = [{
            'Erro' : 'Não foi possível econtrar o artista que você buscou, tente novamente... :('
        }]

  #musicas mais ouvidas do artista  
def toptracks():
    idSpotify = session['idSpotify']
    token = session['token']
    headers = {
        'Authorization': f'Bearer {token}'
    }

    params = {
        'album': 'id',
        'limit': 5
    }
    
    response = requests.get(f'https://api.spotify.com/v1/artists/{idSpotify}/top-tracks', headers=headers, params=params)

    data = session['dictSpotifyMain']

    query = (f"select genre_id from genres where genre = '{data[0]['Genres'][-1]}';")

    genre_id = db.query_data(query)

    data[0]['Nome'] = re.sub(r"[^\w\s]", "", data[0]['Nome'])

    if len(genre_id) == 0:
        query = (f"insert into genres (genre) values ('{data[0]['Genres'][-1]}');")

        db.insert_data(query)

        query = (f"select genre_id from genres where genre = '{data[0]['Genres'][-1]}';")

        genre_id = db.query_data(query)

    query = (f"select id_spotify from artists where artist_name = '{data[0]['Nome']}';")

    id_spotify = db.query_data(query)

    if response.status_code == 200:
        if len(id_spotify) == 0 or id_spotify[0][0] != data[0]['id']:
            query = (f"insert into artists (artist_name, genre_id, followers, popularity, id_spotify, urlImg) values ('{data[0]['Nome']}', {genre_id[0][0]}, '{data[0]['Followers']}', {data[0]['Popularidade']}, '{data[0]['id']}', '{data[0]['ImageURL']}');")

            db.insert_data(query)
            return response.json()

        else:
            mensagem = 'Já inserido'
            print(mensagem)
            return response.json()
    
    else:
        print(f"Erro: {response.status_code} - {response.json()}")
        return None

# API TORNOU-SE OBSOLETA NO DIA 28/11/2024

# busca recomendações pelo id do artista pesquisado agora 
# def recomendations():

#     if not session or 'idSpotify' not in session or 'token' not in session:
#         mensagem = "Erro"
#         return mensagem

#     recomendedArtists = []
#     idSpotify = session['idSpotify']
#     token = session['token']
#     headers = {
#         'Authorization': f'Bearer {token}'
#     }

#     response = requests.get(f'https://api.spotify.com/v1/artists/{idSpotify}/related-artists', headers=headers)
    
#     if response.status_code == 200:
#         retorno = response.json()

#         for artist in retorno.get('artists', []):
#             dictArtistReco = {'Nome': artist['name'], 'id': artist['id'], 'image':artist['images'][0]}
#             recomendedArtists.append(dictArtistReco)



#         return recomendedArtists
    
#     else:
#         mensagem = "Erro"
#         return mensagem
    
def grafico():
    
    dados = dadosGraficoBusca()

    graficos = gerarGraficoBusca(dados)

    current_dir = os.path.dirname(__file__)
    path = os.path.abspath(os.path.join(current_dir, '..', 'Static', graficos))

    return path


