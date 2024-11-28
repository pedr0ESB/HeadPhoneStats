from flask import Blueprint, render_template, request
from Controllers.WebServiceSpotify import *
from Controllers.WebServiceMusicBrainz import *

Recomendation = Blueprint('Recomendacao', __name__)

# -> ROTA Recomendation <- # 

@Recomendation.route('/Recomendacoes', methods=['GET', 'POST'])
def recomendation():

    recomendation = []

    if request.method == 'POST':

        recomendation = recomendations()
        return render_template('recomendacoes.html', recomendation = recomendation)
    
    else:
        return render_template('recomendacoes.html', recomendation = recomendation)
    
@Recomendation.route('/Recomendacoes/grafico', methods=['GET'])
def open_file():
    file_path = open_file()
    return send_file(file_path, as_attachment=True)  