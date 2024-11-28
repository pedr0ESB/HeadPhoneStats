from flask import Blueprint, render_template, request
from Controllers.WebServiceSpotify import *
from Controllers.WebServiceMusicBrainz import *

BuscMSZ = Blueprint('Busca', __name__)

# -> ROTA BuscMSZ <- #
@BuscMSZ.route('/Busca', methods=['GET', 'POST'])
def buscaArtist():
    
    busca = []
    discos = []
    buscaSpotify = []

    if request.method == 'POST':
        artistName = request.form.get('artistName')
        busca = busArtista(artistName)
        
        discos = buscaDiscos()

        if 'Erro' not in discos:
            buscaSpotify = buscaArtistaSpotify()
            TopTracks = toptracks()
            Graficos = grafico()
        else:
            pass

        return render_template('busca.html', busca = busca, discos = discos, buscaSpotify= buscaSpotify, TopTracks=TopTracks, Graficos=Graficos)
    
    return render_template('busca.html', busca = busca)