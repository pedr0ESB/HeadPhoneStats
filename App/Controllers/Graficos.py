import matplotlib.pyplot as plt
import seaborn as sns
from flask import session
from Controllers.dbControll import *
import os

db = DatabaseConnection(host="localhost", dbname="pesquisaHPS", user="postgres", password="316214", port=5432)

def dadosGraficoBusca():

    query = (f"select artist_name, popularity, followers, urlimg from artists where artist_name != '{session['dictSpotifyMain'][0]['Nome']}' order by data_insert desc limit 4;")

    data = db.query_data(query)

    query = (f"select artist_name, popularity, followers, urlimg from artists where artist_name = '{session['dictSpotifyMain'][0]['Nome']}';")

    dataACT = db.query_data(query)

    data.append(dataACT[0])

    return data

def gerarGraficoBusca(dados):

    data = []

    for i, (dados) in enumerate(dados):
        datadict = {'Artistas': dados[0], 'Popularidade': dados[1], 'Seguidores': dados[2]}
        data.append(datadict)

    nomes = [d['Artistas'] for d in data]
    popularidade = [d['Popularidade'] for d in data]

    plt.figure(figsize=(10, 6))
    sns.barplot(x=popularidade, y=nomes, palette="viridis")
    plt.title('Popularidade dos Artistas')
    plt.xlabel('Popularidade')

    current_dir = os.path.dirname(__file__)
    path = os.path.abspath(os.path.join(current_dir, '..', 'Static', 'ArchImg'))

    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

    image_filename = f'grafico_popularidade_pesquisa{session['dictSpotifyMain'][0]["Nome"]}.png'
    image_path = os.path.join(path, image_filename)

    plt.savefig(image_path, format='png', dpi=300, bbox_inches='tight')

    plt.close()

    arquivo_path = os.path.join(path, image_filename)
    if os.path.exists(arquivo_path):
        ultimo_grafico = f'ArchImg/{image_filename}'
        return ultimo_grafico
    else:
        ultimo_grafico = None
        return ultimo_grafico